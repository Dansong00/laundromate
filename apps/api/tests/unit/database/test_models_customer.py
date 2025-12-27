"""Unit tests for Customer model."""
import pytest
from sqlalchemy.exc import IntegrityError

from app.core.models.customer import Customer


class TestCustomerModelCreation:
    """Test Customer model creation."""

    def test_customer_creation_with_required_fields(
        self, db_session, test_user
    ) -> None:
        """Test that customer can be created with required fields only."""
        customer = Customer(
            user_id=test_user.id,
        )
        db_session.add(customer)
        db_session.commit()

        assert customer.id is not None
        assert customer.user_id == test_user.id
        assert customer.loyalty_points == 0
        assert customer.is_vip is False
        assert customer.email_notifications is True
        assert customer.sms_notifications is True

    def test_customer_creation_with_all_fields(self, db_session, test_user) -> None:
        """Test that customer can be created with all fields."""
        customer = Customer(
            user_id=test_user.id,
            preferred_pickup_time="morning",
            special_instructions="Ring doorbell twice",
            loyalty_points=100,
            is_vip=True,
            email_notifications=False,
            sms_notifications=True,
        )
        db_session.add(customer)
        db_session.commit()

        assert customer.preferred_pickup_time == "morning"
        assert customer.special_instructions == "Ring doorbell twice"
        assert customer.loyalty_points == 100
        assert customer.is_vip is True
        assert customer.email_notifications is False
        assert customer.sms_notifications is True


class TestCustomerConstraints:
    """Test Customer model constraints."""

    def test_customer_user_id_is_required(self, db_session) -> None:
        """Test that user_id is required."""
        customer = Customer()
        db_session.add(customer)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_customer_user_id_unique(self, db_session, test_user) -> None:
        """Test that user_id must be unique (one-to-one relationship)."""
        customer1 = Customer(user_id=test_user.id)
        customer2 = Customer(user_id=test_user.id)
        db_session.add(customer1)
        db_session.commit()

        db_session.add(customer2)
        with pytest.raises(IntegrityError):
            db_session.commit()


class TestCustomerDefaults:
    """Test Customer model defaults."""

    def test_customer_loyalty_points_default(self, db_session, test_user) -> None:
        """Test that loyalty_points defaults to 0."""
        customer = Customer(user_id=test_user.id)
        db_session.add(customer)
        db_session.commit()

        assert customer.loyalty_points == 0

    def test_customer_is_vip_default(self, db_session, test_user) -> None:
        """Test that is_vip defaults to False."""
        customer = Customer(user_id=test_user.id)
        db_session.add(customer)
        db_session.commit()

        assert customer.is_vip is False

    def test_customer_notification_preferences_default(
        self, db_session, test_user
    ) -> None:
        """Test that notification preferences default to True."""
        customer = Customer(user_id=test_user.id)
        db_session.add(customer)
        db_session.commit()

        assert customer.email_notifications is True
        assert customer.sms_notifications is True


class TestCustomerRelationships:
    """Test Customer model relationships."""

    def test_customer_has_user_relationship(self, db_session, test_user) -> None:
        """Test that customer has user relationship."""
        customer = Customer(user_id=test_user.id)
        db_session.add(customer)
        db_session.commit()

        assert customer.user is not None
        assert customer.user.id == test_user.id

    def test_customer_has_addresses_relationship(self, db_session, test_user) -> None:
        """Test that customer has addresses relationship."""
        from app.core.models.address import Address

        customer = Customer(user_id=test_user.id)
        db_session.add(customer)
        db_session.commit()

        address = Address(
            customer_id=customer.id,
            address_line_1="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
            address_type="home",
        )
        db_session.add(address)
        db_session.commit()

        assert len(customer.addresses) == 1
        assert customer.addresses[0].id == address.id

    def test_customer_has_orders_relationship(self, db_session, test_user) -> None:
        """Test that customer has orders relationship."""
        from datetime import datetime, timedelta, timezone

        from app.core.models.order import Order, OrderStatus

        customer = Customer(user_id=test_user.id)
        db_session.add(customer)
        db_session.commit()

        order = Order(
            order_number="ORD-123",
            customer_id=customer.id,
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

        assert len(customer.orders) == 1
        assert customer.orders[0].id == order.id

    def test_customer_has_notifications_relationship(
        self, db_session, test_user
    ) -> None:
        """Test that customer has notifications relationship."""
        from app.core.models.notification import Notification, NotificationType

        customer = Customer(user_id=test_user.id)
        db_session.add(customer)
        db_session.commit()

        notification = Notification(
            customer_id=customer.id,
            type=NotificationType.ORDER_CONFIRMATION,
            title="Order Confirmed",
            message="Your order has been confirmed",
            delivery_method="email",
        )
        db_session.add(notification)
        db_session.commit()

        assert len(customer.notifications) == 1
        assert customer.notifications[0].id == notification.id


class TestCustomerTimestamps:
    """Test Customer model timestamps."""

    def test_customer_has_created_at(self, db_session, test_user) -> None:
        """Test that customer has created_at timestamp."""
        customer = Customer(user_id=test_user.id)
        db_session.add(customer)
        db_session.commit()

        assert customer.created_at is not None

    def test_customer_has_updated_at(self, db_session, test_user) -> None:
        """Test that customer has updated_at timestamp."""
        customer = Customer(user_id=test_user.id)
        db_session.add(customer)
        db_session.commit()

        assert customer.updated_at is not None

    def test_customer_updated_at_changes_on_update(self, db_session, test_user) -> None:
        """Test that updated_at changes when customer is updated."""
        customer = Customer(user_id=test_user.id)
        db_session.add(customer)
        db_session.commit()

        original_updated_at = customer.updated_at
        customer.loyalty_points = 100
        db_session.commit()

        assert customer.updated_at != original_updated_at
