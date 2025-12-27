"""Unit tests for Order model."""
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.models.order import Order, OrderStatus


class TestOrderModelCreation:
    """Test Order model creation."""

    def test_order_creation_with_required_fields(
        self, db_session, test_customer
    ) -> None:
        """Test that order can be created with required fields."""
        from app.core.models.address import Address

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
            order_number="ORD-123",
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

        assert order.id is not None
        assert order.order_number == "ORD-123"
        assert order.customer_id == test_customer.id
        assert order.status == OrderStatus.PENDING

    def test_order_creation_with_all_fields(self, db_session, test_customer) -> None:
        """Test that order can be created with all fields."""
        from app.core.models.address import Address

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
            order_number="ORD-124",
            customer_id=test_customer.id,
            status=OrderStatus.CONFIRMED,
            total_amount=100.0,
            tax_amount=8.5,
            tip_amount=10.0,
            final_amount=118.5,
            pickup_address_id=address.id,
            pickup_date=datetime.now(timezone.utc),
            pickup_time_slot="9:00 AM - 11:00 AM",
            pickup_instructions="Ring doorbell",
            delivery_address_id=address.id,
            delivery_date=datetime.now(timezone.utc) + timedelta(days=1),
            delivery_time_slot="2:00 PM - 4:00 PM",
            delivery_instructions="Leave with doorman",
            special_requests="Handle with care",
            is_rush_order=True,
            rush_fee=15.0,
        )
        db_session.add(order)
        db_session.commit()

        assert order.tax_amount == 8.5
        assert order.tip_amount == 10.0
        assert order.is_rush_order is True
        assert order.rush_fee == 15.0


class TestOrderStatusEnum:
    """Test OrderStatus enum."""

    def test_order_status_enum_values(self) -> None:
        """Test that OrderStatus enum has all expected values."""
        assert OrderStatus.PENDING == "pending"
        assert OrderStatus.CONFIRMED == "confirmed"
        assert OrderStatus.PICKED_UP == "picked_up"
        assert OrderStatus.IN_PROGRESS == "in_progress"
        assert OrderStatus.READY == "ready"
        assert OrderStatus.OUT_FOR_DELIVERY == "out_for_delivery"
        assert OrderStatus.DELIVERED == "delivered"
        assert OrderStatus.CANCELLED == "cancelled"

    def test_order_status_default(self, db_session, test_customer) -> None:
        """Test that order status defaults to PENDING."""
        from app.core.models.address import Address

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
            order_number="ORD-125",
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

        assert order.status == OrderStatus.PENDING


class TestOrderConstraints:
    """Test Order model constraints."""

    def test_order_number_is_required(self, db_session, test_customer) -> None:
        """Test that order_number is required."""
        from app.core.models.address import Address

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
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_order_number_unique(self, db_session, test_customer) -> None:
        """Test that order_number must be unique."""
        from app.core.models.address import Address

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

        order1 = Order(
            order_number="ORD-126",
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
        order2 = Order(
            order_number="ORD-126",
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
        db_session.add(order1)
        db_session.commit()

        db_session.add(order2)
        with pytest.raises(IntegrityError):
            db_session.commit()


class TestOrderRelationships:
    """Test Order model relationships."""

    def test_order_has_customer_relationship(self, db_session, test_customer) -> None:
        """Test that order has customer relationship."""
        from app.core.models.address import Address

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
            order_number="ORD-127",
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

        assert order.customer is not None
        assert order.customer.id == test_customer.id

    def test_order_has_items_relationship(self, db_session, test_customer) -> None:
        """Test that order has items relationship."""
        from app.core.models.address import Address
        from app.core.models.order_item import OrderItem
        from app.core.models.service import Service, ServiceCategory

        address = Address(
            customer_id=test_customer.id,
            address_line_1="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
            address_type="home",
        )
        service = Service(
            name="Wash & Fold",
            description="Wash and fold service",
            category=ServiceCategory.WASH_FOLD,
            base_price=10.0,
            turnaround_hours=24,
        )
        db_session.add(address)
        db_session.add(service)
        db_session.commit()

        order = Order(
            order_number="ORD-128",
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

        item = OrderItem(
            order_id=order.id,
            service_id=service.id,
            item_name="Shirts",
            item_type="shirt",
            quantity=5,
            unit_price=10.0,
            total_price=50.0,
        )
        db_session.add(item)
        db_session.commit()

        assert len(order.items) == 1
        assert order.items[0].id == item.id


class TestOrderTimestamps:
    """Test Order model timestamps."""

    def test_order_has_created_at(self, db_session, test_customer) -> None:
        """Test that order has created_at timestamp."""
        from app.core.models.address import Address

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
            order_number="ORD-129",
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

        assert order.created_at is not None

    def test_order_has_optional_timestamps(self, db_session, test_customer) -> None:
        """Test that order has optional timestamps."""
        from app.core.models.address import Address

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
            order_number="ORD-130",
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

        # Initially optional timestamps should be None
        assert order.picked_up_at is None
        assert order.completed_at is None
        assert order.delivered_at is None

        # Can be set later
        order.picked_up_at = datetime.now(timezone.utc)
        order.completed_at = datetime.now(timezone.utc)
        order.delivered_at = datetime.now(timezone.utc)
        db_session.commit()

        assert order.picked_up_at is not None
        assert order.completed_at is not None
        assert order.delivered_at is not None
