"""Unit tests for Invitation model."""
import uuid
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.models.invitation import Invitation, InvitationStatus
from app.core.models.organization import Organization
from app.core.models.store import Store
from app.core.models.user import User


class TestInvitationModelCreation:
    """Test Invitation model creation."""

    def test_invitation_creation_with_required_fields(self, db_session) -> None:
        """Test that invitation can be created with required fields."""
        org = Organization(
            name="Invitation Org",
            billing_address="123 Inv St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Invitation Store",
            street_address="456 Inv Ave",
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
            token="test-token-12345",
            email="owner@example.com",
            store_id=store.id,
            invited_by=inviter.id,
            expires_at=expires_at,
        )
        db_session.add(invitation)
        db_session.commit()

        assert invitation.id is not None
        assert isinstance(invitation.id, uuid.UUID)
        assert invitation.token == "test-token-12345"
        assert invitation.email == "owner@example.com"
        assert invitation.store_id == store.id
        assert invitation.invited_by == inviter.id
        assert invitation.status == InvitationStatus.PENDING
        assert invitation.expires_at == expires_at
        assert invitation.accepted_at is None
        assert invitation.created_at is not None

    def test_invitation_default_status(self, db_session) -> None:
        """Test that invitation defaults to PENDING status."""
        org = Organization(
            name="Default Org",
            billing_address="789 Default St",
            city="Los Angeles",
            state="CA",
            postal_code="90001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Default Store",
            street_address="321 Default Ave",
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

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            token="default-token",
            email="default@example.com",
            store_id=store.id,
            invited_by=inviter.id,
            expires_at=expires_at,
        )
        db_session.add(invitation)
        db_session.commit()

        assert invitation.status == InvitationStatus.PENDING

    def test_invitation_status_enum_values(self, db_session) -> None:
        """Test that invitation can have different status values."""
        org = Organization(
            name="Status Org",
            billing_address="111 Status St",
            city="Chicago",
            state="IL",
            postal_code="60601",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Status Store",
            street_address="222 Status Ave",
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
        pending = Invitation(
            token="pending-token",
            email="pending@example.com",
            store_id=store.id,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.PENDING,
        )
        accepted = Invitation(
            token="accepted-token",
            email="accepted@example.com",
            store_id=store.id,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.ACCEPTED,
            accepted_at=datetime.now(timezone.utc),
        )
        expired = Invitation(
            token="expired-token",
            email="expired@example.com",
            store_id=store.id,
            invited_by=inviter.id,
            expires_at=datetime.now(timezone.utc) - timedelta(days=1),
            status=InvitationStatus.EXPIRED,
        )
        revoked = Invitation(
            token="revoked-token",
            email="revoked@example.com",
            store_id=store.id,
            invited_by=inviter.id,
            expires_at=expires_at,
            status=InvitationStatus.REVOKED,
        )
        db_session.add_all([pending, accepted, expired, revoked])
        db_session.commit()

        assert pending.status == InvitationStatus.PENDING
        assert accepted.status == InvitationStatus.ACCEPTED
        assert expired.status == InvitationStatus.EXPIRED
        assert revoked.status == InvitationStatus.REVOKED

    def test_invitation_token_unique(self, db_session) -> None:
        """Test that invitation tokens must be unique."""
        org = Organization(
            name="Unique Org",
            billing_address="333 Unique St",
            city="Houston",
            state="TX",
            postal_code="77001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Unique Store",
            street_address="444 Unique Ave",
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
        invitation1 = Invitation(
            token="unique-token",
            email="user1@example.com",
            store_id=store.id,
            invited_by=inviter.id,
            expires_at=expires_at,
        )
        invitation2 = Invitation(
            token="unique-token",  # Same token
            email="user2@example.com",
            store_id=store.id,
            invited_by=inviter.id,
            expires_at=expires_at,
        )
        db_session.add(invitation1)
        db_session.commit()
        db_session.add(invitation2)
        with pytest.raises(IntegrityError):  # Unique constraint violation
            db_session.commit()

    def test_invitation_timestamps(self, db_session) -> None:
        """Test that invitation has created_at timestamp."""
        org = Organization(
            name="Timestamp Org",
            billing_address="555 Timestamp St",
            city="Miami",
            state="FL",
            postal_code="33101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Timestamp Store",
            street_address="666 Timestamp Ave",
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

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            token="timestamp-token",
            email="timestamp@example.com",
            store_id=store.id,
            invited_by=inviter.id,
            expires_at=expires_at,
        )
        db_session.add(invitation)
        db_session.commit()

        assert invitation.created_at is not None
        assert isinstance(invitation.created_at, datetime)

    def test_invitation_accepted_at_nullable(self, db_session) -> None:
        """Test that accepted_at can be null for pending invitations."""
        org = Organization(
            name="Accepted Org",
            billing_address="777 Accepted St",
            city="Seattle",
            state="WA",
            postal_code="98101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Accepted Store",
            street_address="888 Accepted Ave",
            city="Seattle",
            state="WA",
            postal_code="98102",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        inviter = User(phone="+1234567895", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            token="accepted-null-token",
            email="accepted-null@example.com",
            store_id=store.id,
            invited_by=inviter.id,
            expires_at=expires_at,
        )
        db_session.add(invitation)
        db_session.commit()

        assert invitation.accepted_at is None

        # Set accepted_at
        invitation.accepted_at = datetime.now(timezone.utc)
        invitation.status = InvitationStatus.ACCEPTED
        db_session.commit()

        assert invitation.accepted_at is not None
        assert isinstance(invitation.accepted_at, datetime)


class TestInvitationRelationships:
    """Test Invitation relationships."""

    def test_invitation_belongs_to_store(self, db_session) -> None:
        """Test that invitation belongs to a store."""
        org = Organization(
            name="Relationship Org",
            billing_address="999 Rel St",
            city="Boston",
            state="MA",
            postal_code="02101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Relationship Store",
            street_address="000 Rel Ave",
            city="Boston",
            state="MA",
            postal_code="02102",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        inviter = User(phone="+1234567896", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            token="relationship-token",
            email="relationship@example.com",
            store_id=store.id,
            invited_by=inviter.id,
            expires_at=expires_at,
        )
        db_session.add(invitation)
        db_session.commit()

        assert invitation.store is not None
        assert invitation.store.id == store.id
        assert invitation.store.name == "Relationship Store"

    def test_invitation_belongs_to_inviter(self, db_session) -> None:
        """Test that invitation belongs to the user who created it."""
        org = Organization(
            name="Inviter Org",
            billing_address="111 Inviter St",
            city="Denver",
            state="CO",
            postal_code="80201",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Inviter Store",
            street_address="222 Inviter Ave",
            city="Denver",
            state="CO",
            postal_code="80202",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        inviter = User(phone="+1234567897", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            token="inviter-token",
            email="inviter@example.com",
            store_id=store.id,
            invited_by=inviter.id,
            expires_at=expires_at,
        )
        db_session.add(invitation)
        db_session.commit()

        assert invitation.inviter is not None
        assert invitation.inviter.id == inviter.id
        assert invitation.inviter.phone == "+1234567897"

    def test_invitation_cascade_delete_on_store_delete(self, db_session) -> None:
        """Test that invitation is deleted when store is deleted."""
        org = Organization(
            name="Cascade Org",
            billing_address="333 Cascade St",
            city="Phoenix",
            state="AZ",
            postal_code="85001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Cascade Store",
            street_address="444 Cascade Ave",
            city="Phoenix",
            state="AZ",
            postal_code="85002",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        inviter = User(phone="+1234567898", is_super_admin=True)
        db_session.add(inviter)
        db_session.commit()

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        invitation = Invitation(
            token="cascade-token",
            email="cascade@example.com",
            store_id=store.id,
            invited_by=inviter.id,
            expires_at=expires_at,
        )
        db_session.add(invitation)
        db_session.commit()

        invitation_id = invitation.id
        db_session.delete(store)
        db_session.commit()

        # Verify invitation was deleted
        deleted_invitation = (
            db_session.query(Invitation).filter(Invitation.id == invitation_id).first()
        )
        assert deleted_invitation is None
