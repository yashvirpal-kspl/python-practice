from fastapi import APIRouter, Depends, Query

from models.monitor import AdminAlert, AdminUser, Overview, Sample
from security import require_admin
from services import admin_service, history_service

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])


@router.get("/overview", response_model=Overview)
def overview():
    """Every monitored server (this host first) with its latest metrics and status."""
    return admin_service.overview()


@router.get("/users", response_model=list[AdminUser])
def users():
    return admin_service.list_users()


@router.get("/history", response_model=list[Sample])
def history(
    user_id: int = Query(ge=0),
    node: str = Query(min_length=1, max_length=100),
    minutes: int = Query(60, ge=1, le=60 * 24 * 30),
    limit: int = Query(500, ge=1, le=5000),
):
    """History of any user's server. user_id 0 is the host and the admin's own servers."""
    return history_service.get_history(user_id, node, minutes, limit)


@router.get("/alerts", response_model=list[AdminAlert])
def alerts(limit: int = Query(50, ge=1, le=500)):
    """Alerts across all users."""
    return admin_service.list_alerts(limit)
