"""Pydantic schemas for AI suggest endpoint."""

from pydantic import BaseModel, Field
from typing import Optional, Literal


class AISuggestRequest(BaseModel):
    """Request body for /ai/suggest."""
    type: Literal["description", "daily_plan"] = "description"
    title: Optional[str] = Field(None, min_length=1, max_length=200)


class AISuggestResponse(BaseModel):
    """Response from /ai/suggest."""
    type: str
    suggestion: str
    is_stub: bool = False
    warning: Optional[str] = None
