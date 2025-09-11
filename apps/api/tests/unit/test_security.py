"""
Unit tests for authentication security module.
"""

import pytest
from datetime import datetime, timedelta
from app.auth.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    decode_access_token
)
from app.core.models.user import User
from sqlalchemy.orm import Session
from jose import JWTError
from fastapi.security import HTTPAuthorizationCredentials


class TestPasswordSecurity:
    """Test password hashing and verification."""

    def test_password_hashing_consistency(self):
        """Test that password hashing produces consistent results."""
        password = "testpassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Hashes should be different due to salt
        assert hash1 != hash2
        assert len(hash1) > 0
        assert len(hash2) > 0

    def test_password_verification_success(self):
        """Test successful password verification."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True

    def test_password_verification_failure(self):
        """Test password verification with wrong password."""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong_password, hashed) is False

    def test_password_hash_salt_uniqueness(self):
        """Test that password hashes use unique salts."""
        password = "testpassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Hashes should be different due to unique salts
        assert hash1 != hash2
        
        # Both should verify correctly
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True

    def test_empty_password_handling(self):
        """Test handling of empty passwords."""
        empty_password = ""
        hashed = get_password_hash(empty_password)
        
        assert verify_password(empty_password, hashed) is True
        assert verify_password("not_empty", hashed) is False

    def test_very_long_password(self):
        """Test handling of very long passwords."""
        long_password = "a" * 1000
        hashed = get_password_hash(long_password)
        
        assert verify_password(long_password, hashed) is True
        assert verify_password("short", hashed) is False


class TestJWTTokenSecurity:
    """Test JWT token creation and validation."""

    def test_token_creation_with_user_id(self):
        """Test JWT token creation with user ID."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        token = create_access_token(subject=user_id)
        
        assert isinstance(token, str)
        assert len(token) > 0
        # JWT tokens have 3 parts separated by dots
        assert len(token.split('.')) == 3

    def test_token_creation_with_expiration(self):
        """Test JWT token creation with custom expiration."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        expires_minutes = 30
        token = create_access_token(subject=user_id, expires_minutes=expires_minutes)
        
        assert isinstance(token, str)
        assert len(token) > 0

    @pytest.mark.asyncio
    async def test_token_validation_success(self, db_session: Session):
        """Test successful token validation."""
        from app.core.models.user import User
        from app.auth.security import get_password_hash
        
        # Create test user
        user = User(
            email="test@example.com",
            hashed_password=get_password_hash("testpassword123"),
            first_name="Test",
            last_name="User",
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # Create token
        token = create_access_token(subject=str(user.id))
        
        # Create mock credentials
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        
        # Validate token
        current_user = await get_current_user(credentials, db_session)
        
        assert current_user is not None
        assert current_user.id == user.id
        assert current_user.email == user.email

    @pytest.mark.asyncio
    async def test_token_validation_invalid_token(self, db_session: Session):
        """Test token validation with invalid token."""
        invalid_token = "invalid.token.here"
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=invalid_token)
        
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(credentials, db_session)
        
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_token_validation_expired_token(self, db_session: Session):
        """Test token validation with expired token."""
        from app.core.models.user import User
        from app.auth.security import get_password_hash
        
        # Create test user
        user = User(
            email="test@example.com",
            hashed_password=get_password_hash("testpassword123"),
            first_name="Test",
            last_name="User",
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # Create expired token (expires in 1 second, then wait)
        token = create_access_token(subject=str(user.id), expires_minutes=0.0001)
        
        # Wait for token to expire
        import time
        time.sleep(0.1)
        
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(credentials, db_session)
        
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_token_validation_nonexistent_user(self, db_session: Session):
        """Test token validation with non-existent user ID."""
        nonexistent_user_id = "123e4567-e89b-12d3-a456-426614174000"
        token = create_access_token(subject=nonexistent_user_id)
        
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(credentials, db_session)
        
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_token_validation_inactive_user(self, db_session: Session):
        """Test token validation with inactive user."""
        from app.core.models.user import User
        from app.auth.security import get_password_hash
        
        # Create inactive user
        user = User(
            email="inactive@example.com",
            hashed_password=get_password_hash("testpassword123"),
            first_name="Inactive",
            last_name="User",
            is_active=False
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # Create token
        token = create_access_token(subject=str(user.id))
        
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        
        # Should still work - inactive check is done at decorator level
        current_user = await get_current_user(credentials, db_session)
        assert current_user.id == user.id
        assert current_user.is_active is False

    def test_token_payload_extraction(self):
        """Test that token contains correct payload."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        token = create_access_token(subject=user_id)
        
        # Decode token to check payload
        payload = decode_access_token(token)
        
        assert payload["sub"] == user_id
        assert "exp" in payload  # Expiration should be present

    def test_token_with_custom_expiration(self):
        """Test token creation with custom expiration."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        expires_minutes = 60
        token = create_access_token(subject=user_id, expires_minutes=expires_minutes)
        
        # Decode token to check expiration
        payload = decode_access_token(token)
        
        assert payload["sub"] == user_id
        assert "exp" in payload
        
        # Check that expiration is approximately correct
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        now = datetime.now()
        time_diff = exp_datetime - now
        
        # Should be approximately 60 minutes (allow some tolerance)
        assert 50 <= time_diff.total_seconds() / 60 <= 70


class TestSecurityIntegration:
    """Test security module integration scenarios."""

    @pytest.mark.asyncio
    async def test_full_auth_flow(self, db_session: Session):
        """Test complete authentication flow."""
        from app.core.models.user import User
        
        # Create user
        password = "testpassword123"
        user = User(
            email="integration@example.com",
            hashed_password=get_password_hash(password),
            first_name="Integration",
            last_name="Test",
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # Verify password
        assert verify_password(password, user.hashed_password) is True
        
        # Create token
        token = create_access_token(subject=str(user.id))
        
        # Validate token and get user
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        current_user = await get_current_user(credentials, db_session)
        
        assert current_user.id == user.id
        assert current_user.email == user.email

    def test_password_strength_variations(self):
        """Test password hashing with various password strengths."""
        passwords = [
            "123456",  # Weak
            "password",  # Common
            "P@ssw0rd!",  # Strong
            "MyVerySecurePassword123!@#",  # Very strong
            "a",  # Very short
            "a" * 100,  # Very long
        ]
        
        for password in passwords:
            hashed = get_password_hash(password)
            assert verify_password(password, hashed) is True
            assert verify_password(password + "x", hashed) is False

    def test_token_expiration_handling(self):
        """Test token expiration handling."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        
        # Create token with very short expiration
        token = create_access_token(subject=user_id, expires_minutes=0.0001)
        
        # Wait a bit to ensure expiration
        import time
        time.sleep(0.1)
        
        # Token should be expired
        with pytest.raises(JWTError):
            decode_access_token(token)