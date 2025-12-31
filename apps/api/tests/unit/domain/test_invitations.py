"""Unit tests for invitation domain logic."""
from datetime import datetime, timedelta, timezone

from app.core.models.invitation import Invitation, InvitationStatus
from app.core.models.organization import Organization
from app.core.models.store import Store
from app.core.models.user import User


class TestInvitationTokenGeneration:
    """Test invitation token generation."""

    def test_generate_invitation_token(self) -> None:
        """Test that invitation token is generated correctly."""
        from app.auth.invitation import generate_invitation_token

        token = generate_invitation_token()

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
        # Token should be URL-safe base64 encoded (32 bytes = ~43 chars)
        assert len(token) >= 32

    def test_generate_invitation_token_unique(self) -> None:
        """Test that generated tokens are unique."""
        from app.auth.invitation import generate_invitation_token

        token1 = generate_invitation_token()
        token2 = generate_invitation_token()

        assert token1 != token2

    def test_generate_invitation_token_url_safe(self) -> None:
        """Test that generated token is URL-safe."""
        from app.auth.invitation import generate_invitation_token

        token = generate_invitation_token()

        # URL-safe characters: alphanumeric, -, _
        # Should not contain +, /, or = (base64 standard)
        assert "+" not in token
        assert "/" not in token
        # = might appear for padding, but token_urlsafe should avoid it

    def test_generate_invitation_token_uses_secrets(self) -> None:
        """Test that token generation uses secrets module for security."""
        from app.auth.invitation import generate_invitation_token

        # Generate multiple tokens to ensure randomness
        tokens = [generate_invitation_token() for _ in range(10)]

        # All tokens should be unique
        assert len(set(tokens)) == 10


class TestInvitationExpiration:
    """Test invitation expiration logic."""

    def test_invitation_is_valid_before_expiration(self, db_session) -> None:
        """Test that invitation is valid before expiration."""
        from app.auth.invitation import is_invitation_valid

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

        store = Store(
            organization_id=org.id,
            name="Expiration Store",
            street_address="456 Exp Ave",
            city="New York",
            state="NY",
            postal_code="10002",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        inviter = User(phone="+1234567890", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            token="valid-token",
            email="valid@example.com",
            store_id=store.id,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.PENDING,
        )
        db_session.add(invitation)
        db_session.commit()

        result = is_invitation_valid(invitation)

        assert result is True

    def test_invitation_is_expired_after_expiration(self, db_session) -> None:
        """Test that invitation is expired after expiration time."""
        from app.auth.invitation import is_invitation_valid

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

        store = Store(
            organization_id=org.id,
            name="Expired Store",
            street_address="321 Expired Ave",
            city="Los Angeles",
            state="CA",
            postal_code="90002",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        inviter = User(phone="+1234567891", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) - timedelta(days=1)
        invitation = Invitation(
            token="expired-token",
            email="expired@example.com",
            store_id=store.id,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.PENDING,
        )
        db_session.add(invitation)
        db_session.commit()

        result = is_invitation_valid(invitation)

        assert result is False

    def test_invitation_is_invalid_when_accepted(self, db_session) -> None:
        """Test that accepted invitation is not valid for acceptance."""
        from app.auth.invitation import is_invitation_valid

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

        store = Store(
            organization_id=org.id,
            name="Accepted Store",
            street_address="666 Accepted Ave",
            city="Chicago",
            state="IL",
            postal_code="60602",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        inviter = User(phone="+1234567892", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            token="accepted-token",
            email="accepted@example.com",
            store_id=store.id,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.ACCEPTED,
            accepted_at=datetime.now(timezone.utc),
        )
        db_session.add(invitation)
        db_session.commit()

        result = is_invitation_valid(invitation)

        assert result is False

    def test_invitation_is_invalid_when_revoked(self, db_session) -> None:
        """Test that revoked invitation is not valid."""
        from app.auth.invitation import is_invitation_valid

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

        store = Store(
            organization_id=org.id,
            name="Revoked Store",
            street_address="888 Revoked Ave",
            city="Houston",
            state="TX",
            postal_code="77002",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        inviter = User(phone="+1234567893", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            token="revoked-token",
            email="revoked@example.com",
            store_id=store.id,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.REVOKED,
        )
        db_session.add(invitation)
        db_session.commit()

        result = is_invitation_valid(invitation)

        assert result is False

    def test_mark_invitation_as_expired(self, db_session) -> None:
        """Test marking an invitation as expired."""
        from app.auth.invitation import mark_invitation_as_expired

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

        store = Store(
            organization_id=org.id,
            name="Mark Expired Store",
            street_address="000 Mark Ave",
            city="Miami",
            state="FL",
            postal_code="33102",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        inviter = User(phone="+1234567894", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) - timedelta(days=1)
        invitation = Invitation(
            token="mark-expired-token",
            email="mark-expired@example.com",
            store_id=store.id,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.PENDING,
        )
        db_session.add(invitation)
        db_session.commit()

        mark_invitation_as_expired(invitation, db_session)
        db_session.refresh(invitation)

        assert invitation.status == InvitationStatus.EXPIRED
