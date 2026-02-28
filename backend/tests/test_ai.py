"""Integration test for /ai/suggest — hitting the deterministic stub."""


class TestAISuggestStub:
    """Integration tests for the AI suggest endpoint in stub mode."""

    def test_suggest_description_stub(self, client, auth_headers):
        """Integration test: /ai/suggest returns deterministic stub description."""
        response = client.post("/ai/suggest", json={
            "type": "description",
            "title": "Set up monitoring dashboard",
        }, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "description"
        assert data["is_stub"] is True
        assert "Set up monitoring dashboard" in data["suggestion"]
        assert "Key deliverables" in data["suggestion"]

    def test_suggest_daily_plan_stub(self, client, auth_headers, sample_task):
        """Integration test: /ai/suggest daily_plan returns predictable plan."""
        response = client.post("/ai/suggest", json={
            "type": "daily_plan",
        }, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "daily_plan"
        assert data["is_stub"] is True
        assert isinstance(data["suggestion"], str)
        assert len(data["suggestion"]) > 0

    def test_suggest_missing_title(self, client, auth_headers):
        """Description mode without title returns 400."""
        response = client.post("/ai/suggest", json={
            "type": "description",
        }, headers=auth_headers)

        assert response.status_code == 400
        assert "Title is required" in response.json()["detail"]

    def test_suggest_unauthenticated(self, client):
        """Unauthenticated request to /ai/suggest returns 403."""
        response = client.post("/ai/suggest", json={
            "type": "description",
            "title": "Test",
        })
        assert response.status_code == 403
