"""Unit tests for authentication domain logic."""
import re
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from jose import JWTError, jwt

from app.auth.security import (
    create_access_token,
    decode_access_token,
    generate_otp,
    get_password_hash,
    is_admin_or_super_admin,
    is_provisioning_specialist,
    is_super_admin,
    is_support_agent,
    verify_password,
)
from app.core.config.settings import settings
from app.core.models.user import User


class TestGenerateOTP:
    """Test OTP generation."""

    def test_generate_otp_default_length(self) -> None:
        """Test that OTP is generated with default length of 6."""
        otp = generate_otp()
        assert len(otp) == 6
        assert otp.isdigit()

    def test_generate_otp_custom_length(self) -> None:
        """Test that OTP can be generated with custom length."""
        otp = generate_otp(length=8)
        assert len(otp) == 8
        assert otp.isdigit()

    def test_generate_otp_numeric_only(self) -> None:
        """Test that OTP contains only numeric digits."""
        otp = generate_otp()
        assert re.match(r"^\d+$", otp) is not None

    def test_generate_otp_randomness(self) -> None:
        """Test that generated OTPs are different."""
        otps = [generate_otp() for _ in range(10)]
        assert len(set(otps)) > 1, "OTPs should be random"


class TestCreateAccessToken:
    """Test access token creation."""

    def test_create_access_token_with_subject(self) -> None:
        """Test that token is created with subject."""
        user_id = str(uuid4())
        token = create_access_token(subject=user_id)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_contains_subject(self) -> None:
        """Test that token contains the subject."""
        user_id = str(uuid4())
        token = create_access_token(subject=user_id)
        payload = decode_access_token(token)
        assert payload["sub"] == user_id

    def test_create_access_token_default_expiration(self) -> None:
        """Test that token has default expiration time."""
        user_id = str(uuid4())
        token = create_access_token(subject=user_id)
        payload = decode_access_token(token)
        assert "exp" in payload
        exp_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        expected_exp = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        assert abs((exp_time - expected_exp).total_seconds()) < 60

    def test_create_access_token_custom_expiration(self) -> None:
        """Test that token can have custom expiration time."""
        user_id = str(uuid4())
        custom_minutes = 30
        token = create_access_token(subject=user_id, expires_minutes=custom_minutes)
        payload = decode_access_token(token)
        exp_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        expected_exp = datetime.now(timezone.utc) + timedelta(minutes=custom_minutes)
        assert abs((exp_time - expected_exp).total_seconds()) < 60


class TestDecodeAccessToken:
    """Test access token decoding."""

    def test_decode_access_token_valid(self) -> None:
        """Test decoding a valid token."""
        user_id = str(uuid4())
        token = create_access_token(subject=user_id)
        payload = decode_access_token(token)
        assert payload["sub"] == user_id
        assert "exp" in payload

    def test_decode_access_token_invalid_format(self) -> None:
        """Test decoding an invalid token format."""
        invalid_token = "invalid.token.here"
        with pytest.raises(JWTError):
            decode_access_token(invalid_token)

    def test_decode_access_token_wrong_secret(self) -> None:
        """Test decoding a token with wrong secret key."""
        user_id = str(uuid4())
        # Try to decode with wrong secret
        wrong_secret = "wrong-secret-key"
        wrong_token = jwt.encode(
            {"sub": user_id, "exp": datetime.now(timezone.utc) + timedelta(minutes=60)},
            wrong_secret,
            algorithm=settings.ALGORITHM,
        )
        # Decoding with wrong secret should fail
        with pytest.raises(JWTError):
            decode_access_token(wrong_token)


class TestPasswordHashing:
    """Test password hashing and verification."""

    def test_get_password_hash_creates_hash(self) -> None:
        """Test that password hash is created."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        assert hashed != password

    def test_get_password_hash_different_for_same_password(self) -> None:
        """Test that same password produces different hashes (salt)."""
        password = "testpassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 != hash2

    def test_verify_password_correct(self) -> None:
        """Test verifying correct password."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self) -> None:
        """Test verifying incorrect password."""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)
        assert verify_password(wrong_password, hashed) is False

    def test_verify_password_empty(self) -> None:
        """Test verifying empty password."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        assert verify_password("", hashed) is False


class TestUserRoleChecks:
    """Test user role checking functions."""

    def test_is_super_admin_true(self, db_session) -> None:
        """Test is_super_admin returns True for super admin."""
        user = User(
            email="super@example.com",
            phone="+1234567890",
            is_super_admin=True,
            is_admin=False,
        )
        db_session.add(user)
        db_session.commit()
        assert is_super_admin(user) is True

    def test_is_super_admin_false(self, db_session) -> None:
        """Test is_super_admin returns False for non-super admin."""
        user = User(
            email="user@example.com",
            phone="+1234567891",
            is_super_admin=False,
            is_admin=False,
        )
        db_session.add(user)
        db_session.commit()
        assert is_super_admin(user) is False

    def test_is_admin_or_super_admin_super_admin(self, db_session) -> None:
        """Test is_admin_or_super_admin returns True for super admin."""
        user = User(
            email="super@example.com",
            phone="+1234567892",
            is_super_admin=True,
            is_admin=False,
        )
        db_session.add(user)
        db_session.commit()
        assert is_admin_or_super_admin(user) is True

    def test_is_admin_or_super_admin_admin(self, db_session) -> None:
        """Test is_admin_or_super_admin returns True for admin."""
        user = User(
            email="admin@example.com",
            phone="+1234567893",
            is_super_admin=False,
            is_admin=True,
        )
        db_session.add(user)
        db_session.commit()
        assert is_admin_or_super_admin(user) is True

    def test_is_admin_or_super_admin_regular_user(self, db_session) -> None:
        """Test is_admin_or_super_admin returns False for regular user."""
        user = User(
            email="user@example.com",
            phone="+1234567894",
            is_super_admin=False,
            is_admin=False,
        )
        db_session.add(user)
        db_session.commit()
        assert is_admin_or_super_admin(user) is False

    def test_is_admin_or_super_admin_both_true(self, db_session) -> None:
        """Test is_admin_or_super_admin returns True when both flags are True."""
        user = User(
            email="both@example.com",
            phone="+1234567895",
            is_super_admin=True,
            is_admin=True,
        )
        db_session.add(user)
        db_session.commit()
        assert is_admin_or_super_admin(user) is True


class TestSupportAgentChecks:
    """Test support agent checking functions."""

    def test_is_support_agent_true_for_support_agent(self, db_session) -> None:
        """Test is_support_agent returns True for support agent."""
        user = User(
            email="support@example.com",
            phone="+1234567890",
            is_super_admin=False,
            is_support_agent=True,
            is_provisioning_specialist=False,
        )
        db_session.add(user)
        db_session.commit()
        assert is_support_agent(user) is True

    def test_is_support_agent_true_for_super_admin(self, db_session) -> None:
        """Test is_support_agent returns True for super admin."""
        user = User(
            email="super@example.com",
            phone="+1234567891",
            is_super_admin=True,
            is_support_agent=False,
            is_provisioning_specialist=False,
        )
        db_session.add(user)
        db_session.commit()
        assert is_support_agent(user) is True

    def test_is_support_agent_false_for_regular_user(self, db_session) -> None:
        """Test is_support_agent returns False for regular user."""
        user = User(
            email="user@example.com",
            phone="+1234567892",
            is_super_admin=False,
            is_support_agent=False,
            is_provisioning_specialist=False,
        )
        db_session.add(user)
        db_session.commit()
        assert is_support_agent(user) is False

    def test_is_support_agent_false_for_provisioning_specialist_only(
        self, db_session
    ) -> None:
        """Test is_support_agent returns False for provisioning specialist only."""
        user = User(
            email="specialist@example.com",
            phone="+1234567893",
            is_super_admin=False,
            is_support_agent=False,
            is_provisioning_specialist=True,
        )
        db_session.add(user)
        db_session.commit()
        assert is_support_agent(user) is False


class TestProvisioningSpecialistChecks:
    """Test provisioning specialist checking functions."""

    def test_is_provisioning_specialist_true_for_specialist(self, db_session) -> None:
        """Test is_provisioning_specialist returns True for provisioning specialist."""
        user = User(
            email="specialist@example.com",
            phone="+1234567890",
            is_super_admin=False,
            is_support_agent=False,
            is_provisioning_specialist=True,
        )
        db_session.add(user)
        db_session.commit()
        assert is_provisioning_specialist(user) is True

    def test_is_provisioning_specialist_true_for_super_admin(self, db_session) -> None:
        """Test is_provisioning_specialist returns True for super admin."""
        user = User(
            email="super@example.com",
            phone="+1234567891",
            is_super_admin=True,
            is_support_agent=False,
            is_provisioning_specialist=False,
        )
        db_session.add(user)
        db_session.commit()
        assert is_provisioning_specialist(user) is True

    def test_is_provisioning_specialist_false_for_regular_user(
        self, db_session
    ) -> None:
        """Test is_provisioning_specialist returns False for regular user."""
        user = User(
            email="user@example.com",
            phone="+1234567892",
            is_super_admin=False,
            is_support_agent=False,
            is_provisioning_specialist=False,
        )
        db_session.add(user)
        db_session.commit()
        assert is_provisioning_specialist(user) is False

    def test_is_provisioning_specialist_false_for_support_agent_only(
        self, db_session
    ) -> None:
        """Test is_provisioning_specialist returns False for support agent only."""
        user = User(
            email="support@example.com",
            phone="+1234567893",
            is_super_admin=False,
            is_support_agent=True,
            is_provisioning_specialist=False,
        )
        db_session.add(user)
        db_session.commit()
        assert is_provisioning_specialist(user) is False
