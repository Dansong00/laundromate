"""Unit tests for Organization repository."""
import uuid

import pytest

from app.core.models.organization import Organization, OrganizationStatus
from app.core.repositories.exceptions import ResourceNotFoundError
from app.core.repositories.organization_repository import OrganizationRepository
from app.core.schemas.organization import OrganizationCreate, OrganizationUpdate


class TestOrganizationRepositoryCreate:
    """Test Organization repository create operations."""

    def test_create_organization(self, db_session) -> None:
        """Test creating a new organization."""
        repo = OrganizationRepository(db_session)
        org_data = OrganizationCreate(
            name="Test Organization",
            billing_address="123 Main St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="US",
        )
        result = repo.create(org_data)

        assert result.id is not None
        assert result.name == "Test Organization"
        assert result.billing_address == "123 Main St"
        assert result.city == "New York"
        assert result.state == "NY"
        assert result.postal_code == "10001"
        assert result.country == "US"
        assert result.status == OrganizationStatus.ACTIVE
        assert result.created_at is not None
        assert result.updated_at is not None

    def test_create_organization_with_all_fields(self, db_session) -> None:
        """Test creating an organization with all fields."""
        repo = OrganizationRepository(db_session)
        org_data = OrganizationCreate(
            name="Full Organization",
            billing_address="456 Oak Ave",
            city="Los Angeles",
            state="CA",
            postal_code="90001",
            country="US",
            contact_email="contact@example.com",
            contact_phone="+1-555-123-4567",
            status=OrganizationStatus.ACTIVE,
        )
        result = repo.create(org_data)

        assert result.contact_email == "contact@example.com"
        assert result.contact_phone == "+1-555-123-4567"
        assert result.status == OrganizationStatus.ACTIVE

    def test_create_organization_persists_to_database(self, db_session) -> None:
        """Test that created organization is persisted to database."""
        repo = OrganizationRepository(db_session)
        org_data = OrganizationCreate(
            name="Persisted Org",
            billing_address="789 Pine St",
            city="Chicago",
            state="IL",
            postal_code="60601",
            country="US",
        )
        result = repo.create(org_data)

        # Verify it exists in database
        db_org = (
            db_session.query(Organization).filter(Organization.id == result.id).first()
        )
        assert db_org is not None
        assert db_org.name == "Persisted Org"


class TestOrganizationRepositoryGet:
    """Test Organization repository get operations."""

    def test_get_organization_by_id(self, db_session) -> None:
        """Test getting an organization by ID."""
        # Create organization directly in DB
        org = Organization(
            name="Get Test Org",
            billing_address="111 Get St",
            city="Houston",
            state="TX",
            postal_code="77001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        repo = OrganizationRepository(db_session)
        result = repo.get_by_id(org.id)

        assert result is not None
        assert result.id == org.id
        assert result.name == "Get Test Org"

    def test_get_organization_by_id_not_found(self, db_session) -> None:
        """Test getting an organization that doesn't exist."""
        repo = OrganizationRepository(db_session)
        fake_id = uuid.uuid4()
        result = repo.get_by_id(fake_id)

        assert result is None

    def test_get_organization_by_id_string(self, db_session) -> None:
        """Test getting an organization by ID as string."""
        org = Organization(
            name="String ID Org",
            billing_address="222 String St",
            city="Miami",
            state="FL",
            postal_code="33101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        repo = OrganizationRepository(db_session)
        result = repo.get_by_id(str(org.id))

        assert result is not None
        assert result.id == org.id


class TestOrganizationRepositoryList:
    """Test Organization repository list operations."""

    def test_list_organizations(self, db_session) -> None:
        """Test listing all organizations."""
        # Create multiple organizations
        org1 = Organization(
            name="List Org 1",
            billing_address="333 List St",
            city="Seattle",
            state="WA",
            postal_code="98101",
            country="US",
        )
        org2 = Organization(
            name="List Org 2",
            billing_address="444 List Ave",
            city="Boston",
            state="MA",
            postal_code="02101",
            country="US",
        )
        org3 = Organization(
            name="List Org 3",
            billing_address="555 List Dr",
            city="Denver",
            state="CO",
            postal_code="80201",
            country="US",
        )
        db_session.add_all([org1, org2, org3])
        db_session.commit()

        repo = OrganizationRepository(db_session)
        results = repo.list()

        assert len(results) >= 3
        names = [r.name for r in results]
        assert "List Org 1" in names
        assert "List Org 2" in names
        assert "List Org 3" in names

    def test_list_organizations_with_pagination(self, db_session) -> None:
        """Test listing organizations with pagination."""
        # Create multiple organizations
        for i in range(5):
            org = Organization(
                name=f"Pagination Org {i}",
                billing_address=f"{i}00 Pagination St",
                city="Phoenix",
                state="AZ",
                postal_code="85001",
                country="US",
            )
            db_session.add(org)
        db_session.commit()

        repo = OrganizationRepository(db_session)
        results = repo.list(skip=0, limit=2)

        assert len(results) == 2

        results_page2 = repo.list(skip=2, limit=2)
        assert len(results_page2) == 2

    def test_list_organizations_filter_by_status(self, db_session) -> None:
        """Test listing organizations filtered by status."""
        active_org = Organization(
            name="Active Org",
            billing_address="666 Active St",
            city="Atlanta",
            state="GA",
            postal_code="30301",
            country="US",
            status=OrganizationStatus.ACTIVE,
        )
        inactive_org = Organization(
            name="Inactive Org",
            billing_address="777 Inactive St",
            city="Detroit",
            state="MI",
            postal_code="48201",
            country="US",
            status=OrganizationStatus.INACTIVE,
        )
        db_session.add_all([active_org, inactive_org])
        db_session.commit()

        repo = OrganizationRepository(db_session)
        active_results = repo.list(status="active")

        assert len(active_results) >= 1
        assert all(r.status == OrganizationStatus.ACTIVE for r in active_results)


class TestOrganizationRepositoryUpdate:
    """Test Organization repository update operations."""

    def test_update_organization(self, db_session) -> None:
        """Test updating an organization."""
        org = Organization(
            name="Update Test Org",
            billing_address="888 Update St",
            city="Portland",
            state="OR",
            postal_code="97201",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        repo = OrganizationRepository(db_session)
        update_data = OrganizationUpdate(name="Updated Name")
        result = repo.update(org.id, update_data)

        assert result.name == "Updated Name"
        assert result.id == org.id

    def test_update_organization_multiple_fields(self, db_session) -> None:
        """Test updating multiple fields of an organization."""
        org = Organization(
            name="Multi Update Org",
            billing_address="999 Multi St",
            city="Las Vegas",
            state="NV",
            postal_code="89101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        repo = OrganizationRepository(db_session)
        update_data = OrganizationUpdate(
            name="Multi Updated",
            city="Reno",
            contact_email="updated@example.com",
        )
        result = repo.update(org.id, update_data)

        assert result.name == "Multi Updated"
        assert result.city == "Reno"
        assert result.contact_email == "updated@example.com"
        # Unchanged fields should remain
        assert result.billing_address == "999 Multi St"

    def test_update_organization_not_found(self, db_session) -> None:
        """Test updating an organization that doesn't exist."""
        repo = OrganizationRepository(db_session)
        fake_id = uuid.uuid4()
        update_data = OrganizationUpdate(name="Should Fail")

        with pytest.raises(ResourceNotFoundError):
            repo.update(fake_id, update_data)

    def test_update_organization_persists_to_database(self, db_session) -> None:
        """Test that updated organization is persisted to database."""
        org = Organization(
            name="Persist Update Org",
            billing_address="000 Persist St",
            city="Minneapolis",
            state="MN",
            postal_code="55401",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        repo = OrganizationRepository(db_session)
        update_data = OrganizationUpdate(state="WI")
        repo.update(org.id, update_data)

        # Verify update in database
        db_org = (
            db_session.query(Organization).filter(Organization.id == org.id).first()
        )
        assert db_org.state == "WI"


class TestOrganizationRepositoryDelete:
    """Test Organization repository delete operations."""

    def test_delete_organization(self, db_session) -> None:
        """Test deleting an organization."""
        org = Organization(
            name="Delete Test Org",
            billing_address="111 Delete St",
            city="Milwaukee",
            state="WI",
            postal_code="53201",
            country="US",
        )
        db_session.add(org)
        db_session.commit()
        org_id = org.id

        repo = OrganizationRepository(db_session)
        result = repo.delete(org_id)

        assert result is True

        # Verify deletion
        deleted_org = (
            db_session.query(Organization).filter(Organization.id == org_id).first()
        )
        assert deleted_org is None

    def test_delete_organization_not_found(self, db_session) -> None:
        """Test deleting an organization that doesn't exist."""
        repo = OrganizationRepository(db_session)
        fake_id = uuid.uuid4()
        result = repo.delete(fake_id)

        assert result is False
