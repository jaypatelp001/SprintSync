"""AI router — /ai/suggest endpoint for LLM-powered planning assistance."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.task import Task
from app.schemas.ai import AISuggestRequest, AISuggestResponse
from app.services.ai_service import suggest_description, suggest_daily_plan
from app.dependencies import get_current_user

router = APIRouter(prefix="/ai", tags=["AI Assist"])


@router.post("/suggest", response_model=AISuggestResponse)
async def ai_suggest(
    payload: AISuggestRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """AI-powered suggestions.

    Supports two modes:
    - **description**: Generate a task description from a short title.
    - **daily_plan**: Generate a concise daily plan based on the user's current tasks.
    """
    if payload.type == "description":
        if not payload.title:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title is required for description suggestions",
            )
        result = await suggest_description(payload.title)
        return AISuggestResponse(type="description", **result)

    elif payload.type == "daily_plan":
        # Get tasks assigned to or created by the current user
        from sqlalchemy import or_
        user_tasks = (
            db.query(Task)
            .filter(
                or_(
                    Task.assignee_id == current_user.id,
                    Task.created_by == current_user.id,
                )
            )
            .all()
        )
        result = await suggest_daily_plan(user_tasks)
        return AISuggestResponse(type="daily_plan", **result)

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid suggestion type. Use 'description' or 'daily_plan'.",
        )
