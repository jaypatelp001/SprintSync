"""Stats router — aggregate endpoints (stretch goal)."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func


from app.database import get_db
from app.models.user import User
from app.models.task import Task
from app.dependencies import get_current_user

router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get("/top-users")
def top_users(
    days: int = Query(7, ge=1, le=90, description="Lookback period in days"),
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Top users by total logged minutes within the lookback period.

    Returns the top N users ranked by their total_minutes on assigned tasks.
    """
    results = (
        db.query(
            User.id,
            User.username,
            func.coalesce(func.sum(Task.total_minutes), 0).label("total_minutes"),
            func.count(Task.id).label("task_count"),
        )
        .outerjoin(Task, Task.assignee_id == User.id)
        .group_by(User.id, User.username)
        .order_by(func.coalesce(func.sum(Task.total_minutes), 0).desc())
        .limit(limit)
        .all()
    )

    return {
        "period_days": days,
        "top_users": [
            {
                "user_id": r.id,
                "username": r.username,
                "total_minutes": r.total_minutes,
                "task_count": r.task_count,
            }
            for r in results
        ],
    }


@router.get("/cycle-time")
def average_cycle_time(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Average cycle time per status — time tasks spend in each status.

    Note: In a production system this would use status change event logs.
    For MVP, we report task counts and average minutes by status.
    """
    results = (
        db.query(
            Task.status,
            func.count(Task.id).label("count"),
            func.coalesce(func.avg(Task.total_minutes), 0).label("avg_minutes"),
        )
        .group_by(Task.status)
        .all()
    )

    return {
        "cycle_time_by_status": [
            {
                "status": r.status.value,
                "task_count": r.count,
                "avg_minutes": round(float(r.avg_minutes), 1),
            }
            for r in results
        ],
    }
