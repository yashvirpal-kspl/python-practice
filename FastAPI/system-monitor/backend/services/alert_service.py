import logging
import smtplib
import ssl
import threading
import time
from email.message import EmailMessage

from config import settings
from db import connect
from services import system_service

log = logging.getLogger("alerts")

RANK = {"warning": 1, "critical": 2}

# (user_id, node, key) -> (level, last_emailed_ts). Guarded by _lock.
_state: dict[tuple[int, str, str], tuple[str, float]] = {}
_lock = threading.Lock()


def smtp_configured() -> bool:
    return bool(settings.smtp_host)


def email_configured() -> bool:
    return smtp_configured() and bool(settings.recipients)


def send_email(subject: str, body: str, recipients: list[str] | None = None) -> bool:
    """Send to `recipients`, or to ALERT_TO when not given."""
    to = recipients or settings.recipients
    if not smtp_configured() or not to:
        log.warning("Email not configured, skipping: %s", subject)
        return False
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.smtp_from or settings.smtp_user
    msg["To"] = ", ".join(to)
    msg.set_content(body)
    try:
        if settings.smtp_ssl:
            server = smtplib.SMTP_SSL(
                settings.smtp_host, settings.smtp_port,
                context=ssl.create_default_context(), timeout=15,
            )
        else:
            server = smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15)
        with server:
            if not settings.smtp_ssl:
                server.starttls(context=ssl.create_default_context())
            if settings.smtp_user:
                server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(msg)
        return True
    except Exception:
        log.exception("Failed to send email")
        return False


def _log_alerts(user_id: int, node: str, items: list[tuple[str, str]], emailed: bool):
    now = time.time()
    with connect() as c:
        c.executemany(
            "INSERT INTO alerts (user_id, node, ts, level, message, emailed) VALUES (?,?,?,?,?,?)",
            [(user_id, node, now, level, msg, int(emailed)) for level, msg in items],
        )


def process(node: str, snapshot: dict | None, error: str | None = None,
            user_id: int = 0, recipients: list[str] | None = None):
    """Evaluate a snapshot and email on new, escalated, stale or recovered alerts.

    snapshot=None means the node could not be reached. `recipients` defaults to ALERT_TO.
    """
    if snapshot is None:
        found = [{"key": "unreachable", "level": "critical",
                  "message": f"Server unreachable ({error})"}]
    else:
        found = system_service.evaluate(snapshot)

    now = time.time()
    fire, recovered = [], []
    with _lock:
        active = set()
        for a in found:
            k = (user_id, node, a["key"])
            active.add(k)
            prev = _state.get(k)
            if prev is None or RANK[a["level"]] > RANK[prev[0]] or now - prev[1] >= settings.alert_cooldown:
                _state[k] = (a["level"], now)
                fire.append(a)
            else:
                _state[k] = (a["level"], prev[1])  # level may have dropped; keep timer
        for k in [k for k in _state if k[:2] == (user_id, node) and k not in active]:
            del _state[k]
            recovered.append(k[2])

    if not fire and not recovered:
        return

    lines = [f"[{a['level'].upper()}] {a['message']}" for a in fire]
    lines += [f"[RESOLVED] {key}" for key in recovered]
    worst = "CRITICAL" if any(a["level"] == "critical" for a in fire) else "WARNING" if fire else "RESOLVED"
    body = f"Node: {node}\n\n" + "\n".join(lines)
    sent = send_email(f"[{worst}] {node}: {len(lines)} alert(s)", body, recipients)

    _log_alerts(user_id, node, [(a["level"], a["message"]) for a in fire]
                + [("resolved", f"{key} recovered") for key in recovered], sent)


def list_alerts(user_id: int, limit: int, node: str | None = None) -> list[dict]:
    q, args = "SELECT * FROM alerts WHERE user_id=?", [user_id]
    if node:
        q += " AND node=?"
        args.append(node)
    q += " ORDER BY ts DESC LIMIT ?"
    args.append(limit)
    with connect() as c:
        return [dict(r) for r in c.execute(q, args)]
