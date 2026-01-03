"""Integration tests for store routes."""
import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.models.organization import Organization
from app.core.models.store import StoreStatus


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


# NOTE: Store-level invitation tests removed - invitations are now organization-level
# See test_organizations_routes.py for organization member invitation tests
