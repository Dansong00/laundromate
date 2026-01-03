"""Unit tests for UserOrganization repository."""
import uuid

import pytest

from app.core.models.organization import Organization
from app.core.models.user import User
from app.core.models.user_organization import UserOrganization, UserOrganizationRole
from app.core.repositories.exceptions import ResourceNotFoundError
from app.core.repositories.user_organization_repository import (
    UserOrganizationRepository,
)
from app.core.schemas.user_organization import UserOrganizationCreate


class TestUserOrganizationRepositoryCreate:
    """Test UserOrganization repository create operations."""

    def test_create_user_organization(self, db_session) -> None:
        """Test creating a new user-organization association."""
        org = Organization(
            name="Create Org",
            billing_address="123 Create St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        user = User(phone="+1234567890")
        db_session.add(user)
        db_session.commit()

        repo = UserOrganizationRepository(db_session)
        user_org_data = UserOrganizationCreate(
            user_id=user.id,
            organization_id=org.id,
            role=UserOrganizationRole.OWNER,
        )
        result = repo.create(user_org_data)

        assert result.id is not None
        assert result.user_id == user.id
        assert result.organization_id == org.id
        assert result.role == UserOrganizationRole.OWNER
        assert result.created_at is not None

    def test_create_user_organization_persists_to_database(self, db_session) -> None:
        """Test that created user-organization is persisted to database."""
        org = Organization(
            name="Persisted Org",
            billing_address="789 Persist St",
            city="Chicago",
            state="IL",
            postal_code="60601",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        user = User(phone="+1234567891")
        db_session.add(user)
        db_session.commit()

        repo = UserOrganizationRepository(db_session)
        user_org_data = UserOrganizationCreate(
            user_id=user.id,
            organization_id=org.id,
            role=UserOrganizationRole.EMPLOYEE,
        )
        result = repo.create(user_org_data)

        # Verify it exists in database
        db_user_org = (
            db_session.query(UserOrganization)
            .filter(UserOrganization.id == result.id)
            .first()
        )
        assert db_user_org is not None
        assert db_user_org.role == UserOrganizationRole.EMPLOYEE


class TestUserOrganizationRepositoryGet:
    """Test UserOrganization repository get operations."""

    def test_get_user_organization_by_id(self, db_session) -> None:
        """Test getting a user-organization association by ID."""
        org = Organization(
            name="Get Org",
            billing_address="111 Get St",
            city="Houston",
            state="TX",
            postal_code="77001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        user = User(phone="+1234567892")
        db_session.add(user)
        db_session.commit()

        user_org = UserOrganization(
            user_id=user.id,
            organization_id=org.id,
            role=UserOrganizationRole.OWNER,
        )
        db_session.add(user_org)
        db_session.commit()

        repo = UserOrganizationRepository(db_session)
        result = repo.get_by_id(user_org.id)

        assert result is not None
        assert result.id == user_org.id
        assert result.user_id == user.id
        assert result.organization_id == org.id

    def test_get_user_organization_by_id_not_found(self, db_session) -> None:
        """Test getting a user-organization that doesn't exist."""
        repo = UserOrganizationRepository(db_session)
        fake_id = uuid.uuid4()
        result = repo.get_by_id(fake_id)

        assert result is None

    def test_find_by_user_and_organization(self, db_session) -> None:
        """Test finding user-organization by user ID and organization ID."""
        org = Organization(
            name="Find Org",
            billing_address="222 Find St",
            city="Miami",
            state="FL",
            postal_code="33101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        user = User(phone="+1234567893")
        db_session.add(user)
        db_session.commit()

        user_org = UserOrganization(
            user_id=user.id,
            organization_id=org.id,
            role=UserOrganizationRole.ADMIN,
        )
        db_session.add(user_org)
        db_session.commit()

        repo = UserOrganizationRepository(db_session)
        result = repo.find_by_user_and_organization(user.id, org.id)

        assert result is not None
        assert result.user_id == user.id
        assert result.organization_id == org.id
        assert result.role == UserOrganizationRole.ADMIN

    def test_find_by_user_and_organization_not_found(self, db_session) -> None:
        """Test finding user-organization that doesn't exist."""
        org = Organization(
            name="Not Found Org",
            billing_address="333 NotFound St",
            city="Seattle",
            state="WA",
            postal_code="98101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        user = User(phone="+1234567894")
        db_session.add(user)
        db_session.commit()

        repo = UserOrganizationRepository(db_session)
        result = repo.find_by_user_and_organization(user.id, org.id)

        assert result is None

    def test_get_model_by_user_and_organization(self, db_session) -> None:
        """Test getting user-organization model by user ID and organization ID."""
        org = Organization(
            name="Model Org",
            billing_address="444 Model St",
            city="Boston",
            state="MA",
            postal_code="02101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        user = User(phone="+1234567895")
        db_session.add(user)
        db_session.commit()

        user_org = UserOrganization(
            user_id=user.id,
            organization_id=org.id,
            role=UserOrganizationRole.OWNER,
        )
        db_session.add(user_org)
        db_session.commit()

        repo = UserOrganizationRepository(db_session)
        result = repo.get_model_by_user_and_organization(user.id, org.id)

        assert result is not None
        assert isinstance(result, UserOrganization)
        assert result.id == user_org.id
        assert result.user_id == user.id
        assert result.organization_id == org.id


class TestUserOrganizationRepositoryList:
    """Test UserOrganization repository list operations."""

    def test_list_user_organizations(self, db_session) -> None:
        """Test listing all user-organization associations."""
        org = Organization(
            name="List Org",
            billing_address="555 List St",
            city="Denver",
            state="CO",
            postal_code="80201",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        user1 = User(phone="+1234567896")
        user2 = User(phone="+1234567897")
        db_session.add_all([user1, user2])
        db_session.commit()

        user_org1 = UserOrganization(
            user_id=user1.id,
            organization_id=org.id,
            role=UserOrganizationRole.OWNER,
        )
        user_org2 = UserOrganization(
            user_id=user2.id,
            organization_id=org.id,
            role=UserOrganizationRole.EMPLOYEE,
        )
        db_session.add_all([user_org1, user_org2])
        db_session.commit()

        repo = UserOrganizationRepository(db_session)
        results = repo.list()

        assert len(results) >= 2
        user_ids = [r.user_id for r in results]
        assert user1.id in user_ids
        assert user2.id in user_ids


class TestUserOrganizationRepositoryUpdate:
    """Test UserOrganization repository update operations."""

    def test_update_user_organization(self, db_session) -> None:
        """Test updating a user-organization association."""
        org = Organization(
            name="Update Org",
            billing_address="666 Update St",
            city="Phoenix",
            state="AZ",
            postal_code="85001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        user = User(phone="+1234567898")
        db_session.add(user)
        db_session.commit()

        user_org = UserOrganization(
            user_id=user.id,
            organization_id=org.id,
            role=UserOrganizationRole.OWNER,
        )
        db_session.add(user_org)
        db_session.commit()

        repo = UserOrganizationRepository(db_session)
        update_data = UserOrganizationCreate(
            user_id=user.id,
            organization_id=org.id,
            role=UserOrganizationRole.ADMIN,
        )
        result = repo.update(user_org.id, update_data)

        assert result.role == UserOrganizationRole.ADMIN

    def test_update_user_organization_not_found(self, db_session) -> None:
        """Test updating a user-organization that doesn't exist."""
        repo = UserOrganizationRepository(db_session)
        fake_id = uuid.uuid4()
        update_data = UserOrganizationCreate(
            user_id=uuid.uuid4(),
            organization_id=uuid.uuid4(),
            role=UserOrganizationRole.OWNER,
        )

        with pytest.raises(ResourceNotFoundError):
            repo.update(fake_id, update_data)


class TestUserOrganizationRepositoryDelete:
    """Test UserOrganization repository delete operations."""

    def test_delete_user_organization(self, db_session) -> None:
        """Test deleting a user-organization association."""
        org = Organization(
            name="Delete Org",
            billing_address="777 Delete St",
            city="Atlanta",
            state="GA",
            postal_code="30301",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        user = User(phone="+1234567899")
        db_session.add(user)
        db_session.commit()

        user_org = UserOrganization(
            user_id=user.id,
            organization_id=org.id,
            role=UserOrganizationRole.OWNER,
        )
        db_session.add(user_org)
        db_session.commit()

        user_org_id = user_org.id
        repo = UserOrganizationRepository(db_session)
        deleted = repo.delete(user_org_id)

        assert deleted is True

        # Verify it's gone
        db_user_org = (
            db_session.query(UserOrganization)
            .filter(UserOrganization.id == user_org_id)
            .first()
        )
        assert db_user_org is None

    def test_delete_user_organization_not_found(self, db_session) -> None:
        """Test deleting a user-organization that doesn't exist."""
        repo = UserOrganizationRepository(db_session)
        fake_id = uuid.uuid4()
        deleted = repo.delete(fake_id)

        assert deleted is False
