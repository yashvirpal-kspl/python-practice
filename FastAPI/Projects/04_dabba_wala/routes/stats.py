from datetime import datetime,date
from fastapi import APIRouter,Depends,Query
from database import get_session
from models import Order,OrderStatus
from sqlmodel import select,Session,func

router = APIRouter(prefix="/stats",tags=["Stats"])

@router.get("/daily",summary="Get daily order statistics")
def daily_summary(
    session:Session = Depends(get_session),
    summary_date: date | None = Query(default=None,description="Date for summary in YYYY-MM-DD format")
):
    if summary_date is None:
        summary_date = date.today()
        
    start = datetime.combine(summary_date,datetime.min.time())
    end = datetime.combine(summary_date,datetime.max.time())
    
    summary = {}
    total = 0
    
    for status in OrderStatus:
        count = session.exec(
            select(func.count(Order.id)).where(
                Order.status == status,
                Order.created_at >= start,
                Order.created_at <= end
            )
        ).one()
        
        summary[status.value] = count
        total += count
        
    result = {
        
    "date": summary_date.isoformat(),
    "total_orders": total,  
    "by_status": summary
    }
    return result
