from fastapi import APIRouter, Header, HTTPException, Request

from models.monitor import AdminLoginIn, SessionOut
from services import admin_auth

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/admin/login", response_model=SessionOut)
def admin_login(body: AdminLoginIn, request: Request):
    """Admin sign-in with email + password. Returns a session token to send as X-API-Key."""
    ip = request.client.host if request.client else "unknown"
    try:
        token, ttl = admin_auth.login(body.email, body.password, ip)
    except admin_auth.AuthError as e:
        raise HTTPException(e.status, e.detail)
    return SessionOut(token=token, expires_in=ttl)


@router.post("/logout", status_code=204)
def logout(x_api_key: str = Header(default="")):
    """Ends an admin session. Does nothing for API keys."""
    admin_auth.logout(x_api_key)
