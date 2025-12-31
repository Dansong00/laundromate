"""Unit tests for Store model."""
import uuid
from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.models.organization import Organization
from app.core.models.store import Store, StoreStatus


class TestStoreModelCreation:
    """Test Store model creation."""

    def test_store_creation_with_required_fields(self, db_session) -> None:
        """Test that store can be created with required fields."""
        org = Organization(
            name="Parent Org",
            billing_address="123 Org St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Test Store",
            street_address="456 Store Ave",
            city="New York",
            state="NY",
            postal_code="10002",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        assert store.id is not None
        assert isinstance(store.id, uuid.UUID)
        assert store.name == "Test Store"
        assert store.organization_id == org.id
        assert store.status == StoreStatus.ACTIVE
        assert store.created_at is not None
        assert store.updated_at is not None

    def test_store_creation_with_all_fields(self, db_session) -> None:
        """Test that store can be created with all fields."""
        org = Organization(
            name="Full Org",
            billing_address="789 Org Blvd",
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
            street_address="321 Store Dr",
            city="Los Angeles",
            state="CA",
            postal_code="90002",
            country="US",
            status=StoreStatus.ACTIVE,
        )
        db_session.add(store)
        db_session.commit()

        assert store.status == StoreStatus.ACTIVE

    def test_store_id_is_uuid(self, db_session) -> None:
        """Test that store ID is a UUID."""
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

        assert isinstance(store.id, uuid.UUID)

    def test_store_default_status(self, db_session) -> None:
        """Test that store defaults to ACTIVE status."""
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

        assert store.status == StoreStatus.ACTIVE

    def test_store_status_enum_values(self, db_session) -> None:
        """Test that store can have different status values."""
        org = Organization(
            name="Status Org",
            billing_address="555 Status St",
            city="Miami",
            state="FL",
            postal_code="33101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        active_store = Store(
            organization_id=org.id,
            name="Active Store",
            street_address="666 Active Ave",
            city="Miami",
            state="FL",
            postal_code="33102",
            country="US",
            status=StoreStatus.ACTIVE,
        )
        inactive_store = Store(
            organization_id=org.id,
            name="Inactive Store",
            street_address="777 Inactive Dr",
            city="Miami",
            state="FL",
            postal_code="33103",
            country="US",
            status=StoreStatus.INACTIVE,
        )
        db_session.add_all([active_store, inactive_store])
        db_session.commit()

        assert active_store.status == StoreStatus.ACTIVE
        assert inactive_store.status == StoreStatus.INACTIVE

    def test_store_timestamps(self, db_session) -> None:
        """Test that store has created_at and updated_at timestamps."""
        org = Organization(
            name="Timestamp Org",
            billing_address="888 Timestamp St",
            city="Seattle",
            state="WA",
            postal_code="98101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Timestamp Store",
            street_address="999 Timestamp Ave",
            city="Seattle",
            state="WA",
            postal_code="98102",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        assert store.created_at is not None
        assert isinstance(store.created_at, datetime)
        assert store.updated_at is not None
        assert isinstance(store.updated_at, datetime)

    def test_store_name_required(self, db_session) -> None:
        """Test that store name is required."""
        org = Organization(
            name="Required Org",
            billing_address="000 Required St",
            city="Boston",
            state="MA",
            postal_code="02101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            street_address="111 Required Ave",
            city="Boston",
            state="MA",
            postal_code="02102",
            country="US",
        )
        db_session.add(store)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_store_organization_id_required(self, db_session) -> None:
        """Test that store organization_id is required."""
        store = Store(
            name="No Org Store",
            street_address="222 No Org Ave",
            city="Denver",
            state="CO",
            postal_code="80201",
            country="US",
        )
        db_session.add(store)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_store_unique_name_per_organization(self, db_session) -> None:
        """Test that store names must be unique within an organization."""
        org = Organization(
            name="Unique Org",
            billing_address="333 Unique St",
            city="Phoenix",
            state="AZ",
            postal_code="85001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store1 = Store(
            organization_id=org.id,
            name="Unique Store",
            street_address="444 Unique Ave",
            city="Phoenix",
            state="AZ",
            postal_code="85002",
            country="US",
        )
        store2 = Store(
            organization_id=org.id,
            name="Unique Store",  # Same name
            street_address="555 Unique Dr",
            city="Phoenix",
            state="AZ",
            postal_code="85003",
            country="US",
        )
        db_session.add(store1)
        db_session.commit()
        db_session.add(store2)
        with pytest.raises(IntegrityError):  # Unique constraint violation
            db_session.commit()

    def test_store_same_name_different_organizations(self, db_session) -> None:
        """Test that stores can have the same name in different organizations."""
        org1 = Organization(
            name="Org 1",
            billing_address="666 Org1 St",
            city="Atlanta",
            state="GA",
            postal_code="30301",
            country="US",
        )
        org2 = Organization(
            name="Org 2",
            billing_address="777 Org2 St",
            city="Atlanta",
            state="GA",
            postal_code="30302",
            country="US",
        )
        db_session.add_all([org1, org2])
        db_session.commit()

        store1 = Store(
            organization_id=org1.id,
            name="Same Name Store",
            street_address="888 Same Ave",
            city="Atlanta",
            state="GA",
            postal_code="30303",
            country="US",
        )
        store2 = Store(
            organization_id=org2.id,
            name="Same Name Store",  # Same name, different org
            street_address="999 Same Dr",
            city="Atlanta",
            state="GA",
            postal_code="30304",
            country="US",
        )
        db_session.add_all([store1, store2])
        db_session.commit()

        assert store1.name == store2.name
        assert store1.organization_id != store2.organization_id


class TestStoreRelationships:
    """Test Store relationships."""

    def test_store_belongs_to_organization(self, db_session) -> None:
        """Test that store belongs to an organization."""
        org = Organization(
            name="Relationship Org",
            billing_address="000 Rel St",
            city="Detroit",
            state="MI",
            postal_code="48201",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Relationship Store",
            street_address="111 Rel Ave",
            city="Detroit",
            state="MI",
            postal_code="48202",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        assert store.organization is not None
        assert store.organization.id == org.id
        assert store.organization.name == "Relationship Org"

    def test_store_cascade_delete_on_organization_delete(self, db_session) -> None:
        """Test that store is deleted when organization is deleted."""
        org = Organization(
            name="Cascade Org",
            billing_address="222 Cascade St",
            city="Portland",
            state="OR",
            postal_code="97201",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Cascade Store",
            street_address="333 Cascade Ave",
            city="Portland",
            state="OR",
            postal_code="97202",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        store_id = store.id
        db_session.delete(org)
        db_session.commit()

        # Verify store was deleted
        deleted_store = db_session.query(Store).filter(Store.id == store_id).first()
        assert deleted_store is None
