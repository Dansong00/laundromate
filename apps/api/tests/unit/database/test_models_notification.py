"""Unit tests for Notification model."""
from datetime import datetime, timezone

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.models.notification import (
    Notification,
    NotificationStatus,
    NotificationType,
)


class TestNotificationModelCreation:
    """Test Notification model creation."""

    def test_notification_creation_with_required_fields(
        self, db_session, test_customer
    ) -> None:
        """Test that notification can be created with required fields."""
        notification = Notification(
            customer_id=test_customer.id,
            type=NotificationType.ORDER_CONFIRMATION,
            title="Order Confirmed",
            message="Your order has been confirmed",
            delivery_method="email",
        )
        db_session.add(notification)
        db_session.commit()

        assert notification.id is not None
        assert notification.customer_id == test_customer.id
        assert notification.type == NotificationType.ORDER_CONFIRMATION
        assert notification.title == "Order Confirmed"
        assert notification.message == "Your order has been confirmed"
        assert notification.delivery_method == "email"

    def test_notification_creation_with_all_fields(
        self, db_session, test_customer
    ) -> None:
        """Test that notification can be created with all fields."""
        notification = Notification(
            customer_id=test_customer.id,
            order_id=1,
            type=NotificationType.ORDER_READY,
            title="Order Ready",
            message="Your order is ready for pickup",
            delivery_method="sms",
            status=NotificationStatus.SENT,
            sent_at=datetime.now(timezone.utc),
            delivered_at=datetime.now(timezone.utc),
            external_id="ext-123",
            retry_count=0,
        )
        db_session.add(notification)
        db_session.commit()

        assert notification.order_id == 1
        assert notification.status == NotificationStatus.SENT
        assert notification.sent_at is not None
        assert notification.delivered_at is not None
        assert notification.external_id == "ext-123"
        assert notification.retry_count == 0


class TestNotificationTypeEnum:
    """Test NotificationType enum."""

    def test_notification_type_enum_values(self) -> None:
        """Test that NotificationType enum has all expected values."""
        assert NotificationType.ORDER_CONFIRMATION == "order_confirmation"
        assert NotificationType.PICKUP_REMINDER == "pickup_reminder"
        assert NotificationType.ORDER_READY == "order_ready"
        assert NotificationType.OUT_FOR_DELIVERY == "out_for_delivery"
        assert NotificationType.DELIVERY_CONFIRMATION == "delivery_confirmation"
        assert NotificationType.ORDER_STATUS_UPDATE == "order_status_update"
        assert NotificationType.PROMOTIONAL == "promotional"


class TestNotificationStatusEnum:
    """Test NotificationStatus enum."""

    def test_notification_status_enum_values(self) -> None:
        """Test that NotificationStatus enum has all expected values."""
        assert NotificationStatus.PENDING == "pending"
        assert NotificationStatus.SENT == "sent"
        assert NotificationStatus.DELIVERED == "delivered"
        assert NotificationStatus.FAILED == "failed"
        assert NotificationStatus.READ == "read"

    def test_notification_status_default(self, db_session, test_customer) -> None:
        """Test that notification status defaults to PENDING."""
        notification = Notification(
            customer_id=test_customer.id,
            type=NotificationType.ORDER_CONFIRMATION,
            title="Order Confirmed",
            message="Your order has been confirmed",
            delivery_method="email",
        )
        db_session.add(notification)
        db_session.commit()

        assert notification.status == NotificationStatus.PENDING


class TestNotificationConstraints:
    """Test Notification model constraints."""

    def test_notification_customer_id_is_required(self, db_session) -> None:
        """Test that customer_id is required."""
        notification = Notification(
            type=NotificationType.ORDER_CONFIRMATION,
            title="Order Confirmed",
            message="Your order has been confirmed",
            delivery_method="email",
        )
        db_session.add(notification)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_notification_type_is_required(self, db_session, test_customer) -> None:
        """Test that type is required."""
        notification = Notification(
            customer_id=test_customer.id,
            title="Order Confirmed",
            message="Your order has been confirmed",
            delivery_method="email",
        )
        db_session.add(notification)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_notification_title_is_required(self, db_session, test_customer) -> None:
        """Test that title is required."""
        notification = Notification(
            customer_id=test_customer.id,
            type=NotificationType.ORDER_CONFIRMATION,
            message="Your order has been confirmed",
            delivery_method="email",
        )
        db_session.add(notification)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_notification_order_id_is_optional(self, db_session, test_customer) -> None:
        """Test that order_id is optional."""
        notification = Notification(
            customer_id=test_customer.id,
            order_id=None,
            type=NotificationType.PROMOTIONAL,
            title="Special Offer",
            message="Get 20% off your next order",
            delivery_method="email",
        )
        db_session.add(notification)
        db_session.commit()

        assert notification.order_id is None


class TestNotificationDefaults:
    """Test Notification model defaults."""

    def test_notification_status_default(self, db_session, test_customer) -> None:
        """Test that status defaults to PENDING."""
        notification = Notification(
            customer_id=test_customer.id,
            type=NotificationType.ORDER_CONFIRMATION,
            title="Order Confirmed",
            message="Your order has been confirmed",
            delivery_method="email",
        )
        db_session.add(notification)
        db_session.commit()

        assert notification.status == NotificationStatus.PENDING

    def test_notification_retry_count_default(self, db_session, test_customer) -> None:
        """Test that retry_count defaults to 0."""
        notification = Notification(
            customer_id=test_customer.id,
            type=NotificationType.ORDER_CONFIRMATION,
            title="Order Confirmed",
            message="Your order has been confirmed",
            delivery_method="email",
        )
        db_session.add(notification)
        db_session.commit()

        assert notification.retry_count == 0


class TestNotificationRelationships:
    """Test Notification model relationships."""

    def test_notification_has_customer_relationship(
        self, db_session, test_customer
    ) -> None:
        """Test that notification has customer relationship."""
        notification = Notification(
            customer_id=test_customer.id,
            type=NotificationType.ORDER_CONFIRMATION,
            title="Order Confirmed",
            message="Your order has been confirmed",
            delivery_method="email",
        )
        db_session.add(notification)
        db_session.commit()

        assert notification.customer is not None
        assert notification.customer.id == test_customer.id

    def test_notification_has_order_relationship(
        self, db_session, test_customer
    ) -> None:
        """Test that notification has order relationship."""
        from datetime import datetime, timedelta, timezone

        from app.core.models.address import Address
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
            order_number="ORD-142",
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

        notification = Notification(
            customer_id=test_customer.id,
            order_id=order.id,
            type=NotificationType.ORDER_CONFIRMATION,
            title="Order Confirmed",
            message="Your order has been confirmed",
            delivery_method="email",
        )
        db_session.add(notification)
        db_session.commit()

        assert notification.order is not None
        assert notification.order.id == order.id


class TestNotificationTimestamps:
    """Test Notification model timestamps."""

    def test_notification_has_created_at(self, db_session, test_customer) -> None:
        """Test that notification has created_at timestamp."""
        notification = Notification(
            customer_id=test_customer.id,
            type=NotificationType.ORDER_CONFIRMATION,
            title="Order Confirmed",
            message="Your order has been confirmed",
            delivery_method="email",
        )
        db_session.add(notification)
        db_session.commit()

        assert notification.created_at is not None

    def test_notification_has_optional_timestamps(
        self, db_session, test_customer
    ) -> None:
        """Test that notification has optional timestamps."""
        notification = Notification(
            customer_id=test_customer.id,
            type=NotificationType.ORDER_CONFIRMATION,
            title="Order Confirmed",
            message="Your order has been confirmed",
            delivery_method="email",
        )
        db_session.add(notification)
        db_session.commit()

        # Initially optional timestamps should be None
        assert notification.sent_at is None
        assert notification.delivered_at is None
        assert notification.read_at is None

        # Can be set later
        notification.sent_at = datetime.now(timezone.utc)
        notification.delivered_at = datetime.now(timezone.utc)
        notification.read_at = datetime.now(timezone.utc)
        db_session.commit()

        assert notification.sent_at is not None
        assert notification.delivered_at is not None
        assert notification.read_at is not None
