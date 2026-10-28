import hashlib
import secrets
from dataclasses import dataclass

from fastapi import Depends, Header, HTTPException, status

from config import settings
from db import connect


@dataclass
class Principal:
    id: int  # 0 = admin / the host itself
    email: str | None
    is_admin: bool


def hash_key(key: str) -> str:
    # API keys are high-entropy random strings, so a fast hash is sufficient
    return hashlib.sha256(key.encode()).hexdigest()


def get_principal(x_api_key: str = Header(default="")) -> Principal:
    unauthorized = HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or missing X-API-Key")
    if not x_api_key:
        raise unauthorized
    if settings.api_key and secrets.compare_digest(x_api_key, settings.api_key):
        return Principal(id=0, email=None, is_admin=True)
    with connect() as c:
        row = c.execute(
            "SELECT id, email FROM users WHERE key_hash=?", (hash_key(x_api_key),)
        ).fetchone()
    if not row:
        raise unauthorized
    return Principal(id=row["id"], email=row["email"], is_admin=False)


def require_admin(p: Principal = Depends(get_principal)) -> Principal:
    if not p.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin key required")
    return p
