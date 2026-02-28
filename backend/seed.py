"""Seed script — populates the database with demo data."""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.database import engine, SessionLocal, Base
from app.models.user import User
from app.models.task import Task, TaskStatus
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed():
    """Create tables and insert demo users + tasks."""
    # Create all tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(User).first():
            print("Database already seeded. Skipping.")
            return

        # --- Users ---
        admin = User(
            username="admin",
            email="admin@sprintsync.dev",
            hashed_password=pwd_context.hash("admin123"),
            is_admin=True,
        )
        alice = User(
            username="alice",
            email="alice@sprintsync.dev",
            hashed_password=pwd_context.hash("alice123"),
            is_admin=False,
        )
        bob = User(
            username="bob",
            email="bob@sprintsync.dev",
            hashed_password=pwd_context.hash("bob123"),
            is_admin=False,
        )
        db.add_all([admin, alice, bob])
        db.flush()

        # --- Tasks ---
        tasks = [
            Task(
                title="Set up CI/CD pipeline",
                description="Configure GitHub Actions for lint, test, and deploy stages.",
                status=TaskStatus.DONE,
                total_minutes=120,
                assignee_id=alice.id,
                created_by=admin.id,
            ),
            Task(
                title="Design database schema",
                description="Create ERD and define SQLAlchemy models for User and Task entities.",
                status=TaskStatus.DONE,
                total_minutes=90,
                assignee_id=alice.id,
                created_by=admin.id,
            ),
            Task(
                title="Implement authentication",
                description="JWT-based auth with login, register, and protected route middleware.",
                status=TaskStatus.IN_PROGRESS,
                total_minutes=45,
                assignee_id=bob.id,
                created_by=admin.id,
            ),
            Task(
                title="Build task dashboard UI",
                description="React component showing filterable task list with status badges.",
                status=TaskStatus.TODO,
                total_minutes=0,
                assignee_id=bob.id,
                created_by=admin.id,
            ),
            Task(
                title="Integrate LLM for task suggestions",
                description="Connect to OpenAI API with fallback stub for automated task description generation.",
                status=TaskStatus.REVIEW,
                total_minutes=60,
                assignee_id=alice.id,
                created_by=admin.id,
            ),
        ]
        db.add_all(tasks)
        db.commit()

        print("✅ Seeded database with 3 users and 5 tasks.")
        print("   Users: admin/admin123 (admin), alice/alice123, bob/bob123")

    except Exception as e:
        db.rollback()
        print(f"❌ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
