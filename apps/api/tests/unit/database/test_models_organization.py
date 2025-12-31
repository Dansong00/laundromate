"""Unit tests for Organization model."""
import uuid
from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.models.organization import Organization, OrganizationStatus


class TestOrganizationModelCreation:
    """Test Organization model creation."""

    def test_organization_creation_with_required_fields(self, db_session) -> None:
        """Test that organization can be created with required fields only."""
        org = Organization(
            name="Test Organization",
            billing_address="123 Main St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        assert org.id is not None
        assert isinstance(org.id, uuid.UUID)
        assert org.name == "Test Organization"
        assert org.status == OrganizationStatus.ACTIVE
        assert org.created_at is not None
        assert org.updated_at is not None

    def test_organization_creation_with_all_fields(self, db_session) -> None:
        """Test that organization can be created with all fields."""
        org = Organization(
            name="Full Org",
            billing_address="456 Oak Ave",
            city="Los Angeles",
            state="CA",
            postal_code="90001",
            country="US",
            contact_email="contact@example.com",
            contact_phone="+1-555-123-4567",
            status=OrganizationStatus.ACTIVE,
        )
        db_session.add(org)
        db_session.commit()

        assert org.contact_email == "contact@example.com"
        assert org.contact_phone == "+1-555-123-4567"
        assert org.status == OrganizationStatus.ACTIVE

    def test_organization_id_is_uuid(self, db_session) -> None:
        """Test that organization ID is a UUID."""
        org = Organization(
            name="UUID Test",
            billing_address="789 Pine St",
            city="Chicago",
            state="IL",
            postal_code="60601",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        assert isinstance(org.id, uuid.UUID)

    def test_organization_default_status(self, db_session) -> None:
        """Test that organization defaults to ACTIVE status."""
        org = Organization(
            name="Default Status",
            billing_address="321 Elm St",
            city="Houston",
            state="TX",
            postal_code="77001",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        assert org.status == OrganizationStatus.ACTIVE

    def test_organization_status_enum_values(self, db_session) -> None:
        """Test that organization can have different status values."""
        org1 = Organization(
            name="Active Org",
            billing_address="111 First St",
            city="Miami",
            state="FL",
            postal_code="33101",
            country="US",
            status=OrganizationStatus.ACTIVE,
        )
        org2 = Organization(
            name="Inactive Org",
            billing_address="222 Second St",
            city="Seattle",
            state="WA",
            postal_code="98101",
            country="US",
            status=OrganizationStatus.INACTIVE,
        )
        org3 = Organization(
            name="Suspended Org",
            billing_address="333 Third St",
            city="Boston",
            state="MA",
            postal_code="02101",
            country="US",
            status=OrganizationStatus.SUSPENDED,
        )
        db_session.add_all([org1, org2, org3])
        db_session.commit()

        assert org1.status == OrganizationStatus.ACTIVE
        assert org2.status == OrganizationStatus.INACTIVE
        assert org3.status == OrganizationStatus.SUSPENDED

    def test_organization_timestamps(self, db_session) -> None:
        """Test that organization has created_at and updated_at timestamps."""
        org = Organization(
            name="Timestamp Test",
            billing_address="444 Fourth St",
            city="Denver",
            state="CO",
            postal_code="80201",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        assert org.created_at is not None
        assert isinstance(org.created_at, datetime)
        assert org.updated_at is not None
        assert isinstance(org.updated_at, datetime)

    def test_organization_name_required(self, db_session) -> None:
        """Test that organization name is required."""
        org = Organization(
            billing_address="555 Fifth St",
            city="Phoenix",
            state="AZ",
            postal_code="85001",
            country="US",
        )
        db_session.add(org)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_organization_country_code_format(self, db_session) -> None:
        """Test that country code is stored as ISO 3166-1 alpha-2 format."""
        org = Organization(
            name="Country Test",
            billing_address="666 Sixth St",
            city="Atlanta",
            state="GA",
            postal_code="30301",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        assert len(org.country) == 2
        assert org.country == "US"


class TestOrganizationRelationships:
    """Test Organization relationships."""

    def test_organization_has_stores_relationship(self, db_session) -> None:
        """Test that organization can have multiple stores."""
        from app.core.models.store import Store, StoreStatus

        org = Organization(
            name="Multi-Store Org",
            billing_address="777 Seventh St",
            city="Detroit",
            state="MI",
            postal_code="48201",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store1 = Store(
            organization_id=org.id,
            name="Store 1",
            street_address="100 Store St",
            city="Detroit",
            state="MI",
            postal_code="48201",
            country="US",
            status=StoreStatus.ACTIVE,
        )
        store2 = Store(
            organization_id=org.id,
            name="Store 2",
            street_address="200 Store Ave",
            city="Detroit",
            state="MI",
            postal_code="48202",
            country="US",
            status=StoreStatus.ACTIVE,
        )
        db_session.add_all([store1, store2])
        db_session.commit()

        assert len(org.stores) == 2
        assert store1 in org.stores
        assert store2 in org.stores

    def test_organization_cascade_delete_stores(self, db_session) -> None:
        """Test that deleting organization cascades to stores."""
        from app.core.models.store import Store, StoreStatus

        org = Organization(
            name="Cascade Test",
            billing_address="888 Eighth St",
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
            street_address="300 Cascade Ave",
            city="Portland",
            state="OR",
            postal_code="97201",
            country="US",
            status=StoreStatus.ACTIVE,
        )
        db_session.add(store)
        db_session.commit()

        store_id = store.id
        db_session.delete(org)
        db_session.commit()

        # Verify store was deleted
        deleted_store = db_session.query(Store).filter(Store.id == store_id).first()
        assert deleted_store is None
