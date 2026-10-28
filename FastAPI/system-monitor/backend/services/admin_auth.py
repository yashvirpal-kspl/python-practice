import hashlib
import hmac
import logging
import os
import secrets
import threading
import time
from collections import defaultdict, deque

from config import settings
from db import connect
from security import SESSION_PREFIX, hash_key

log = logging.getLogger("admin")

MIN_PASSWORD_LEN = 12
EMAIL_MAX_FAILURES = 20  # across all IPs, guards against distributed guessing
_N, _R, _P = 2**14, 8, 1  # scrypt cost


class AuthError(Exception):
    def __init__(self, status: int, detail: str):
        self.status, self.detail = status, detail


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    h = hashlib.scrypt(password.encode(), salt=salt, n=_N, r=_R, p=_P, dklen=32)
    return f"scrypt${_N}${_R}${_P}${salt.hex()}${h.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        _, n, r, p, salt, h = stored.split("$")
        expected = bytes.fromhex(h)
        calc = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt),
                              n=int(n), r=int(r), p=int(p), dklen=len(expected))
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(calc, expected)


# Verified against when the email is unknown, so timing doesn't reveal the admin's address
_DUMMY_HASH = hash_password("not-the-real-password")


def sync_admin():
    """Create or update the admin account from ADMIN_EMAIL / ADMIN_PASSWORD."""
    email = settings.admin_email.strip().lower()
    password = settings.admin_password
    with connect() as c:
        if not email or not password:
            c.execute("DELETE FROM admin_account")
            c.execute("DELETE FROM sessions")
            log.info("ADMIN_EMAIL / ADMIN_PASSWORD not set: admin password login is disabled")
            return
        if len(password) < MIN_PASSWORD_LEN:
            c.execute("DELETE FROM admin_account")
            c.execute("DELETE FROM sessions")
            log.error("ADMIN_PASSWORD must be at least %d characters: admin password login is disabled",
                      MIN_PASSWORD_LEN)
            return
        row = c.execute("SELECT email, password_hash FROM admin_account WHERE id=1").fetchone()
        if row and row["email"] == email and verify_password(password, row["password_hash"]):
            return
        c.execute(
            "INSERT INTO admin_account (id, email, password_hash) VALUES (1, ?, ?)"
            " ON CONFLICT(id) DO UPDATE SET email=excluded.email, password_hash=excluded.password_hash",
            (email, hash_password(password)),
        )
        c.execute("DELETE FROM sessions")  # credentials changed: sign everyone out
        log.info("Admin account set to %s", email)


# ---- brute-force protection (in memory, resets on restart) ----
_failures: dict[str, deque] = defaultdict(deque)
_lock = threading.Lock()


def _recent(key: str, now: float) -> deque:
    q = _failures[key]
    window = settings.login_lock_minutes * 60
    while q and now - q[0] > window:
        q.popleft()
    return q


def login(email: str, password: str, ip: str) -> tuple[str, int]:
    """Return (session_token, ttl_seconds) or raise AuthError."""
    email = email.strip().lower()
    ip_key, email_key = f"ip:{ip}", f"email:{email}"
    now = time.time()
    with _lock:
        if (len(_recent(ip_key, now)) >= settings.login_max_failures
                or len(_recent(email_key, now)) >= EMAIL_MAX_FAILURES):
            raise AuthError(429, "Too many failed attempts. Try again later.")

    with connect() as c:
        row = c.execute("SELECT email, password_hash FROM admin_account WHERE id=1").fetchone()
    email_ok = bool(row) and hmac.compare_digest(row["email"].encode(), email.encode())
    password_ok = verify_password(password, row["password_hash"] if row else _DUMMY_HASH)

    if not (email_ok and password_ok):
        with _lock:
            _failures[ip_key].append(now)
            _failures[email_key].append(now)
        raise AuthError(401, "Invalid email or password")

    with _lock:
        _failures.pop(ip_key, None)
        _failures.pop(email_key, None)
    token = SESSION_PREFIX + secrets.token_urlsafe(32)
    ttl = settings.admin_session_hours * 3600
    with connect() as c:
        c.execute("INSERT INTO sessions (token_hash, created, expires) VALUES (?,?,?)",
                  (hash_key(token), now, now + ttl))
    return token, ttl


def logout(token: str):
    if token.startswith(SESSION_PREFIX):
        with connect() as c:
            c.execute("DELETE FROM sessions WHERE token_hash=?", (hash_key(token),))


def prune_sessions():
    with connect() as c:
        c.execute("DELETE FROM sessions WHERE expires<?", (time.time(),))
