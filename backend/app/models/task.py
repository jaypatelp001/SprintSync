"""Task ORM model with status enum and time tracking."""

import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class TaskStatus(str, enum.Enum):
    """Valid task statuses with defined transition rules."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"


# Allowed status transitions (current → set of valid next states)
VALID_TRANSITIONS = {
    TaskStatus.TODO: {TaskStatus.IN_PROGRESS},
    TaskStatus.IN_PROGRESS: {TaskStatus.REVIEW, TaskStatus.TODO},
    TaskStatus.REVIEW: {TaskStatus.DONE, TaskStatus.IN_PROGRESS},
    TaskStatus.DONE: {TaskStatus.TODO},  # reopen
}


class Task(Base):
    """Task table — work items with status tracking and time logging."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(
        Enum(TaskStatus), default=TaskStatus.TODO, nullable=False, index=True
    )
    total_minutes = Column(Integer, default=0, nullable=False)

    # Foreign keys
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    assignee = relationship(
        "User", back_populates="assigned_tasks", foreign_keys=[assignee_id]
    )
    creator = relationship(
        "User", back_populates="created_tasks", foreign_keys=[created_by]
    )

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
