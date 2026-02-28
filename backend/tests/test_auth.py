"""Unit tests for authentication — happy paths."""


class TestRegister:
    """Tests for POST /auth/register."""

    def test_register_new_user(self, client):
        """Happy path: register a new user returns 201 with token."""
        response = client.post("/auth/register", json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "securepass123",
        })

        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["username"] == "newuser"
        assert data["user"]["email"] == "new@example.com"
        assert data["user"]["is_admin"] is False

    def test_register_duplicate_username(self, client, test_user):
        """Registering with an existing username returns 409."""
        response = client.post("/auth/register", json={
            "username": "testuser",
            "email": "different@example.com",
            "password": "somepassword",
        })

        assert response.status_code == 409
        assert "Username already taken" in response.json()["detail"]


class TestLogin:
    """Tests for POST /auth/login."""

    def test_login_valid_credentials(self, client, test_user):
        """Happy path: login with valid credentials returns token."""
        response = client.post("/auth/login", json={
            "username": "testuser",
            "password": "testpass123",
        })

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["user"]["username"] == "testuser"

    def test_login_invalid_password(self, client, test_user):
        """Login with wrong password returns 401."""
        response = client.post("/auth/login", json={
            "username": "testuser",
            "password": "wrongpassword",
        })

        assert response.status_code == 401


class TestAuthMe:
    """Tests for GET /auth/me."""

    def test_get_current_user(self, client, auth_headers):
        """Authenticated user can retrieve their own profile."""
        response = client.get("/auth/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"

    def test_unauthenticated_request(self, client):
        """Request without token returns 403."""
        response = client.get("/auth/me")
        assert response.status_code == 403
