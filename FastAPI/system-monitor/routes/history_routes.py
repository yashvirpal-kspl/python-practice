from fastapi import APIRouter, Depends, HTTPException, Query

from config import settings
from models.monitor import AlertRecord, Sample
from security import Principal, get_principal
from services import alert_service, history_service

router = APIRouter(tags=["history"])


@router.get("/history", response_model=list[Sample])
def history(
    node: str | None = Query(default=None, description="Server name; admin defaults to this host"),
    minutes: int = Query(60, ge=1, le=60 * 24 * 30),
    limit: int = Query(500, ge=1, le=5000),
    p: Principal = Depends(get_principal),
):
    if node is None:
        if not p.is_admin:
            raise HTTPException(400, "node is required, see /history/nodes")
        node = settings.node_name
    return history_service.get_history(p.id, node, minutes, limit)


@router.get("/history/nodes", response_model=list[str])
def nodes(p: Principal = Depends(get_principal)):
    return history_service.get_nodes(p.id)


@router.get("/alerts", response_model=list[AlertRecord])
def alerts(limit: int = Query(50, ge=1, le=500), node: str | None = None,
           p: Principal = Depends(get_principal)):
    return alert_service.list_alerts(p.id, limit, node)


@router.post("/alerts/test")
def test_email(p: Principal = Depends(get_principal)):
    """Send a test email to your own address (the admin's goes to ALERT_TO)."""
    recipients = [p.email] if p.email else None
    if not alert_service.smtp_configured() or not (recipients or settings.recipients):
        raise HTTPException(400, "Email is not configured")
    ok = alert_service.send_email(
        "[TEST] VPS Monitor alert", "If you can read this, email alerts are working.", recipients,
    )
    if not ok:
        raise HTTPException(502, "Sending failed, check server logs")
    return {"sent_to": recipients or settings.recipients}
