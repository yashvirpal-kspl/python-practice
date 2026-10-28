import time

from config import settings
from db import connect

_SERVERS_SQL = """
SELECT s.user_id, s.name, s.url, s.enabled, u.email AS owner_email,
       m.ts, m.cpu, m.mem, m.disk, m.load1
FROM servers s
LEFT JOIN users u ON u.id = s.user_id
LEFT JOIN samples m ON m.id = (
    SELECT id FROM samples WHERE user_id = s.user_id AND node = s.name ORDER BY ts DESC LIMIT 1
)
ORDER BY s.user_id, s.name
"""


def _status(enabled: bool, ts: float | None) -> str:
    if not enabled:
        return "disabled"
    if ts is None:
        return "pending"  # added but not polled yet
    # allow a few missed cycles before calling it down
    return "down" if time.time() - ts > max(3 * settings.sample_interval, 180) else "ok"


def overview() -> dict:
    with connect() as c:
        rows = c.execute(_SERVERS_SQL).fetchall()
        host = c.execute(
            "SELECT ts, cpu, mem, disk, load1 FROM samples WHERE user_id=0 AND node=?"
            " ORDER BY ts DESC LIMIT 1",
            (settings.node_name,),
        ).fetchone()
        user_count = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    items = [{
        "user_id": 0,
        "owner_email": None,
        "name": settings.node_name,
        "url": None,
        "enabled": True,
        "is_host": True,
        "status": _status(True, host["ts"] if host else None),
        "last_seen": host["ts"] if host else None,
        "cpu": host["cpu"] if host else None,
        "mem": host["mem"] if host else None,
        "disk": host["disk"] if host else None,
        "load1": host["load1"] if host else None,
    }]
    for r in rows:
        items.append({
            "user_id": r["user_id"],
            "owner_email": r["owner_email"],
            "name": r["name"],
            "url": r["url"],
            "enabled": bool(r["enabled"]),
            "is_host": False,
            "status": _status(bool(r["enabled"]), r["ts"]),
            "last_seen": r["ts"],
            "cpu": r["cpu"],
            "mem": r["mem"],
            "disk": r["disk"],
            "load1": r["load1"],
        })
    return {"users": user_count, "servers": len(rows), "items": items}


def list_users() -> list[dict]:
    with connect() as c:
        rows = c.execute(
            "SELECT u.id, u.email, u.created, u.key_hash IS NOT NULL AS has_key,"
            " (SELECT COUNT(*) FROM servers WHERE user_id = u.id) AS servers"
            " FROM users u ORDER BY u.created DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def list_alerts(limit: int) -> list[dict]:
    with connect() as c:
        rows = c.execute(
            "SELECT a.*, u.email AS owner_email FROM alerts a"
            " LEFT JOIN users u ON u.id = a.user_id ORDER BY a.ts DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]
