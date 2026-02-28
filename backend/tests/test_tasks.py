"""Unit tests for task CRUD — happy paths."""


class TestCreateTask:
    """Tests for POST /tasks."""

    def test_create_task_success(self, client, auth_headers):
        """Happy path: create a new task returns 201."""
        response = client.post("/tasks/", json={
            "title": "Write unit tests",
            "description": "Cover auth and task endpoints",
        }, headers=auth_headers)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Write unit tests"
        assert data["status"] == "todo"
        assert data["total_minutes"] == 0

    def test_create_task_unauthenticated(self, client):
        """Creating a task without auth returns 403."""
        response = client.post("/tasks/", json={
            "title": "Should fail",
        })
        assert response.status_code == 403


class TestListTasks:
    """Tests for GET /tasks."""

    def test_list_tasks(self, client, auth_headers, sample_task):
        """Happy path: list returns tasks with total count."""
        response = client.get("/tasks/", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert len(data["tasks"]) >= 1

    def test_filter_by_status(self, client, auth_headers, sample_task):
        """Filtering by status returns matching tasks."""
        response = client.get("/tasks/?status=todo", headers=auth_headers)

        assert response.status_code == 200
        tasks = response.json()["tasks"]
        for task in tasks:
            assert task["status"] == "todo"


class TestTaskStatusTransition:
    """Tests for PATCH /tasks/{id}/status."""

    def test_valid_transition(self, client, auth_headers, sample_task):
        """TODO → IN_PROGRESS is a valid transition."""
        response = client.patch(
            f"/tasks/{sample_task.id}/status",
            json={"status": "in_progress"},
            headers=auth_headers,
        )

        assert response.status_code == 200
        assert response.json()["status"] == "in_progress"

    def test_invalid_transition(self, client, auth_headers, sample_task):
        """TODO → DONE is not allowed (must go through in_progress + review)."""
        response = client.patch(
            f"/tasks/{sample_task.id}/status",
            json={"status": "done"},
            headers=auth_headers,
        )

        assert response.status_code == 400
        assert "Cannot transition" in response.json()["detail"]
