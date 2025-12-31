"""Unit tests for User-Store association model."""
import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.models.organization import Organization
from app.core.models.store import Store
from app.core.models.user import User
from app.core.models.user_store import UserStore, UserStoreRole


class TestUserStoreModelCreation:
    """Test UserStore model creation."""

    def test_user_store_creation_with_required_fields(self, db_session) -> None:
        """Test that user-store association can be created with required fields."""
        org = Organization(
            name="UserStore Org",
            billing_address="123 UserStore St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="UserStore Store",
            street_address="456 UserStore Ave",
            city="New York",
            state="NY",
            postal_code="10002",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        user = User(phone="+1234567890")
        db_session.add(user)
        db_session.commit()

        user_store = UserStore(
            user_id=user.id,
            store_id=store.id,
        )
        db_session.add(user_store)
        db_session.commit()

        assert user_store.id is not None
        assert isinstance(user_store.id, uuid.UUID)
        assert user_store.user_id == user.id
        assert user_store.store_id == store.id
        assert user_store.role == UserStoreRole.OWNER
        assert user_store.created_at is not None

    def test_user_store_creation_with_all_fields(self, db_session) -> None:
        """Test that user-store association can be created with all fields."""
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

        store = Store(
            organization_id=org.id,
            name="Full Store",
            street_address="321 Full Ave",
            city="Los Angeles",
            state="CA",
            postal_code="90002",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        user = User(phone="+1234567891")
        db_session.add(user)
        db_session.commit()

        user_store = UserStore(
            user_id=user.id,
            store_id=store.id,
            role=UserStoreRole.OPERATOR,
        )
        db_session.add(user_store)
        db_session.commit()

        assert user_store.role == UserStoreRole.OPERATOR

    def test_user_store_id_is_uuid(self, db_session) -> None:
        """Test that user-store ID is a UUID."""
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

        store = Store(
            organization_id=org.id,
            name="UUID Store",
            street_address="222 UUID Ave",
            city="Chicago",
            state="IL",
            postal_code="60602",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        user = User(phone="+1234567892")
        db_session.add(user)
        db_session.commit()

        user_store = UserStore(
            user_id=user.id,
            store_id=store.id,
        )
        db_session.add(user_store)
        db_session.commit()

        assert isinstance(user_store.id, uuid.UUID)

    def test_user_store_default_role(self, db_session) -> None:
        """Test that user-store defaults to OWNER role."""
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

        store = Store(
            organization_id=org.id,
            name="Default Store",
            street_address="444 Default Ave",
            city="Houston",
            state="TX",
            postal_code="77002",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        user = User(phone="+1234567893")
        db_session.add(user)
        db_session.commit()

        user_store = UserStore(
            user_id=user.id,
            store_id=store.id,
        )
        db_session.add(user_store)
        db_session.commit()

        assert user_store.role == UserStoreRole.OWNER

    def test_user_store_role_enum_values(self, db_session) -> None:
        """Test that user-store can have different role values."""
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

        store = Store(
            organization_id=org.id,
            name="Role Store",
            street_address="666 Role Ave",
            city="Miami",
            state="FL",
            postal_code="33102",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        owner_user = User(phone="+1234567894")
        operator_user = User(phone="+1234567895")
        db_session.add_all([owner_user, operator_user])
        db_session.commit()

        owner_assoc = UserStore(
            user_id=owner_user.id,
            store_id=store.id,
            role=UserStoreRole.OWNER,
        )
        operator_assoc = UserStore(
            user_id=operator_user.id,
            store_id=store.id,
            role=UserStoreRole.OPERATOR,
        )
        db_session.add_all([owner_assoc, operator_assoc])
        db_session.commit()

        assert owner_assoc.role == UserStoreRole.OWNER
        assert operator_assoc.role == UserStoreRole.OPERATOR

    def test_user_store_unique_user_store_pair(self, db_session) -> None:
        """Test that user-store pairs must be unique."""
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

        store = Store(
            organization_id=org.id,
            name="Unique Store",
            street_address="888 Unique Ave",
            city="Seattle",
            state="WA",
            postal_code="98102",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        user = User(phone="+1234567896")
        db_session.add(user)
        db_session.commit()

        user_store1 = UserStore(
            user_id=user.id,
            store_id=store.id,
            role=UserStoreRole.OWNER,
        )
        user_store2 = UserStore(
            user_id=user.id,
            store_id=store.id,  # Same user-store pair
            role=UserStoreRole.OPERATOR,
        )
        db_session.add(user_store1)
        db_session.commit()
        db_session.add(user_store2)
        with pytest.raises(IntegrityError):  # Unique constraint violation
            db_session.commit()

    def test_user_store_same_user_different_stores(self, db_session) -> None:
        """Test that same user can be associated with different stores."""
        org = Organization(
            name="Multi Org",
            billing_address="999 Multi St",
            city="Boston",
            state="MA",
            postal_code="02101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store1 = Store(
            organization_id=org.id,
            name="Store 1",
            street_address="000 Store1 Ave",
            city="Boston",
            state="MA",
            postal_code="02102",
            country="US",
        )
        store2 = Store(
            organization_id=org.id,
            name="Store 2",
            street_address="111 Store2 Dr",
            city="Boston",
            state="MA",
            postal_code="02103",
            country="US",
        )
        db_session.add_all([store1, store2])
        db_session.commit()

        user = User(phone="+1234567897")
        db_session.add(user)
        db_session.commit()

        user_store1 = UserStore(
            user_id=user.id,
            store_id=store1.id,
            role=UserStoreRole.OWNER,
        )
        user_store2 = UserStore(
            user_id=user.id,
            store_id=store2.id,  # Different store
            role=UserStoreRole.OWNER,
        )
        db_session.add_all([user_store1, user_store2])
        db_session.commit()

        assert user_store1.user_id == user_store2.user_id
        assert user_store1.store_id != user_store2.store_id


class TestUserStoreRelationships:
    """Test UserStore relationships."""

    def test_user_store_belongs_to_user(self, db_session) -> None:
        """Test that user-store association belongs to a user."""
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

        store = Store(
            organization_id=org.id,
            name="Rel Store",
            street_address="333 Rel Ave",
            city="Denver",
            state="CO",
            postal_code="80202",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        user = User(phone="+1234567898")
        db_session.add(user)
        db_session.commit()

        user_store = UserStore(
            user_id=user.id,
            store_id=store.id,
        )
        db_session.add(user_store)
        db_session.commit()

        assert user_store.user is not None
        assert user_store.user.id == user.id
        assert user_store.user.phone == "+1234567898"

    def test_user_store_belongs_to_store(self, db_session) -> None:
        """Test that user-store association belongs to a store."""
        org = Organization(
            name="Store Rel Org",
            billing_address="444 StoreRel St",
            city="Phoenix",
            state="AZ",
            postal_code="85001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Store Rel Store",
            street_address="555 StoreRel Ave",
            city="Phoenix",
            state="AZ",
            postal_code="85002",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        user = User(phone="+1234567899")
        db_session.add(user)
        db_session.commit()

        user_store = UserStore(
            user_id=user.id,
            store_id=store.id,
        )
        db_session.add(user_store)
        db_session.commit()

        assert user_store.store is not None
        assert user_store.store.id == store.id
        assert user_store.store.name == "Store Rel Store"

    def test_user_store_cascade_delete_on_user_delete(self, db_session) -> None:
        """Test that user-store is deleted when user is deleted."""
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

        store = Store(
            organization_id=org.id,
            name="Cascade Store",
            street_address="777 Cascade Ave",
            city="Atlanta",
            state="GA",
            postal_code="30302",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        user = User(phone="+1234567900")
        db_session.add(user)
        db_session.commit()

        user_store = UserStore(
            user_id=user.id,
            store_id=store.id,
        )
        db_session.add(user_store)
        db_session.commit()

        user_store_id = user_store.id
        db_session.delete(user)
        db_session.commit()

        # Verify user-store was deleted
        deleted_user_store = (
            db_session.query(UserStore).filter(UserStore.id == user_store_id).first()
        )
        assert deleted_user_store is None

    def test_user_store_cascade_delete_on_store_delete(self, db_session) -> None:
        """Test that user-store is deleted when store is deleted."""
        org = Organization(
            name="Store Cascade Org",
            billing_address="888 StoreCascade St",
            city="Detroit",
            state="MI",
            postal_code="48201",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Store Cascade Store",
            street_address="999 StoreCascade Ave",
            city="Detroit",
            state="MI",
            postal_code="48202",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        user = User(phone="+1234567901")
        db_session.add(user)
        db_session.commit()

        user_store = UserStore(
            user_id=user.id,
            store_id=store.id,
        )
        db_session.add(user_store)
        db_session.commit()

        user_store_id = user_store.id
        db_session.delete(store)
        db_session.commit()

        # Verify user-store was deleted
        deleted_user_store = (
            db_session.query(UserStore).filter(UserStore.id == user_store_id).first()
        )
        assert deleted_user_store is None
