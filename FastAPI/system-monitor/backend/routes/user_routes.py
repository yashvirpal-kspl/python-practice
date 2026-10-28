import secrets
import threading
import time
from collections import defaultdict, deque

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request

from config import settings
from models.monitor import KeyOut, Me, RegisterIn, VerifyIn
from security import Principal, get_principal
from services import alert_service, user_service

router = APIRouter(tags=["users"])

# Per-IP registration limiter (in memory, resets on restart).
# Behind a reverse proxy request.client is the proxy; run uvicorn with --proxy-headers.
_hits: dict[str, deque] = defaultdict(deque)
_hits_lock = threading.Lock()


def _rate_limit(ip: str):
    now = time.time()
    with _hits_lock:
        q = _hits[ip]
        while q and now - q[0] > 3600:
            q.popleft()
        if len(q) >= settings.register_per_ip_per_hour:
            raise HTTPException(429, "Too many registration attempts, try again later")
        q.append(now)


@router.post("/users/register", status_code=202)
def register(body: RegisterIn, request: Request, background: BackgroundTasks):
    """Email a verification code. The response is identical whether or not the address exists."""
    if not settings.allow_registration:
        raise HTTPException(403, "Registration is closed")
    if not alert_service.smtp_configured():
        raise HTTPException(503, "Registration unavailable: email is not configured on this server")
    _rate_limit(request.client.host if request.client else "unknown")
    background.add_task(user_service.start_registration, body.email)
    return {"detail": "If the address is valid, a verification code has been sent."}


@router.post("/users/verify", response_model=KeyOut)
def verify(body: VerifyIn):
    key = user_service.verify(body.email, body.code)
    if not key:
        raise HTTPException(400, "Invalid or expired code")
    return KeyOut(api_key=key)


@router.get("/me", response_model=Me)
def me(p: Principal = Depends(get_principal)):
    return Me(id=p.id, email=p.email, is_admin=p.is_admin)


@router.post("/me/rotate-key", response_model=KeyOut)
def rotate_key(p: Principal = Depends(get_principal)):
    if p.is_admin:
        raise HTTPException(400, "The admin key is set in .env")
    return KeyOut(api_key=user_service.rotate_key(p.id))


@router.delete("/me", status_code=204)
def delete_me(p: Principal = Depends(get_principal)):
    """Delete the account and all of its servers, history and alerts."""
    if p.is_admin:
        raise HTTPException(400, "The admin account cannot be deleted")
    user_service.delete_user(p.id)
