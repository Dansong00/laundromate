"""Unit tests for User-Organization association model."""
import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.models.organization import Organization
from app.core.models.user import User
from app.core.models.user_organization import UserOrganization, UserOrganizationRole


class TestUserOrganizationModelCreation:
    """Test UserOrganization model creation."""

    def test_user_organization_creation_with_required_fields(self, db_session) -> None:
        """Test that user-organization association can be created."""
        org = Organization(
            name="UserOrg Org",
            billing_address="123 UserOrg St",
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

        user_org = UserOrganization(
            user_id=user.id,
            organization_id=org.id,
        )
        db_session.add(user_org)
        db_session.commit()

        assert user_org.id is not None
        assert isinstance(user_org.id, uuid.UUID)
        assert user_org.user_id == user.id
        assert user_org.organization_id == org.id
        assert user_org.role == UserOrganizationRole.OWNER
        assert user_org.created_at is not None

    def test_user_organization_creation_with_all_fields(self, db_session) -> None:
        """Test that user-organization association can be created with all fields."""
        org = Organization(
            name="Full Org",
            billing_address="789 Full St",
            city="Los Angeles",
            state="CA",
            postal_code="90001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        user = User(phone="+1234567891")
        db_session.add(user)
        db_session.commit()

        user_org = UserOrganization(
            user_id=user.id,
            organization_id=org.id,
            role=UserOrganizationRole.EMPLOYEE,
        )
        db_session.add(user_org)
        db_session.commit()

        assert user_org.role == UserOrganizationRole.EMPLOYEE

    def test_user_organization_id_is_uuid(self, db_session) -> None:
        """Test that user-organization ID is a UUID."""
        org = Organization(
            name="UUID Org",
            billing_address="111 UUID St",
            city="Chicago",
            state="IL",
            postal_code="60601",
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
        )
        db_session.add(user_org)
        db_session.commit()

        assert isinstance(user_org.id, uuid.UUID)

    def test_user_organization_default_role(self, db_session) -> None:
        """Test that user-organization defaults to OWNER role."""
        org = Organization(
            name="Default Org",
            billing_address="333 Default St",
            city="Houston",
            state="TX",
            postal_code="77001",
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
        )
        db_session.add(user_org)
        db_session.commit()

        assert user_org.role == UserOrganizationRole.OWNER

    def test_user_organization_role_enum_values(self, db_session) -> None:
        """Test that user-organization can have different role values."""
        org = Organization(
            name="Role Org",
            billing_address="555 Role St",
            city="Miami",
            state="FL",
            postal_code="33101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        owner_user = User(phone="+1234567894")
        employee_user = User(phone="+1234567895")
        admin_user = User(phone="+1234567896")
        db_session.add_all([owner_user, employee_user, admin_user])
        db_session.commit()

        owner_assoc = UserOrganization(
            user_id=owner_user.id,
            organization_id=org.id,
            role=UserOrganizationRole.OWNER,
        )
        employee_assoc = UserOrganization(
            user_id=employee_user.id,
            organization_id=org.id,
            role=UserOrganizationRole.EMPLOYEE,
        )
        admin_assoc = UserOrganization(
            user_id=admin_user.id,
            organization_id=org.id,
            role=UserOrganizationRole.ADMIN,
        )
        db_session.add_all([owner_assoc, employee_assoc, admin_assoc])
        db_session.commit()

        assert owner_assoc.role == UserOrganizationRole.OWNER
        assert employee_assoc.role == UserOrganizationRole.EMPLOYEE
        assert admin_assoc.role == UserOrganizationRole.ADMIN

    def test_user_organization_unique_user_org_pair(self, db_session) -> None:
        """Test that user-organization pairs must be unique."""
        org = Organization(
            name="Unique Org",
            billing_address="777 Unique St",
            city="Seattle",
            state="WA",
            postal_code="98101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        user = User(phone="+1234567896")
        db_session.add(user)
        db_session.commit()

        user_org1 = UserOrganization(
            user_id=user.id,
            organization_id=org.id,
            role=UserOrganizationRole.OWNER,
        )
        user_org2 = UserOrganization(
            user_id=user.id,
            organization_id=org.id,  # Same user-org pair
            role=UserOrganizationRole.EMPLOYEE,
        )
        db_session.add(user_org1)
        db_session.commit()
        db_session.add(user_org2)
        with pytest.raises(IntegrityError):  # Unique constraint violation
            db_session.commit()

    def test_user_organization_same_user_different_organizations(
        self, db_session
    ) -> None:
        """Test that same user can be associated with different organizations."""
        org1 = Organization(
            name="Multi Org 1",
            billing_address="999 Multi St",
            city="Boston",
            state="MA",
            postal_code="02101",
            country="US",
        )
        org2 = Organization(
            name="Multi Org 2",
            billing_address="000 Multi Ave",
            city="Boston",
            state="MA",
            postal_code="02102",
            country="US",
        )
        db_session.add_all([org1, org2])
        db_session.commit()

        user = User(phone="+1234567897")
        db_session.add(user)
        db_session.commit()

        user_org1 = UserOrganization(
            user_id=user.id,
            organization_id=org1.id,
            role=UserOrganizationRole.OWNER,
        )
        user_org2 = UserOrganization(
            user_id=user.id,
            organization_id=org2.id,  # Different organization
            role=UserOrganizationRole.OWNER,
        )
        db_session.add_all([user_org1, user_org2])
        db_session.commit()

        assert user_org1.user_id == user_org2.user_id
        assert user_org1.organization_id != user_org2.organization_id


class TestUserOrganizationRelationships:
    """Test UserOrganization relationships."""

    def test_user_organization_belongs_to_user(self, db_session) -> None:
        """Test that user-organization association belongs to a user."""
        org = Organization(
            name="Rel Org",
            billing_address="222 Rel St",
            city="Denver",
            state="CO",
            postal_code="80201",
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
        )
        db_session.add(user_org)
        db_session.commit()

        assert user_org.user is not None
        assert user_org.user.id == user.id
        assert user_org.user.phone == "+1234567898"

    def test_user_organization_belongs_to_organization(self, db_session) -> None:
        """Test that user-organization association belongs to an organization."""
        org = Organization(
            name="Org Rel Org",
            billing_address="444 OrgRel St",
            city="Phoenix",
            state="AZ",
            postal_code="85001",
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
        )
        db_session.add(user_org)
        db_session.commit()

        assert user_org.organization is not None
        assert user_org.organization.id == org.id
        assert user_org.organization.name == "Org Rel Org"

    def test_user_organization_cascade_delete_on_user_delete(self, db_session) -> None:
        """Test that user-organization is deleted when user is deleted."""
        org = Organization(
            name="Cascade Org",
            billing_address="666 Cascade St",
            city="Atlanta",
            state="GA",
            postal_code="30301",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        user = User(phone="+1234567900")
        db_session.add(user)
        db_session.commit()

        user_org = UserOrganization(
            user_id=user.id,
            organization_id=org.id,
        )
        db_session.add(user_org)
        db_session.commit()

        user_org_id = user_org.id
        db_session.delete(user)
        db_session.commit()

        # Verify user-organization was deleted
        deleted_user_org = (
            db_session.query(UserOrganization)
            .filter(UserOrganization.id == user_org_id)
            .first()
        )
        assert deleted_user_org is None

    def test_user_organization_cascade_delete_on_organization_delete(
        self, db_session
    ) -> None:
        """Test that user-organization is deleted when organization is deleted."""
        org = Organization(
            name="Org Cascade Org",
            billing_address="888 OrgCascade St",
            city="Detroit",
            state="MI",
            postal_code="48201",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        user = User(phone="+1234567901")
        db_session.add(user)
        db_session.commit()

        user_org = UserOrganization(
            user_id=user.id,
            organization_id=org.id,
        )
        db_session.add(user_org)
        db_session.commit()

        user_org_id = user_org.id
        db_session.delete(org)
        db_session.commit()

        # Verify user-organization was deleted
        deleted_user_org = (
            db_session.query(UserOrganization)
            .filter(UserOrganization.id == user_org_id)
            .first()
        )
        assert deleted_user_org is None
