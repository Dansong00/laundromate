"""Integration tests for organization routes."""
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.models.organization import Organization, OrganizationStatus


class TestCreateOrganization:
    """Test POST /super-admin/organizations endpoint."""

    def test_create_organization_success(
        self, client: TestClient, super_admin_auth_headers: dict
    ) -> None:
        """Test successfully creating an organization."""
        payload = {
            "name": "Test Organization",
            "billing_address": "123 Main St",
            "city": "New York",
            "state": "NY",
            "postal_code": "10001",
            "country": "US",
        }
        response = client.post(
            "/super-admin/organizations", json=payload, headers=super_admin_auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Organization"
        assert data["billing_address"] == "123 Main St"
        assert data["city"] == "New York"
        assert data["state"] == "NY"
        assert data["postal_code"] == "10001"
        assert data["country"] == "US"
        assert data["status"] == OrganizationStatus.ACTIVE.value
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_organization_with_all_fields(
        self, client: TestClient, super_admin_auth_headers: dict
    ) -> None:
        """Test creating an organization with all fields."""
        payload = {
            "name": "Full Organization",
            "billing_address": "456 Oak Ave",
            "city": "Los Angeles",
            "state": "CA",
            "postal_code": "90001",
            "country": "US",
            "contact_email": "contact@example.com",
            "contact_phone": "+1-555-123-4567",
            "status": OrganizationStatus.ACTIVE.value,
        }
        response = client.post(
            "/super-admin/organizations", json=payload, headers=super_admin_auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["contact_email"] == "contact@example.com"
        assert data["contact_phone"] == "+1-555-123-4567"

    def test_create_organization_requires_authentication(
        self, client: TestClient
    ) -> None:
        """Test that creating an organization requires authentication."""
        payload = {
            "name": "Unauthorized Org",
            "billing_address": "789 Unauthorized St",
            "city": "Chicago",
            "state": "IL",
            "postal_code": "60601",
            "country": "US",
        }
        response = client.post("/super-admin/organizations", json=payload)

        assert response.status_code == 401

    def test_create_organization_requires_super_admin(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Test that creating an organization requires super admin role."""
        payload = {
            "name": "Regular User Org",
            "billing_address": "111 Regular St",
            "city": "Houston",
            "state": "TX",
            "postal_code": "77001",
            "country": "US",
        }
        response = client.post(
            "/super-admin/organizations", json=payload, headers=auth_headers
        )

        assert response.status_code == 403

    def test_create_organization_validation_error(
        self, client: TestClient, super_admin_auth_headers: dict
    ) -> None:
        """Test creating organization with invalid data returns validation error."""
        payload = {
            "name": "",  # Empty name
            "billing_address": "123 Main St",
            "city": "New York",
            "state": "NY",
            "postal_code": "10001",
            "country": "US",
        }
        response = client.post(
            "/super-admin/organizations", json=payload, headers=super_admin_auth_headers
        )

        assert response.status_code == 422


class TestListOrganizations:
    """Test GET /super-admin/organizations endpoint."""

    def test_list_organizations_success(
        self, client: TestClient, super_admin_auth_headers: dict, db_session: Session
    ) -> None:
        """Test successfully listing organizations."""
        # Create test organizations
        org1 = Organization(
            name="List Org 1",
            billing_address="111 List St",
            city="Seattle",
            state="WA",
            postal_code="98101",
            country="US",
        )
        org2 = Organization(
            name="List Org 2",
            billing_address="222 List Ave",
            city="Boston",
            state="MA",
            postal_code="02101",
            country="US",
        )
        db_session.add_all([org1, org2])
        db_session.commit()

        response = client.get(
            "/super-admin/organizations", headers=super_admin_auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2
        names = [org["name"] for org in data]
        assert "List Org 1" in names
        assert "List Org 2" in names

    def test_list_organizations_with_pagination(
        self, client: TestClient, super_admin_auth_headers: dict, db_session: Session
    ) -> None:
        """Test listing organizations with pagination."""
        # Create multiple organizations
        for i in range(5):
            org = Organization(
                name=f"Pagination Org {i}",
                billing_address=f"{i}00 Pagination St",
                city="Denver",
                state="CO",
                postal_code="80201",
                country="US",
            )
            db_session.add(org)
        db_session.commit()

        response = client.get(
            "/super-admin/organizations?skip=0&limit=2",
            headers=super_admin_auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_organizations_filter_by_status(
        self,
        client: TestClient,
        super_admin_auth_headers: dict,
        db_session: Session,
    ) -> None:
        """Test listing organizations filtered by status."""
        active_org = Organization(
            name="Active Org",
            billing_address="333 Active St",
            city="Phoenix",
            state="AZ",
            postal_code="85001",
            country="US",
            status=OrganizationStatus.ACTIVE,
        )
        inactive_org = Organization(
            name="Inactive Org",
            billing_address="444 Inactive St",
            city="Atlanta",
            state="GA",
            postal_code="30301",
            country="US",
            status=OrganizationStatus.INACTIVE,
        )
        db_session.add_all([active_org, inactive_org])
        db_session.commit()

        response = client.get(
            "/super-admin/organizations?status=active",
            headers=super_admin_auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert all(org["status"] == OrganizationStatus.ACTIVE.value for org in data)
        assert any(org["name"] == "Active Org" for org in data)

    def test_list_organizations_requires_authentication(
        self, client: TestClient
    ) -> None:
        """Test that listing organizations requires authentication."""
        response = client.get("/super-admin/organizations")

        assert response.status_code == 401

    def test_list_organizations_requires_super_admin(
        self, client: TestClient, auth_headers: dict
    ) -> None:
        """Test that listing organizations requires super admin role."""
        response = client.get("/super-admin/organizations", headers=auth_headers)

        assert response.status_code == 403
