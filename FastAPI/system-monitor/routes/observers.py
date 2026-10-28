from fastapi import APIRouter, Depends, Query

from models.monitor import FileEvent
from security import require_admin
from services import observer

router = APIRouter(prefix="/files", tags=["files"], dependencies=[Depends(require_admin)])


@router.get("/events", response_model=list[FileEvent])
def file_events(limit: int = Query(50, ge=1, le=500)):
    return observer.list_events(limit)
