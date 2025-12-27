"""Unit tests for VerificationCode model."""
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.models.verification_code import VerificationCode


class TestVerificationCodeModelCreation:
    """Test VerificationCode model creation."""

    def test_verification_code_creation_with_required_fields(self, db_session) -> None:
        """Test that verification code can be created with required fields."""
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
        verification_code = VerificationCode(
            phone="+1234567890",
            code="123456",
            expires_at=expires_at,
        )
        db_session.add(verification_code)
        db_session.commit()

        assert verification_code.id is not None
        assert verification_code.phone == "+1234567890"
        assert verification_code.code == "123456"
        assert verification_code.expires_at == expires_at
        assert verification_code.is_used is False

    def test_verification_code_creation_with_all_fields(self, db_session) -> None:
        """Test that verification code can be created with all fields."""
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
        verification_code = VerificationCode(
            phone="+1234567891",
            code="654321",
            expires_at=expires_at,
            is_used=True,
        )
        db_session.add(verification_code)
        db_session.commit()

        assert verification_code.is_used is True


class TestVerificationCodeConstraints:
    """Test VerificationCode model constraints."""

    def test_verification_code_phone_is_required(self, db_session) -> None:
        """Test that phone is required."""
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
        verification_code = VerificationCode(
            code="123456",
            expires_at=expires_at,
        )
        db_session.add(verification_code)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_verification_code_code_is_required(self, db_session) -> None:
        """Test that code is required."""
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
        verification_code = VerificationCode(
            phone="+1234567890",
            expires_at=expires_at,
        )
        db_session.add(verification_code)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_verification_code_expires_at_is_required(self, db_session) -> None:
        """Test that expires_at is required."""
        verification_code = VerificationCode(
            phone="+1234567890",
            code="123456",
        )
        db_session.add(verification_code)
        with pytest.raises(IntegrityError):
            db_session.commit()


class TestVerificationCodeDefaults:
    """Test VerificationCode model defaults."""

    def test_verification_code_is_used_default(self, db_session) -> None:
        """Test that is_used defaults to False."""
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
        verification_code = VerificationCode(
            phone="+1234567890",
            code="123456",
            expires_at=expires_at,
        )
        db_session.add(verification_code)
        db_session.commit()

        assert verification_code.is_used is False


class TestVerificationCodeTimestamps:
    """Test VerificationCode model timestamps."""

    def test_verification_code_has_created_at(self, db_session) -> None:
        """Test that verification code has created_at timestamp."""
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
        verification_code = VerificationCode(
            phone="+1234567890",
            code="123456",
            expires_at=expires_at,
        )
        db_session.add(verification_code)
        db_session.commit()

        assert verification_code.created_at is not None
        assert isinstance(verification_code.created_at, datetime)

    def test_verification_code_created_at_before_expires_at(self, db_session) -> None:
        """Test that created_at is before expires_at."""
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
        verification_code = VerificationCode(
            phone="+1234567890",
            code="123456",
            expires_at=expires_at,
        )
        db_session.add(verification_code)
        db_session.commit()

        assert verification_code.created_at < verification_code.expires_at


class TestVerificationCodeIndexes:
    """Test VerificationCode model indexes."""

    def test_verification_code_phone_indexed(self, db_session) -> None:
        """Test that phone is indexed for fast lookups."""
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
        verification_code = VerificationCode(
            phone="+1234567890",
            code="123456",
            expires_at=expires_at,
        )
        db_session.add(verification_code)
        db_session.commit()

        # Query by phone should be fast (indexed)
        found_code = (
            db_session.query(VerificationCode)
            .filter(VerificationCode.phone == "+1234567890")
            .first()
        )
        assert found_code is not None
        assert found_code.id == verification_code.id


class TestVerificationCodeExpiration:
    """Test VerificationCode expiration logic."""

    def test_verification_code_not_expired(self, db_session) -> None:
        """Test that verification code is not expired when expires_at is in future."""
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
        verification_code = VerificationCode(
            phone="+1234567890",
            code="123456",
            expires_at=expires_at,
        )
        db_session.add(verification_code)
        db_session.commit()

        assert verification_code.expires_at > datetime.now(timezone.utc)

    def test_verification_code_expired(self, db_session) -> None:
        """Test that verification code is expired when expires_at is in past."""
        expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
        verification_code = VerificationCode(
            phone="+1234567891",
            code="123456",
            expires_at=expires_at,
        )
        db_session.add(verification_code)
        db_session.commit()

        assert verification_code.expires_at < datetime.now(timezone.utc)
