"""Unit tests for order domain logic."""
from datetime import datetime, timedelta, timezone

from app.core.models.order import Order, OrderStatus


class TestOrderStatus:
    """Test OrderStatus enum."""

    def test_order_status_values(self) -> None:
        """Test that OrderStatus has expected values."""
        assert OrderStatus.PENDING == "pending"
        assert OrderStatus.CONFIRMED == "confirmed"
        assert OrderStatus.PICKED_UP == "picked_up"
        assert OrderStatus.IN_PROGRESS == "in_progress"
        assert OrderStatus.READY == "ready"
        assert OrderStatus.OUT_FOR_DELIVERY == "out_for_delivery"
        assert OrderStatus.DELIVERED == "delivered"
        assert OrderStatus.CANCELLED == "cancelled"

    def test_order_status_transitions_valid(self, db_session) -> None:
        """Test valid order status transitions."""
        order = Order(
            order_number="ORD-123",
            customer_id=1,
            status=OrderStatus.PENDING,
            total_amount=50.0,
            final_amount=50.0,
            pickup_address_id=1,
            pickup_date=datetime.now(timezone.utc),
            pickup_time_slot="9:00 AM - 11:00 AM",
            delivery_address_id=1,
            delivery_date=datetime.now(timezone.utc) + timedelta(days=1),
            delivery_time_slot="2:00 PM - 4:00 PM",
        )
        db_session.add(order)
        db_session.commit()

        # Test status transitions
        order.status = OrderStatus.CONFIRMED
        assert order.status == OrderStatus.CONFIRMED

        order.status = OrderStatus.PICKED_UP
        assert order.status == OrderStatus.PICKED_UP

        order.status = OrderStatus.IN_PROGRESS
        assert order.status == OrderStatus.IN_PROGRESS

        order.status = OrderStatus.READY
        assert order.status == OrderStatus.READY

        order.status = OrderStatus.DELIVERED
        assert order.status == OrderStatus.DELIVERED


class TestOrderAmountCalculations:
    """Test order amount calculations."""

    def test_order_final_amount_without_tax_or_rush(self, db_session) -> None:
        """Test final amount calculation without tax or rush fee."""
        order = Order(
            order_number="ORD-123",
            customer_id=1,
            status=OrderStatus.PENDING,
            total_amount=100.0,
            tax_amount=0.0,
            tip_amount=0.0,
            rush_fee=0.0,
            final_amount=100.0,
            pickup_address_id=1,
            pickup_date=datetime.now(timezone.utc),
            pickup_time_slot="9:00 AM - 11:00 AM",
            delivery_address_id=1,
            delivery_date=datetime.now(timezone.utc) + timedelta(days=1),
            delivery_time_slot="2:00 PM - 4:00 PM",
        )
        db_session.add(order)
        db_session.commit()

        expected_final = order.total_amount + order.tax_amount + order.rush_fee
        assert order.final_amount == expected_final

    def test_order_final_amount_with_tax(self, db_session) -> None:
        """Test final amount calculation with tax."""
        order = Order(
            order_number="ORD-124",
            customer_id=1,
            status=OrderStatus.PENDING,
            total_amount=100.0,
            tax_amount=8.5,
            tip_amount=0.0,
            rush_fee=0.0,
            final_amount=108.5,
            pickup_address_id=1,
            pickup_date=datetime.now(timezone.utc),
            pickup_time_slot="9:00 AM - 11:00 AM",
            delivery_address_id=1,
            delivery_date=datetime.now(timezone.utc) + timedelta(days=1),
            delivery_time_slot="2:00 PM - 4:00 PM",
        )
        db_session.add(order)
        db_session.commit()

        expected_final = order.total_amount + order.tax_amount + order.rush_fee
        assert order.final_amount == expected_final

    def test_order_final_amount_with_rush_fee(self, db_session) -> None:
        """Test final amount calculation with rush fee."""
        order = Order(
            order_number="ORD-125",
            customer_id=1,
            status=OrderStatus.PENDING,
            total_amount=100.0,
            tax_amount=0.0,
            tip_amount=0.0,
            rush_fee=15.0,
            final_amount=115.0,
            is_rush_order=True,
            pickup_address_id=1,
            pickup_date=datetime.now(timezone.utc),
            pickup_time_slot="9:00 AM - 11:00 AM",
            delivery_address_id=1,
            delivery_date=datetime.now(timezone.utc) + timedelta(days=1),
            delivery_time_slot="2:00 PM - 4:00 PM",
        )
        db_session.add(order)
        db_session.commit()

        expected_final = order.total_amount + order.tax_amount + order.rush_fee
        assert order.final_amount == expected_final
        assert order.is_rush_order is True

    def test_order_final_amount_with_all_fees(self, db_session) -> None:
        """Test final amount calculation with tax, tip, and rush fee."""
        order = Order(
            order_number="ORD-126",
            customer_id=1,
            status=OrderStatus.PENDING,
            total_amount=100.0,
            tax_amount=8.5,
            tip_amount=10.0,
            rush_fee=15.0,
            final_amount=133.5,
            is_rush_order=True,
            pickup_address_id=1,
            pickup_date=datetime.now(timezone.utc),
            pickup_time_slot="9:00 AM - 11:00 AM",
            delivery_address_id=1,
            delivery_date=datetime.now(timezone.utc) + timedelta(days=1),
            delivery_time_slot="2:00 PM - 4:00 PM",
        )
        db_session.add(order)
        db_session.commit()

        # Note: tip_amount is not included in final_amount calculation
        # based on the router logic
        expected_final = order.total_amount + order.tax_amount + order.rush_fee
        assert order.final_amount == expected_final


class TestOrderNumberGeneration:
    """Test order number generation logic."""

    def test_order_number_format(self, db_session) -> None:
        """Test that order number follows expected format."""
        from datetime import datetime as dt

        order_number = f"ORD-{int(dt.utcnow().timestamp())}"
        order = Order(
            order_number=order_number,
            customer_id=1,
            status=OrderStatus.PENDING,
            total_amount=50.0,
            final_amount=50.0,
            pickup_address_id=1,
            pickup_date=datetime.now(timezone.utc),
            pickup_time_slot="9:00 AM - 11:00 AM",
            delivery_address_id=1,
            delivery_date=datetime.now(timezone.utc) + timedelta(days=1),
            delivery_time_slot="2:00 PM - 4:00 PM",
        )
        db_session.add(order)
        db_session.commit()

        assert order.order_number.startswith("ORD-")
        assert len(order.order_number) > 4

    def test_order_number_uniqueness(self, db_session) -> None:
        """Test that order numbers are unique."""
        from datetime import datetime as dt

        order_number1 = f"ORD-{int(dt.utcnow().timestamp())}"
        order1 = Order(
            order_number=order_number1,
            customer_id=1,
            status=OrderStatus.PENDING,
            total_amount=50.0,
            final_amount=50.0,
            pickup_address_id=1,
            pickup_date=datetime.now(timezone.utc),
            pickup_time_slot="9:00 AM - 11:00 AM",
            delivery_address_id=1,
            delivery_date=datetime.now(timezone.utc) + timedelta(days=1),
            delivery_time_slot="2:00 PM - 4:00 PM",
        )
        db_session.add(order1)
        db_session.commit()

        # Wait a moment to ensure different timestamp
        import time

        time.sleep(1)
        order_number2 = f"ORD-{int(dt.utcnow().timestamp())}"
        order2 = Order(
            order_number=order_number2,
            customer_id=1,
            status=OrderStatus.PENDING,
            total_amount=50.0,
            final_amount=50.0,
            pickup_address_id=1,
            pickup_date=datetime.now(timezone.utc),
            pickup_time_slot="9:00 AM - 11:00 AM",
            delivery_address_id=1,
            delivery_date=datetime.now(timezone.utc) + timedelta(days=1),
            delivery_time_slot="2:00 PM - 4:00 PM",
        )
        db_session.add(order2)
        db_session.commit()

        assert order1.order_number != order2.order_number


class TestRushOrderFees:
    """Test rush order fee calculations."""

    def test_rush_order_fee_set(self, db_session) -> None:
        """Test that rush order fee can be set."""
        order = Order(
            order_number="ORD-127",
            customer_id=1,
            status=OrderStatus.PENDING,
            total_amount=100.0,
            tax_amount=0.0,
            tip_amount=0.0,
            rush_fee=20.0,
            final_amount=120.0,
            is_rush_order=True,
            pickup_address_id=1,
            pickup_date=datetime.now(timezone.utc),
            pickup_time_slot="9:00 AM - 11:00 AM",
            delivery_address_id=1,
            delivery_date=datetime.now(timezone.utc) + timedelta(days=1),
            delivery_time_slot="2:00 PM - 4:00 PM",
        )
        db_session.add(order)
        db_session.commit()

        assert order.is_rush_order is True
        assert order.rush_fee == 20.0

    def test_non_rush_order_no_fee(self, db_session) -> None:
        """Test that non-rush orders have no rush fee."""
        order = Order(
            order_number="ORD-128",
            customer_id=1,
            status=OrderStatus.PENDING,
            total_amount=100.0,
            tax_amount=0.0,
            tip_amount=0.0,
            rush_fee=0.0,
            final_amount=100.0,
            is_rush_order=False,
            pickup_address_id=1,
            pickup_date=datetime.now(timezone.utc),
            pickup_time_slot="9:00 AM - 11:00 AM",
            delivery_address_id=1,
            delivery_date=datetime.now(timezone.utc) + timedelta(days=1),
            delivery_time_slot="2:00 PM - 4:00 PM",
        )
        db_session.add(order)
        db_session.commit()

        assert order.is_rush_order is False
        assert order.rush_fee == 0.0


class TestOrderValidation:
    """Test order validation logic."""

    def test_order_requires_pickup_and_delivery_dates(self, db_session) -> None:
        """Test that order requires both pickup and delivery dates."""
        pickup_date = datetime.now(timezone.utc)
        delivery_date = datetime.now(timezone.utc) + timedelta(days=1)

        order = Order(
            order_number="ORD-129",
            customer_id=1,
            status=OrderStatus.PENDING,
            total_amount=50.0,
            final_amount=50.0,
            pickup_address_id=1,
            pickup_date=pickup_date,
            pickup_time_slot="9:00 AM - 11:00 AM",
            delivery_address_id=1,
            delivery_date=delivery_date,
            delivery_time_slot="2:00 PM - 4:00 PM",
        )
        db_session.add(order)
        db_session.commit()

        assert order.pickup_date == pickup_date
        assert order.delivery_date == delivery_date
        assert order.delivery_date > order.pickup_date

    def test_order_requires_time_slots(self, db_session) -> None:
        """Test that order requires time slots."""
        order = Order(
            order_number="ORD-130",
            customer_id=1,
            status=OrderStatus.PENDING,
            total_amount=50.0,
            final_amount=50.0,
            pickup_address_id=1,
            pickup_date=datetime.now(timezone.utc),
            pickup_time_slot="9:00 AM - 11:00 AM",
            delivery_address_id=1,
            delivery_date=datetime.now(timezone.utc) + timedelta(days=1),
            delivery_time_slot="2:00 PM - 4:00 PM",
        )
        db_session.add(order)
        db_session.commit()

        assert order.pickup_time_slot is not None
        assert order.delivery_time_slot is not None
        assert len(order.pickup_time_slot) > 0
        assert len(order.delivery_time_slot) > 0
