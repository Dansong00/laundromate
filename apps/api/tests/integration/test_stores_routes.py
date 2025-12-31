"""Integration tests for store routes."""
import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.models.invitation import Invitation, InvitationStatus
from app.core.models.organization import Organization
from app.core.models.store import Store, StoreStatus
from app.core.models.user import User


class TestCreateStore:
    """Test POST /super-admin/organizations/{id}/stores endpoint."""

    def test_create_store_success(
        self,
        client: TestClient,
        super_admin_auth_headers: dict,
        db_session: Session,
    ) -> None:
        """Test successfully creating a store."""
        org = Organization(
            name="Store Org",
            billing_address="123 Org St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        payload = {
            "name": "Test Store",
            "street_address": "456 Store Ave",
            "city": "New York",
            "state": "NY",
            "postal_code": "10002",
            "country": "US",
        }
        response = client.post(
            f"/super-admin/organizations/{org.id}/stores",
            json=payload,
            headers=super_admin_auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Store"
        assert data["organization_id"] == str(org.id)
        assert data["street_address"] == "456 Store Ave"
        assert data["city"] == "New York"
        assert data["state"] == "NY"
        assert data["postal_code"] == "10002"
        assert data["country"] == "US"
        assert data["status"] == StoreStatus.ACTIVE.value
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_store_organization_not_found(
        self, client: TestClient, super_admin_auth_headers: dict
    ) -> None:
        """Test creating a store for non-existent organization."""
        fake_org_id = uuid.uuid4()
        payload = {
            "name": "Orphan Store",
            "street_address": "789 Orphan Ave",
            "city": "Los Angeles",
            "state": "CA",
            "postal_code": "90001",
            "country": "US",
        }
        response = client.post(
            f"/super-admin/organizations/{fake_org_id}/stores",
            json=payload,
            headers=super_admin_auth_headers,
        )

        assert response.status_code == 404

    def test_create_store_requires_authentication(
        self, client: TestClient, db_session: Session
    ) -> None:
        """Test that creating a store requires authentication."""
        org = Organization(
            name="Auth Org",
            billing_address="111 Auth St",
            city="Chicago",
            state="IL",
            postal_code="60601",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        payload = {
            "name": "Unauthorized Store",
            "street_address": "222 Unauthorized Ave",
            "city": "Chicago",
            "state": "IL",
            "postal_code": "60602",
            "country": "US",
        }
        response = client.post(
            f"/super-admin/organizations/{org.id}/stores", json=payload
        )

        assert response.status_code == 401

    def test_create_store_requires_super_admin(
        self, client: TestClient, auth_headers: dict, db_session: Session
    ) -> None:
        """Test that creating a store requires super admin role."""
        org = Organization(
            name="Regular Org",
            billing_address="333 Regular St",
            city="Houston",
            state="TX",
            postal_code="77001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        payload = {
            "name": "Regular User Store",
            "street_address": "444 Regular Ave",
            "city": "Houston",
            "state": "TX",
            "postal_code": "77002",
            "country": "US",
        }
        response = client.post(
            f"/super-admin/organizations/{org.id}/stores",
            json=payload,
            headers=auth_headers,
        )

        assert response.status_code == 403


class TestInviteStoreOwner:
    """Test POST /super-admin/stores/{id}/invite-owner endpoint."""

    @patch("app.core.services.email_service.send_invitation_email")
    def test_invite_store_owner_success(
        self,
        mock_send_email: MagicMock,
        client: TestClient,
        super_admin_auth_headers: dict,
        super_admin_user: User,
        db_session: Session,
    ) -> None:
        """Test successfully inviting a store owner."""
        mock_send_email.return_value = True

        org = Organization(
            name="Invite Org",
            billing_address="555 Invite St",
            city="Miami",
            state="FL",
            postal_code="33101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Invite Store",
            street_address="666 Invite Ave",
            city="Miami",
            state="FL",
            postal_code="33102",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        payload = {"email": "owner@example.com"}
        response = client.post(
            f"/super-admin/stores/{store.id}/invite-owner",
            json=payload,
            headers=super_admin_auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "owner@example.com"
        assert data["store_id"] == str(store.id)
        assert data["status"] == InvitationStatus.PENDING.value
        assert "token" in data
        assert "expires_at" in data
        assert "created_at" in data

        # Verify email was sent
        mock_send_email.assert_called_once()
        call_args = mock_send_email.call_args
        assert call_args[1]["to_email"] == "owner@example.com"
        assert call_args[1]["store_name"] == "Invite Store"
        assert call_args[1]["organization_name"] == "Invite Org"

        # Verify invitation was created in database
        invitation = (
            db_session.query(Invitation)
            .filter(Invitation.email == "owner@example.com")
            .first()
        )
        assert invitation is not None
        assert invitation.store_id == store.id
        assert invitation.invited_by == super_admin_user.id

    def test_invite_store_owner_store_not_found(
        self, client: TestClient, super_admin_auth_headers: dict
    ) -> None:
        """Test inviting owner for non-existent store."""
        fake_store_id = uuid.uuid4()
        payload = {"email": "owner@example.com"}
        response = client.post(
            f"/super-admin/stores/{fake_store_id}/invite-owner",
            json=payload,
            headers=super_admin_auth_headers,
        )

        assert response.status_code == 404

    def test_invite_store_owner_duplicate_email(
        self,
        client: TestClient,
        super_admin_auth_headers: dict,
        super_admin_user: User,
        db_session: Session,
    ) -> None:
        """Test that inviting with duplicate email returns error."""
        org = Organization(
            name="Duplicate Org",
            billing_address="777 Duplicate St",
            city="Seattle",
            state="WA",
            postal_code="98101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Duplicate Store",
            street_address="888 Duplicate Ave",
            city="Seattle",
            state="WA",
            postal_code="98102",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        # Create existing invitation
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        existing_invitation = Invitation(
            token="existing-token",
            email="duplicate@example.com",
            store_id=store.id,
            invited_by=super_admin_user.id,
            expires_at=expires_at,
            status=InvitationStatus.PENDING,
        )
        db_session.add(existing_invitation)
        db_session.commit()

        payload = {"email": "duplicate@example.com"}
        response = client.post(
            f"/super-admin/stores/{store.id}/invite-owner",
            json=payload,
            headers=super_admin_auth_headers,
        )

        assert response.status_code == 400
        assert "already invited" in response.json()["detail"].lower()

    def test_invite_store_owner_requires_authentication(
        self, client: TestClient, db_session: Session
    ) -> None:
        """Test that inviting store owner requires authentication."""
        org = Organization(
            name="Auth Org",
            billing_address="999 Auth St",
            city="Boston",
            state="MA",
            postal_code="02101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Auth Store",
            street_address="000 Auth Ave",
            city="Boston",
            state="MA",
            postal_code="02102",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        payload = {"email": "owner@example.com"}
        response = client.post(
            f"/super-admin/stores/{store.id}/invite-owner", json=payload
        )

        assert response.status_code == 401

    def test_invite_store_owner_requires_super_admin(
        self, client: TestClient, auth_headers: dict, db_session: Session
    ) -> None:
        """Test that inviting store owner requires super admin role."""
        org = Organization(
            name="Regular Org",
            billing_address="111 Regular St",
            city="Denver",
            state="CO",
            postal_code="80201",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Regular Store",
            street_address="222 Regular Ave",
            city="Denver",
            state="CO",
            postal_code="80202",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        payload = {"email": "owner@example.com"}
        response = client.post(
            f"/super-admin/stores/{store.id}/invite-owner",
            json=payload,
            headers=auth_headers,
        )

        assert response.status_code == 403
