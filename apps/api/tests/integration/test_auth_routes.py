"""
Integration tests for authentication routes.
"""

from fastapi.testclient import TestClient

from app.auth.security import create_access_token


class TestAuthRoutes:
    """Test authentication endpoints."""

    def test_me_requires_auth(self, client: TestClient) -> None:
        """GET /auth/me returns 401 without token."""
        response = client.get("/auth/me")
        assert response.status_code == 401

    def test_me_success(self, client: TestClient, test_user) -> None:
        """GET /auth/me returns current user with valid token."""
        token = create_access_token(subject=str(test_user.id))
        response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_user.id)
        assert data["phone"] == test_user.phone
