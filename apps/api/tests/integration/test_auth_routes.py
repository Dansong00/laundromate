"""
Integration tests for authentication routes.
"""

from fastapi.testclient import TestClient

from app.core.models.user import User


class TestAuthRoutes:
    """Test authentication endpoints."""

    def test_register_user_success(
        self, client: TestClient, sample_user_data: dict
    ) -> None:
        """Test successful user registration."""
        response = client.post("/auth/register", json=sample_user_data)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["first_name"] == sample_user_data["first_name"]
        assert "id" in data
        assert "hashed_password" not in data  # Should not expose password

    def test_register_user_duplicate_email(
        self, client: TestClient, test_user: User, sample_user_data: dict
    ) -> None:
        """Test registration with duplicate email fails."""
        sample_user_data["email"] = test_user.email

        response = client.post("/auth/register", json=sample_user_data)

        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_login_success(self, client: TestClient, test_user: User) -> None:
        """Test successful user login."""
        login_data = {"email": test_user.email, "password": "testpassword123"}

        response = client.post("/auth/login", json=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(
        self, client: TestClient, test_user: User
    ) -> None:
        """Test login with invalid credentials fails."""
        login_data = {"email": test_user.email, "password": "wrongpassword"}

        response = client.post("/auth/login", json=login_data)

        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]
