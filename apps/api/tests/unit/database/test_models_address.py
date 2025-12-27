"""Unit tests for Address model."""
import pytest
from sqlalchemy.exc import IntegrityError

from app.core.models.address import Address


class TestAddressModelCreation:
    """Test Address model creation."""

    def test_address_creation_with_required_fields(
        self, db_session, test_customer
    ) -> None:
        """Test that address can be created with required fields."""
        address = Address(
            customer_id=test_customer.id,
            address_line_1="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
            address_type="home",
        )
        db_session.add(address)
        db_session.commit()

        assert address.id is not None
        assert address.address_line_1 == "123 Main St"
        assert address.city == "New York"
        assert address.state == "NY"
        assert address.zip_code == "10001"
        assert address.address_type == "home"

    def test_address_creation_with_all_fields(self, db_session, test_customer) -> None:
        """Test that address can be created with all fields."""
        address = Address(
            customer_id=test_customer.id,
            address_line_1="123 Main St",
            address_line_2="Apt 4B",
            city="New York",
            state="NY",
            zip_code="10001",
            country="USA",
            address_type="home",
            is_default=True,
            is_active=True,
            instructions="Ring doorbell twice",
            latitude="40.7128",
            longitude="-74.0060",
        )
        db_session.add(address)
        db_session.commit()

        assert address.address_line_2 == "Apt 4B"
        assert address.country == "USA"
        assert address.is_default is True
        assert address.is_active is True
        assert address.instructions == "Ring doorbell twice"


class TestAddressConstraints:
    """Test Address model constraints."""

    def test_address_customer_id_is_required(self, db_session) -> None:
        """Test that customer_id is required."""
        address = Address(
            address_line_1="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
            address_type="home",
        )
        db_session.add(address)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_address_line_1_is_required(self, db_session, test_customer) -> None:
        """Test that address_line_1 is required."""
        address = Address(
            customer_id=test_customer.id,
            city="New York",
            state="NY",
            zip_code="10001",
            address_type="home",
        )
        db_session.add(address)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_city_is_required(self, db_session, test_customer) -> None:
        """Test that city is required."""
        address = Address(
            customer_id=test_customer.id,
            address_line_1="123 Main St",
            state="NY",
            zip_code="10001",
            address_type="home",
        )
        db_session.add(address)
        with pytest.raises(IntegrityError):
            db_session.commit()


class TestAddressDefaults:
    """Test Address model defaults."""

    def test_address_country_default(self, db_session, test_customer) -> None:
        """Test that country defaults to USA."""
        address = Address(
            customer_id=test_customer.id,
            address_line_1="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
            address_type="home",
        )
        db_session.add(address)
        db_session.commit()

        assert address.country == "USA"

    def test_address_is_default_default(self, db_session, test_customer) -> None:
        """Test that is_default defaults to False."""
        address = Address(
            customer_id=test_customer.id,
            address_line_1="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
            address_type="home",
        )
        db_session.add(address)
        db_session.commit()

        assert address.is_default is False

    def test_address_is_active_default(self, db_session, test_customer) -> None:
        """Test that is_active defaults to True."""
        address = Address(
            customer_id=test_customer.id,
            address_line_1="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
            address_type="home",
        )
        db_session.add(address)
        db_session.commit()

        assert address.is_active is True


class TestAddressRelationships:
    """Test Address model relationships."""

    def test_address_has_customer_relationship(self, db_session, test_customer) -> None:
        """Test that address has customer relationship."""
        address = Address(
            customer_id=test_customer.id,
            address_line_1="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
            address_type="home",
        )
        db_session.add(address)
        db_session.commit()

        assert address.customer is not None
        assert address.customer.id == test_customer.id

    def test_address_has_pickup_orders_relationship(
        self, db_session, test_customer
    ) -> None:
        """Test that address has pickup_orders relationship."""
        from datetime import datetime, timedelta, timezone

        from app.core.models.order import Order, OrderStatus

        address = Address(
            customer_id=test_customer.id,
            address_line_1="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
            address_type="home",
        )
        db_session.add(address)
        db_session.commit()

        order = Order(
            order_number="ORD-132",
            customer_id=test_customer.id,
            status=OrderStatus.PENDING,
            total_amount=50.0,
            final_amount=50.0,
            pickup_address_id=address.id,
            pickup_date=datetime.now(timezone.utc),
            pickup_time_slot="9:00 AM - 11:00 AM",
            delivery_address_id=address.id,
            delivery_date=datetime.now(timezone.utc) + timedelta(days=1),
            delivery_time_slot="2:00 PM - 4:00 PM",
        )
        db_session.add(order)
        db_session.commit()

        assert len(address.pickup_orders) == 1
        assert address.pickup_orders[0].id == order.id

    def test_address_has_delivery_orders_relationship(
        self, db_session, test_customer
    ) -> None:
        """Test that address has delivery_orders relationship."""
        from datetime import datetime, timedelta, timezone

        from app.core.models.order import Order, OrderStatus

        address = Address(
            customer_id=test_customer.id,
            address_line_1="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
            address_type="home",
        )
        db_session.add(address)
        db_session.commit()

        order = Order(
            order_number="ORD-133",
            customer_id=test_customer.id,
            status=OrderStatus.PENDING,
            total_amount=50.0,
            final_amount=50.0,
            pickup_address_id=address.id,
            pickup_date=datetime.now(timezone.utc),
            pickup_time_slot="9:00 AM - 11:00 AM",
            delivery_address_id=address.id,
            delivery_date=datetime.now(timezone.utc) + timedelta(days=1),
            delivery_time_slot="2:00 PM - 4:00 PM",
        )
        db_session.add(order)
        db_session.commit()

        assert len(address.delivery_orders) == 1
        assert address.delivery_orders[0].id == order.id


class TestAddressTimestamps:
    """Test Address model timestamps."""

    def test_address_has_created_at(self, db_session, test_customer) -> None:
        """Test that address has created_at timestamp."""
        address = Address(
            customer_id=test_customer.id,
            address_line_1="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
            address_type="home",
        )
        db_session.add(address)
        db_session.commit()

        assert address.created_at is not None

    def test_address_has_updated_at(self, db_session, test_customer) -> None:
        """Test that address has updated_at timestamp."""
        address = Address(
            customer_id=test_customer.id,
            address_line_1="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
            address_type="home",
        )
        db_session.add(address)
        db_session.commit()

        assert address.updated_at is not None

    def test_address_updated_at_changes_on_update(
        self, db_session, test_customer
    ) -> None:
        """Test that updated_at changes when address is updated."""
        address = Address(
            customer_id=test_customer.id,
            address_line_1="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
            address_type="home",
        )
        db_session.add(address)
        db_session.commit()

        original_updated_at = address.updated_at
        address.city = "Brooklyn"
        db_session.commit()

        assert address.updated_at != original_updated_at
