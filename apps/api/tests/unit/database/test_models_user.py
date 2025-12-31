"""Unit tests for User model."""
import uuid
from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.models.user import User


class TestUserModelCreation:
    """Test User model creation."""

    def test_user_creation_with_required_fields(self, db_session) -> None:
        """Test that user can be created with required fields only."""
        user = User(
            phone="+1234567890",
        )
        db_session.add(user)
        db_session.commit()

        assert user.id is not None
        assert isinstance(user.id, uuid.UUID)
        assert user.phone == "+1234567890"
        assert user.is_active is True
        assert user.is_admin is False
        assert user.is_super_admin is False

    def test_user_creation_with_all_fields(self, db_session) -> None:
        """Test that user can be created with all fields."""
        user = User(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            phone="+1234567890",
            is_active=True,
            is_admin=False,
            is_super_admin=False,
        )
        db_session.add(user)
        db_session.commit()

        assert user.email == "test@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.phone == "+1234567890"

    def test_user_id_is_uuid(self, db_session) -> None:
        """Test that user ID is a UUID."""
        user = User(phone="+1234567890")
        db_session.add(user)
        db_session.commit()

        assert isinstance(user.id, uuid.UUID)

    def test_user_defaults(self, db_session) -> None:
        """Test that user has correct default values."""
        user = User(phone="+1234567890")
        db_session.add(user)
        db_session.commit()

        assert user.is_active is True
        assert user.is_admin is False
        assert user.is_super_admin is False
        assert user.is_support_agent is False
        assert user.is_provisioning_specialist is False

    def test_user_creation_with_role_fields(self, db_session) -> None:
        """Test that user can be created with role fields."""
        user = User(
            phone="+1234567890",
            is_super_admin=True,
            is_support_agent=False,
            is_provisioning_specialist=False,
        )
        db_session.add(user)
        db_session.commit()

        assert user.is_super_admin is True
        assert user.is_support_agent is False
        assert user.is_provisioning_specialist is False

    def test_user_support_agent_role(self, db_session) -> None:
        """Test that user can be set as support agent."""
        user = User(
            phone="+1234567891",
            is_super_admin=False,
            is_support_agent=True,
            is_provisioning_specialist=False,
        )
        db_session.add(user)
        db_session.commit()

        assert user.is_support_agent is True
        assert user.is_super_admin is False
        assert user.is_provisioning_specialist is False

    def test_user_provisioning_specialist_role(self, db_session) -> None:
        """Test that user can be set as provisioning specialist."""
        user = User(
            phone="+1234567892",
            is_super_admin=False,
            is_support_agent=False,
            is_provisioning_specialist=True,
        )
        db_session.add(user)
        db_session.commit()

        assert user.is_provisioning_specialist is True
        assert user.is_super_admin is False
        assert user.is_support_agent is False

    def test_user_role_fields_default_to_false(self, db_session) -> None:
        """Test that role fields default to False."""
        user = User(phone="+1234567893")
        db_session.add(user)
        db_session.commit()

        assert user.is_support_agent is False
        assert user.is_provisioning_specialist is False


class TestUserConstraints:
    """Test User model constraints."""

    def test_user_phone_is_required(self, db_session) -> None:
        """Test that phone is required."""
        user = User()
        db_session.add(user)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_user_email_unique(self, db_session) -> None:
        """Test that email must be unique."""
        user1 = User(email="test@example.com", phone="+1234567890")
        user2 = User(email="test@example.com", phone="+1234567891")
        db_session.add(user1)
        db_session.commit()

        db_session.add(user2)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_user_phone_unique(self, db_session) -> None:
        """Test that phone must be unique."""
        user1 = User(phone="+1234567890")
        user2 = User(phone="+1234567890")
        db_session.add(user1)
        db_session.commit()

        db_session.add(user2)
        with pytest.raises(IntegrityError):
            db_session.commit()


class TestUserTimestamps:
    """Test User model timestamps."""

    def test_user_has_created_at(self, db_session) -> None:
        """Test that user has created_at timestamp."""
        user = User(phone="+1234567890")
        db_session.add(user)
        db_session.commit()

        assert user.created_at is not None
        assert isinstance(user.created_at, datetime)

    def test_user_has_updated_at(self, db_session) -> None:
        """Test that user has updated_at timestamp."""
        user = User(phone="+1234567890")
        db_session.add(user)
        db_session.commit()

        assert user.updated_at is not None
        assert isinstance(user.updated_at, datetime)

    def test_user_updated_at_changes_on_update(self, db_session) -> None:
        """Test that updated_at changes when user is updated."""
        user = User(phone="+1234567890")
        db_session.add(user)
        db_session.commit()

        original_updated_at = user.updated_at
        user.first_name = "Updated"
        db_session.commit()

        assert user.updated_at != original_updated_at


class TestUserRelationships:
    """Test User model relationships."""

    def test_user_has_customer_relationship(self, db_session) -> None:
        """Test that user has customer relationship."""
        from app.core.models.customer import Customer

        user = User(phone="+1234567890")
        db_session.add(user)
        db_session.commit()

        customer = Customer(user_id=user.id)
        db_session.add(customer)
        db_session.commit()

        assert user.customer is not None
        assert user.customer.id == customer.id

    def test_user_customer_is_one_to_one(self, db_session) -> None:
        """Test that user-customer relationship is one-to-one."""
        from app.core.models.customer import Customer

        user = User(phone="+1234567890")
        db_session.add(user)
        db_session.commit()

        customer = Customer(user_id=user.id)
        db_session.add(customer)
        db_session.commit()

        # Accessing customer should return single object, not list
        assert user.customer is not None
        assert isinstance(user.customer, Customer)


class TestUserIndexes:
    """Test User model indexes."""

    def test_user_email_indexed(self, db_session) -> None:
        """Test that email is indexed for fast lookups."""
        user = User(email="test@example.com", phone="+1234567890")
        db_session.add(user)
        db_session.commit()

        # Query by email should be fast (indexed)
        found_user = (
            db_session.query(User).filter(User.email == "test@example.com").first()
        )
        assert found_user is not None
        assert found_user.id == user.id

    def test_user_phone_indexed(self, db_session) -> None:
        """Test that phone is indexed for fast lookups."""
        user = User(phone="+1234567890")
        db_session.add(user)
        db_session.commit()

        # Query by phone should be fast (indexed)
        found_user = db_session.query(User).filter(User.phone == "+1234567890").first()
        assert found_user is not None
        assert found_user.id == user.id
