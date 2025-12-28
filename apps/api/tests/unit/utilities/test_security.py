"""Unit tests for security utility functions."""
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
    is_super_admin,
    verify_password,
)
from app.core.config.settings import settings
from app.core.models.user import User


class TestGenerateOTP:
    """Test OTP generation utility."""

    def test_generate_otp_default_length(self) -> None:
        """Test that OTP is generated with default length of 6."""
        otp = generate_otp()
        assert len(otp) == 6
        assert otp.isdigit()

    def test_generate_otp_custom_length(self) -> None:
        """Test that OTP can be generated with custom length."""
        for length in [4, 6, 8, 10]:
            otp = generate_otp(length=length)
            assert len(otp) == length
            assert otp.isdigit()

    def test_generate_otp_numeric_only(self) -> None:
        """Test that OTP contains only numeric digits."""
        otp = generate_otp()
        assert re.match(r"^\d+$", otp) is not None

    def test_generate_otp_randomness(self) -> None:
        """Test that generated OTPs are different."""
        otps = [generate_otp() for _ in range(20)]
        unique_otps = set(otps)
        assert len(unique_otps) > 1, "OTPs should be random"


class TestCreateAccessToken:
    """Test access token creation utility."""

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
        # Allow 60 second tolerance
        assert abs((exp_time - expected_exp).total_seconds()) < 60

    def test_create_access_token_custom_expiration(self) -> None:
        """Test that token can have custom expiration time."""
        user_id = str(uuid4())
        custom_minutes = 30
        token = create_access_token(subject=user_id, expires_minutes=custom_minutes)
        payload = decode_access_token(token)
        exp_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        expected_exp = datetime.now(timezone.utc) + timedelta(minutes=custom_minutes)
        # Allow 60 second tolerance
        assert abs((exp_time - expected_exp).total_seconds()) < 60

    def test_create_access_token_different_subjects(self) -> None:
        """Test that different subjects create different tokens."""
        user_id1 = str(uuid4())
        user_id2 = str(uuid4())
        token1 = create_access_token(subject=user_id1)
        token2 = create_access_token(subject=user_id2)
        assert token1 != token2


class TestDecodeAccessToken:
    """Test access token decoding utility."""

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

    def test_decode_access_token_expired(self) -> None:
        """Test decoding an expired token."""
        user_id = str(uuid4())
        # Create expired token
        expired_payload = {
            "sub": user_id,
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
        }
        expired_token = jwt.encode(
            expired_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        # Decoding expired token should fail
        with pytest.raises(JWTError):
            decode_access_token(expired_token)


class TestPasswordHashing:
    """Test password hashing and verification utilities."""

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

    def test_get_password_hash_always_produces_hash(self) -> None:
        """Test that hash is always produced, even for empty string."""
        hashed = get_password_hash("")
        assert isinstance(hashed, str)
        assert len(hashed) > 0

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

    def test_verify_password_case_sensitive(self) -> None:
        """Test that password verification is case sensitive."""
        password = "TestPassword123"
        hashed = get_password_hash(password)
        assert verify_password("testpassword123", hashed) is False
        assert verify_password("TestPassword123", hashed) is True

    def test_verify_password_special_characters(self) -> None:
        """Test password with special characters."""
        password = "P@ssw0rd!#$%"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True
        assert verify_password("P@ssw0rd!#$", hashed) is False


class TestUserRoleChecks:
    """Test user role checking utilities."""

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
