"""
Integration tests for authentication routes.
"""

from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.models.verification_code import VerificationCode


class TestAuthRoutes:
    """Test authentication endpoints."""

    def test_request_otp_success(self, client: TestClient) -> None:
        """Test requesting an OTP."""
        payload = {"phone": "+1234567890"}
        response = client.post("/auth/otp/request", json=payload)

        assert response.status_code == 200
        assert response.json()["message"] == "OTP sent successfully"

    def test_verify_otp_success(self, client: TestClient, db_session: Session) -> None:
        """Test verifying a valid OTP."""
        phone = "+1234567890"
        code = "123456"

        # Create a valid OTP in DB
        otp = VerificationCode(
            phone=phone,
            code=code,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
            is_used=False,
        )
        db_session.add(otp)
        db_session.commit()

        payload = {"phone": phone, "code": code}
        response = client.post("/auth/otp/verify", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["phone"] == phone

    def test_verify_otp_invalid(self, client: TestClient, db_session: Session) -> None:
        """Test verifying an invalid OTP."""
        phone = "+1234567890"

        # Create a valid OTP in DB
        otp = VerificationCode(
            phone=phone,
            code="123456",
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
            is_used=False,
        )
        db_session.add(otp)
        db_session.commit()

        # Try with wrong code
        payload = {"phone": phone, "code": "000000"}
        response = client.post("/auth/otp/verify", json=payload)

        assert response.status_code == 400
        assert "Invalid or expired OTP" in response.json()["detail"]

    def test_verify_otp_expired(self, client: TestClient, db_session: Session) -> None:
        """Test verifying an expired OTP."""
        phone = "+1234567890"
        code = "123456"

        # Create an expired OTP in DB
        otp = VerificationCode(
            phone=phone,
            code=code,
            expires_at=datetime.now(timezone.utc) - timedelta(minutes=1),
            is_used=False,
        )
        db_session.add(otp)
        db_session.commit()

        payload = {"phone": phone, "code": code}
        response = client.post("/auth/otp/verify", json=payload)

        assert response.status_code == 400
        assert "Invalid or expired OTP" in response.json()["detail"]
