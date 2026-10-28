import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

import httpx
from pydantic import ValidationError

from config import settings
from db import connect
from models.monitor import SystemSnapshot
from netguard import check_url
from services import alert_service, history_service, system_service

log = logging.getLogger("collector")

MAX_RESPONSE_BYTES = 1_000_000
POLL_WORKERS = 10


def list_servers(user_id: int | None = None, enabled_only: bool = False) -> list[dict]:
    """Servers with the owner's email attached (None for the admin / host)."""
    q = ("SELECT s.*, u.email AS owner_email FROM servers s"
         " LEFT JOIN users u ON u.id = s.user_id WHERE 1=1")
    args = []
    if user_id is not None:
        q += " AND s.user_id=?"
        args.append(user_id)
    if enabled_only:
        q += " AND s.enabled=1"
    q += " ORDER BY s.user_id, s.name"
    with connect() as c:
        return [dict(r) for r in c.execute(q, args)]


def _fetch(server: dict, client: httpx.Client) -> dict:
    # Non-admin users must not be able to point us at internal addresses
    if server["user_id"] != 0 and not settings.allow_private_urls:
        check_url(server["url"])
    r = client.get(
        server["url"].rstrip("/") + "/system",
        headers={"X-API-Key": server["api_key"]},
    )
    r.raise_for_status()
    if len(r.content) > MAX_RESPONSE_BYTES:
        raise ValueError("response too large")
    # Validate the shape; never trust a remote's payload
    return SystemSnapshot.model_validate(r.json()).model_dump()


def _poll_remote(server: dict, client: httpx.Client):
    name, uid = server["name"], server["user_id"]
    recipients = [server["owner_email"]] if server["owner_email"] else None
    try:
        snap = _fetch(server, client)
    except (httpx.HTTPError, ValueError, ValidationError) as e:
        log.warning("Poll failed for %s (user %s): %s", name, uid, e)
        alert_service.process(name, None, error=str(e)[:200] or type(e).__name__,
                              user_id=uid, recipients=recipients)
        return
    history_service.record_sample(name, snap, user_id=uid)
    alert_service.process(name, snap, user_id=uid, recipients=recipients)


def collect_once():
    snap = system_service.get_system_info()
    history_service.record_sample(settings.node_name, snap)
    alert_service.process(settings.node_name, snap)

    servers = list_servers(enabled_only=True)
    if servers:
        # follow_redirects stays off: a redirect could bypass the URL check
        with httpx.Client(timeout=8, follow_redirects=False) as client, \
                ThreadPoolExecutor(max_workers=POLL_WORKERS) as pool:
            list(pool.map(lambda s: _poll_remote(s, client), servers))

    history_service.prune()


async def run_collector():
    while True:
        try:
            await asyncio.to_thread(collect_once)
        except Exception:
            log.exception("Collector cycle failed")
        await asyncio.sleep(settings.sample_interval)
