"""Unit tests for Store repository."""
import uuid

import pytest

from app.core.models.organization import Organization
from app.core.models.store import Store, StoreStatus
from app.core.repositories.exceptions import ResourceNotFoundError
from app.core.repositories.store_repository import StoreRepository
from app.core.schemas.store import StoreCreate, StoreUpdate


class TestStoreRepositoryCreate:
    """Test Store repository create operations."""

    def test_create_store(self, db_session) -> None:
        """Test creating a new store."""
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

        repo = StoreRepository(db_session)
        store_data = StoreCreate(
            organization_id=org.id,
            name="Test Store",
            street_address="456 Store Ave",
            city="New York",
            state="NY",
            postal_code="10002",
            country="US",
        )
        result = repo.create(store_data)

        assert result.id is not None
        assert result.name == "Test Store"
        assert result.organization_id == org.id
        assert result.street_address == "456 Store Ave"
        assert result.city == "New York"
        assert result.state == "NY"
        assert result.postal_code == "10002"
        assert result.country == "US"
        assert result.status == StoreStatus.ACTIVE
        assert result.created_at is not None
        assert result.updated_at is not None

    def test_create_store_with_all_fields(self, db_session) -> None:
        """Test creating a store with all fields."""
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

        repo = StoreRepository(db_session)
        store_data = StoreCreate(
            organization_id=org.id,
            name="Full Store",
            street_address="321 Full Ave",
            city="Los Angeles",
            state="CA",
            postal_code="90002",
            country="US",
            status=StoreStatus.ACTIVE,
        )
        result = repo.create(store_data)

        assert result.status == StoreStatus.ACTIVE

    def test_create_store_persists_to_database(self, db_session) -> None:
        """Test that created store is persisted to database."""
        org = Organization(
            name="Persist Org",
            billing_address="555 Persist St",
            city="Chicago",
            state="IL",
            postal_code="60601",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        repo = StoreRepository(db_session)
        store_data = StoreCreate(
            organization_id=org.id,
            name="Persisted Store",
            street_address="666 Persist Ave",
            city="Chicago",
            state="IL",
            postal_code="60602",
            country="US",
        )
        result = repo.create(store_data)

        # Verify it exists in database
        db_store = db_session.query(Store).filter(Store.id == result.id).first()
        assert db_store is not None
        assert db_store.name == "Persisted Store"


class TestStoreRepositoryGet:
    """Test Store repository get operations."""

    def test_get_store_by_id(self, db_session) -> None:
        """Test getting a store by ID."""
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

        store = Store(
            organization_id=org.id,
            name="Get Test Store",
            street_address="222 Get Ave",
            city="Houston",
            state="TX",
            postal_code="77002",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        repo = StoreRepository(db_session)
        result = repo.get_by_id(store.id)

        assert result is not None
        assert result.id == store.id
        assert result.name == "Get Test Store"

    def test_get_store_by_id_not_found(self, db_session) -> None:
        """Test getting a store that doesn't exist."""
        repo = StoreRepository(db_session)
        fake_id = uuid.uuid4()
        result = repo.get_by_id(fake_id)

        assert result is None

    def test_get_store_by_id_string(self, db_session) -> None:
        """Test getting a store by ID as string."""
        org = Organization(
            name="String Org",
            billing_address="333 String St",
            city="Miami",
            state="FL",
            postal_code="33101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="String Store",
            street_address="444 String Ave",
            city="Miami",
            state="FL",
            postal_code="33102",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        repo = StoreRepository(db_session)
        result = repo.get_by_id(str(store.id))

        assert result is not None
        assert result.id == store.id


class TestStoreRepositoryList:
    """Test Store repository list operations."""

    def test_list_stores(self, db_session) -> None:
        """Test listing all stores."""
        org = Organization(
            name="List Org",
            billing_address="555 List St",
            city="Seattle",
            state="WA",
            postal_code="98101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store1 = Store(
            organization_id=org.id,
            name="List Store 1",
            street_address="666 List Ave",
            city="Seattle",
            state="WA",
            postal_code="98102",
            country="US",
        )
        store2 = Store(
            organization_id=org.id,
            name="List Store 2",
            street_address="777 List Dr",
            city="Seattle",
            state="WA",
            postal_code="98103",
            country="US",
        )
        db_session.add_all([store1, store2])
        db_session.commit()

        repo = StoreRepository(db_session)
        results = repo.list()

        assert len(results) >= 2
        names = [r.name for r in results]
        assert "List Store 1" in names
        assert "List Store 2" in names

    def test_list_stores_with_pagination(self, db_session) -> None:
        """Test listing stores with pagination."""
        org = Organization(
            name="Pagination Org",
            billing_address="888 Pagination St",
            city="Boston",
            state="MA",
            postal_code="02101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        for i in range(5):
            store = Store(
                organization_id=org.id,
                name=f"Pagination Store {i}",
                street_address=f"{i}00 Pagination Ave",
                city="Boston",
                state="MA",
                postal_code="02102",
                country="US",
            )
            db_session.add(store)
        db_session.commit()

        repo = StoreRepository(db_session)
        results = repo.list(skip=0, limit=2)

        assert len(results) == 2

        results_page2 = repo.list(skip=2, limit=2)
        assert len(results_page2) == 2

    def test_list_stores_by_organization(self, db_session) -> None:
        """Test listing stores for a specific organization."""
        org1 = Organization(
            name="Org 1",
            billing_address="999 Org1 St",
            city="Denver",
            state="CO",
            postal_code="80201",
            country="US",
        )
        org2 = Organization(
            name="Org 2",
            billing_address="000 Org2 St",
            city="Phoenix",
            state="AZ",
            postal_code="85001",
            country="US",
        )
        db_session.add_all([org1, org2])
        db_session.commit()

        store1 = Store(
            organization_id=org1.id,
            name="Org1 Store",
            street_address="111 Org1 Ave",
            city="Denver",
            state="CO",
            postal_code="80202",
            country="US",
        )
        store2 = Store(
            organization_id=org2.id,
            name="Org2 Store",
            street_address="222 Org2 Ave",
            city="Phoenix",
            state="AZ",
            postal_code="85002",
            country="US",
        )
        db_session.add_all([store1, store2])
        db_session.commit()

        repo = StoreRepository(db_session)
        org1_stores = repo.list_by_organization(org1.id)

        assert len(org1_stores) >= 1
        assert all(s.organization_id == org1.id for s in org1_stores)
        assert any(s.name == "Org1 Store" for s in org1_stores)


class TestStoreRepositoryUpdate:
    """Test Store repository update operations."""

    def test_update_store(self, db_session) -> None:
        """Test updating a store."""
        org = Organization(
            name="Update Org",
            billing_address="333 Update St",
            city="Atlanta",
            state="GA",
            postal_code="30301",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Update Test Store",
            street_address="444 Update Ave",
            city="Atlanta",
            state="GA",
            postal_code="30302",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        repo = StoreRepository(db_session)
        update_data = StoreUpdate(name="Updated Name")
        result = repo.update(store.id, update_data)

        assert result.name == "Updated Name"
        assert result.id == store.id

    def test_update_store_multiple_fields(self, db_session) -> None:
        """Test updating multiple fields of a store."""
        org = Organization(
            name="Multi Org",
            billing_address="555 Multi St",
            city="Detroit",
            state="MI",
            postal_code="48201",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Multi Update Store",
            street_address="666 Multi Ave",
            city="Detroit",
            state="MI",
            postal_code="48202",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        repo = StoreRepository(db_session)
        update_data = StoreUpdate(
            name="Multi Updated",
            city="Ann Arbor",
            status=StoreStatus.INACTIVE,
        )
        result = repo.update(store.id, update_data)

        assert result.name == "Multi Updated"
        assert result.city == "Ann Arbor"
        assert result.status == StoreStatus.INACTIVE
        # Unchanged fields should remain
        assert result.street_address == "666 Multi Ave"

    def test_update_store_not_found(self, db_session) -> None:
        """Test updating a store that doesn't exist."""
        repo = StoreRepository(db_session)
        fake_id = uuid.uuid4()
        update_data = StoreUpdate(name="Should Fail")

        with pytest.raises(ResourceNotFoundError):
            repo.update(fake_id, update_data)

    def test_update_store_persists_to_database(self, db_session) -> None:
        """Test that updated store is persisted to database."""
        org = Organization(
            name="Persist Org",
            billing_address="777 Persist St",
            city="Portland",
            state="OR",
            postal_code="97201",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Persist Update Store",
            street_address="888 Persist Ave",
            city="Portland",
            state="OR",
            postal_code="97202",
            country="US",
        )
        db_session.add(store)
        db_session.commit()

        repo = StoreRepository(db_session)
        update_data = StoreUpdate(state="WA")
        repo.update(store.id, update_data)

        # Verify update in database
        db_store = db_session.query(Store).filter(Store.id == store.id).first()
        assert db_store.state == "WA"


class TestStoreRepositoryDelete:
    """Test Store repository delete operations."""

    def test_delete_store(self, db_session) -> None:
        """Test deleting a store."""
        org = Organization(
            name="Delete Org",
            billing_address="999 Delete St",
            city="Las Vegas",
            state="NV",
            postal_code="89101",
            country="US",
        )
        db_session.add(org)
        db_session.commit()

        store = Store(
            organization_id=org.id,
            name="Delete Test Store",
            street_address="000 Delete Ave",
            city="Las Vegas",
            state="NV",
            postal_code="89102",
            country="US",
        )
        db_session.add(store)
        db_session.commit()
        store_id = store.id

        repo = StoreRepository(db_session)
        result = repo.delete(store_id)

        assert result is True

        # Verify deletion
        deleted_store = db_session.query(Store).filter(Store.id == store_id).first()
        assert deleted_store is None

    def test_delete_store_not_found(self, db_session) -> None:
        """Test deleting a store that doesn't exist."""
        repo = StoreRepository(db_session)
        fake_id = uuid.uuid4()
        result = repo.delete(fake_id)

        assert result is False
