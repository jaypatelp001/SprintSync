"""Pydantic schemas for User request/response validation."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# --- Request Schemas ---

class UserRegister(BaseModel):
    """Registration request body."""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., max_length=100)
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """Login request body."""
    username: str
    password: str


class UserUpdate(BaseModel):
    """Update user request body."""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = Field(None, max_length=100)
    is_admin: Optional[bool] = None


# --- Response Schemas ---

class UserResponse(BaseModel):
    """User data returned to clients (no password)."""
    id: int
    username: str
    email: str
    is_admin: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """JWT token response after login/register."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
