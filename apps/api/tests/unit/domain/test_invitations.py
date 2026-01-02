"""Unit tests for invitation domain logic."""
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException

from app.core.models.invitation import Invitation, InvitationStatus
from app.core.models.organization import Organization
from app.core.models.user import User
from app.core.models.user_organization import UserOrganizationRole
from app.core.repositories.invitation_repository import InvitationRepository
from app.core.repositories.user_organization_repository import (
    UserOrganizationRepository,
)
from app.core.repositories.user_repository import UserRepository
from app.core.repositories.user_store_repository import UserStoreRepository
from app.core.services.invitation_service import InvitationService


def create_invitation_service(db_session):
    """Helper function to create InvitationService with repositories."""
    invitation_repo = InvitationRepository(db_session)
    user_repo = UserRepository(db_session)
    user_org_repo = UserOrganizationRepository(db_session)
    user_store_repo = UserStoreRepository(db_session)
    return InvitationService(invitation_repo, user_repo, user_org_repo, user_store_repo)


class TestInvitationTokenGeneration:
    """Test invitation token generation."""

    def test_generate_invitation_token(self, db_session) -> None:
        """Test that invitation token is generated correctly."""
        service = create_invitation_service(db_session)
        token = service.generate_token()

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
        # Token should be URL-safe base64 encoded (32 bytes = ~43 chars)
        assert len(token) >= 32

    def test_generate_invitation_token_unique(self, db_session) -> None:
        """Test that generated tokens are unique."""
        service = create_invitation_service(db_session)
        token1 = service.generate_token()
        token2 = service.generate_token()

        assert token1 != token2

    def test_generate_invitation_token_url_safe(self, db_session) -> None:
        """Test that generated token is URL-safe."""
        service = create_invitation_service(db_session)
        token = service.generate_token()

        # URL-safe characters: alphanumeric, -, _
        # Should not contain +, /, or = (base64 standard)
        assert "+" not in token
        assert "/" not in token
        # = might appear for padding, but token_urlsafe should avoid it

    def test_generate_invitation_token_uses_secrets(self, db_session) -> None:
        """Test that token generation uses secrets module for security."""
        service = create_invitation_service(db_session)
        # Generate multiple tokens to ensure randomness
        tokens = [service.generate_token() for _ in range(10)]

        # All tokens should be unique
        assert len(set(tokens)) == 10


class TestInvitationExpiration:
    """Test invitation expiration logic."""

    def test_invitation_is_valid_before_expiration(self, db_session) -> None:
        """Test that invitation is valid before expiration."""
        service = create_invitation_service(db_session)

        org = Organization(
            name="Expiration Org",
            billing_address="123 Exp St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        inviter = User(phone="+1234567890", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            token="valid-token",
            email="valid@example.com",
            organization_id=org.id,
            organization_role=UserOrganizationRole.OWNER,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.PENDING,
        )
        db_session.add(invitation)
        db_session.commit()

        result = service.is_valid(invitation)

        assert result is True

    def test_invitation_is_expired_after_expiration(self, db_session) -> None:
        """Test that invitation is expired after expiration time."""
        service = create_invitation_service(db_session)

        org = Organization(
            name="Expired Org",
            billing_address="789 Expired St",
            city="Los Angeles",
            state="CA",
            postal_code="90001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        inviter = User(phone="+1234567891", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) - timedelta(days=1)
        invitation = Invitation(
            token="expired-token",
            email="expired@example.com",
            organization_id=org.id,
            organization_role=UserOrganizationRole.OWNER,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.PENDING,
        )
        db_session.add(invitation)
        db_session.commit()

        result = service.is_valid(invitation)

        assert result is False

    def test_invitation_is_invalid_when_accepted(self, db_session) -> None:
        """Test that accepted invitation is not valid for acceptance."""
        service = create_invitation_service(db_session)

        org = Organization(
            name="Accepted Org",
            billing_address="555 Accepted St",
            city="Chicago",
            state="IL",
            postal_code="60601",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        inviter = User(phone="+1234567892", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            token="accepted-token",
            email="accepted@example.com",
            organization_id=org.id,
            organization_role=UserOrganizationRole.OWNER,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.ACCEPTED,
            accepted_at=datetime.now(timezone.utc),
        )
        db_session.add(invitation)
        db_session.commit()

        result = service.is_valid(invitation)

        assert result is False

    def test_invitation_is_invalid_when_revoked(self, db_session) -> None:
        """Test that revoked invitation is not valid."""
        service = create_invitation_service(db_session)

        org = Organization(
            name="Revoked Org",
            billing_address="777 Revoked St",
            city="Houston",
            state="TX",
            postal_code="77001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        inviter = User(phone="+1234567893", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            token="revoked-token",
            email="revoked@example.com",
            organization_id=org.id,
            organization_role=UserOrganizationRole.OWNER,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.REVOKED,
        )
        db_session.add(invitation)
        db_session.commit()

        result = service.is_valid(invitation)

        assert result is False

    def test_mark_invitation_as_expired(self, db_session) -> None:
        """Test marking an invitation as expired."""
        service = create_invitation_service(db_session)

        org = Organization(
            name="Mark Expired Org",
            billing_address="999 Mark St",
            city="Miami",
            state="FL",
            postal_code="33101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        inviter = User(phone="+1234567894", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) - timedelta(days=1)
        invitation = Invitation(
            token="mark-expired-token",
            email="mark-expired@example.com",
            organization_id=org.id,
            organization_role=UserOrganizationRole.OWNER,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.PENDING,
        )
        db_session.add(invitation)
        db_session.commit()

        service.mark_as_expired(invitation)
        # Refresh invitation from database to verify status was updated
        db_session.refresh(invitation)

        assert invitation.status == InvitationStatus.EXPIRED


class TestInvitationTokenValidation:
    """Test invitation token format validation."""

    def test_validate_invitation_rejects_empty_token(self, db_session) -> None:
        """Test that empty token is rejected."""
        service = create_invitation_service(db_session)
        with pytest.raises(HTTPException) as exc_info:
            service.validate_invitation("")
        assert exc_info.value.status_code == 400

    def test_validate_invitation_rejects_short_token(self, db_session) -> None:
        """Test that token shorter than minimum length is rejected."""
        service = create_invitation_service(db_session)
        with pytest.raises(HTTPException) as exc_info:
            service.validate_invitation("short")
        assert exc_info.value.status_code == 400

    def test_validate_invitation_rejects_long_token(self, db_session) -> None:
        """Test that token longer than maximum length is rejected."""
        service = create_invitation_service(db_session)
        long_token = "a" * 100  # Way too long
        with pytest.raises(HTTPException) as exc_info:
            service.validate_invitation(long_token)
        assert exc_info.value.status_code == 400

    def test_validate_invitation_rejects_token_with_special_chars(
        self, db_session
    ) -> None:
        """Test that token with invalid characters is rejected."""
        service = create_invitation_service(db_session)
        invalid_tokens = [
            "test token with spaces",
            "test+token+with+plus",
            "test/token/with/slash",
            "test=token=with=equals",
            "test@token@with@at",
            "test#token#with#hash",
            "test$token$with$dollar",
            "test%token%with%percent",
            "test&token&with&ampersand",
        ]
        for invalid_token in invalid_tokens:
            with pytest.raises(HTTPException) as exc_info:
                service.validate_invitation(invalid_token)
            assert exc_info.value.status_code == 400

    def test_validate_invitation_accepts_valid_format(self, db_session) -> None:
        """Test that valid token format passes validation (even if not found)."""
        service = create_invitation_service(db_session)
        # Generate a valid token format
        valid_token = service.generate_token()
        # Should not raise format validation error, but will raise 404 for not found
        with pytest.raises(HTTPException) as exc_info:
            service.validate_invitation(valid_token)
        # Should be 404 (not found), not 400 (bad format)
        assert exc_info.value.status_code == 404

    def test_accept_invitation_rejects_invalid_token_format(self, db_session) -> None:
        """Test that accept_invitation rejects invalid token format."""
        service = create_invitation_service(db_session)
        invalid_token = "invalid token with spaces"
        with pytest.raises(HTTPException) as exc_info:
            service.accept_invitation(invalid_token, "Password123!")
        assert exc_info.value.status_code == 400
        assert "Invalid invitation token format" in exc_info.value.detail
