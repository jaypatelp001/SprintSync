"""Pydantic schemas for Task request/response validation."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.task import TaskStatus


# --- Request Schemas ---

class TaskCreate(BaseModel):
    """Create task request body."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    total_minutes: int = Field(default=0, ge=0)


class TaskUpdate(BaseModel):
    """Update task request body."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    total_minutes: Optional[int] = Field(None, ge=0)


class TaskStatusUpdate(BaseModel):
    """Status transition request body."""
    status: TaskStatus


class TaskLogTime(BaseModel):
    """Add minutes to a task."""
    minutes: int = Field(..., gt=0)


# --- Response Schemas ---

class TaskResponse(BaseModel):
    """Task data returned to clients."""
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    total_minutes: int
    assignee_id: Optional[int]
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskListResponse(BaseModel):
    """Paginated task list response."""
    tasks: list[TaskResponse]
    total: int
