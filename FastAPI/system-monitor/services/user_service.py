import hashlib
import hmac
import secrets
import time

from config import settings
from db import connect
from security import hash_key
from services import alert_service

RESEND_GAP = 60  # seconds between verification emails for one address


def _hash_code(code: str) -> str:
    return hashlib.sha256(code.encode()).hexdigest()


def new_key() -> str:
    return "vpsm_" + secrets.token_urlsafe(32)


def start_registration(email: str):
    """Email a one-time code. Works for new users and for recovering a lost key.

    Returns nothing on purpose so callers can't tell whether an address already exists.
    """
    email = email.lower()
    now = time.time()
    code = secrets.token_urlsafe(12)
    with connect() as c:
        row = c.execute("SELECT id, verify_sent FROM users WHERE email=?", (email,)).fetchone()
        if row and row["verify_sent"] and now - row["verify_sent"] < RESEND_GAP:
            return
        expires = now + settings.verify_ttl_minutes * 60
        if row:
            c.execute("UPDATE users SET verify_hash=?, verify_expires=?, verify_sent=? WHERE id=?",
                      (_hash_code(code), expires, now, row["id"]))
        else:
            c.execute("INSERT INTO users (email, verify_hash, verify_expires, verify_sent, created)"
                      " VALUES (?,?,?,?,?)", (email, _hash_code(code), expires, now, now))
    alert_service.send_email(
        "Your VPS Monitor verification code",
        f"Your code: {code}\n\nIt expires in {settings.verify_ttl_minutes} minutes.\n"
        "Submit it to POST /users/verify together with your email to receive your API key.\n"
        "Verifying issues a NEW key and invalidates any previous one.\n"
        "If you didn't request this, ignore this email.",
        [email],
    )


def verify(email: str, code: str) -> str | None:
    """Return a fresh API key if the code is valid, else None."""
    email = email.lower()
    with connect() as c:
        row = c.execute("SELECT id, verify_hash, verify_expires FROM users WHERE email=?", (email,)).fetchone()
        if not row or not row["verify_hash"] or row["verify_expires"] < time.time():
            return None
        if not hmac.compare_digest(row["verify_hash"], _hash_code(code)):
            return None
        key = new_key()
        c.execute("UPDATE users SET key_hash=?, verify_hash=NULL, verify_expires=NULL WHERE id=?",
                  (hash_key(key), row["id"]))
    return key


def rotate_key(user_id: int) -> str:
    key = new_key()
    with connect() as c:
        c.execute("UPDATE users SET key_hash=? WHERE id=?", (hash_key(key), user_id))
    return key


def delete_user(user_id: int):
    with connect() as c:
        for table in ("samples", "alerts", "servers"):
            c.execute(f"DELETE FROM {table} WHERE user_id=?", (user_id,))
        c.execute("DELETE FROM users WHERE id=?", (user_id,))
