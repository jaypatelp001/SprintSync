"""Shared test fixtures — in-memory SQLite test database and auth helpers."""

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Force stub mode and SQLite for tests
os.environ["AI_STUB_MODE"] = "false"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from app.database import Base, get_db
from app.main import app
from app.services.auth_service import create_access_token, hash_password
from app.models.user import User
from app.models.task import Task, TaskStatus

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(autouse=True)
def test_db():
    """Create fresh tables for each test, then tear down."""
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def db_session():
    """Direct database session for setup helpers."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_user(db_session):
    """Create and return a regular test user."""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("testpass123"),
        is_admin=False,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def admin_user(db_session):
    """Create and return an admin test user."""
    user = User(
        username="adminuser",
        email="admin@example.com",
        hashed_password=hash_password("adminpass123"),
        is_admin=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user):
    """Return auth headers for the test user."""
    token = create_access_token(test_user.id, test_user.is_admin)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(admin_user):
    """Return auth headers for the admin user."""
    token = create_access_token(admin_user.id, admin_user.is_admin)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_task(db_session, test_user):
    """Create and return a sample task."""
    task = Task(
        title="Sample Task",
        description="A test task",
        status=TaskStatus.TODO,
        total_minutes=0,
        created_by=test_user.id,
        assignee_id=test_user.id,
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task
