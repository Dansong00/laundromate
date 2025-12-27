"""Unit tests for notification domain logic."""
from datetime import datetime, timezone

from app.core.models.notification import (
    Notification,
    NotificationStatus,
    NotificationType,
)


class TestNotificationType:
    """Test NotificationType enum."""

    def test_notification_type_values(self) -> None:
        """Test that NotificationType has expected values."""
        assert NotificationType.ORDER_CONFIRMATION == "order_confirmation"
        assert NotificationType.PICKUP_REMINDER == "pickup_reminder"
        assert NotificationType.ORDER_READY == "order_ready"
        assert NotificationType.OUT_FOR_DELIVERY == "out_for_delivery"
        assert NotificationType.DELIVERY_CONFIRMATION == "delivery_confirmation"
        assert NotificationType.ORDER_STATUS_UPDATE == "order_status_update"
        assert NotificationType.PROMOTIONAL == "promotional"


class TestNotificationStatus:
    """Test NotificationStatus enum."""

    def test_notification_status_values(self) -> None:
        """Test that NotificationStatus has expected values."""
        assert NotificationStatus.PENDING == "pending"
        assert NotificationStatus.SENT == "sent"
        assert NotificationStatus.DELIVERED == "delivered"
        assert NotificationStatus.FAILED == "failed"
        assert NotificationStatus.READ == "read"


class TestNotificationStatusTransitions:
    """Test notification status transitions."""

    def test_notification_starts_as_pending(self, db_session, test_customer) -> None:
        """Test that notification starts with PENDING status."""
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

    def test_notification_status_transition_to_sent(
        self, db_session, test_customer
    ) -> None:
        """Test notification status transition to SENT."""
        notification = Notification(
            customer_id=test_customer.id,
            type=NotificationType.ORDER_CONFIRMATION,
            title="Order Confirmed",
            message="Your order has been confirmed",
            delivery_method="email",
        )
        db_session.add(notification)
        db_session.commit()

        notification.status = NotificationStatus.SENT
        notification.sent_at = datetime.now(timezone.utc)
        db_session.commit()

        assert notification.status == NotificationStatus.SENT
        assert notification.sent_at is not None

    def test_notification_status_transition_to_delivered(
        self, db_session, test_customer
    ) -> None:
        """Test notification status transition to DELIVERED."""
        notification = Notification(
            customer_id=test_customer.id,
            type=NotificationType.ORDER_CONFIRMATION,
            title="Order Confirmed",
            message="Your order has been confirmed",
            delivery_method="email",
            status=NotificationStatus.SENT,
            sent_at=datetime.now(timezone.utc),
        )
        db_session.add(notification)
        db_session.commit()

        notification.status = NotificationStatus.DELIVERED
        notification.delivered_at = datetime.now(timezone.utc)
        db_session.commit()

        assert notification.status == NotificationStatus.DELIVERED
        assert notification.delivered_at is not None

    def test_notification_status_transition_to_failed(
        self, db_session, test_customer
    ) -> None:
        """Test notification status transition to FAILED."""
        notification = Notification(
            customer_id=test_customer.id,
            type=NotificationType.ORDER_CONFIRMATION,
            title="Order Confirmed",
            message="Your order has been confirmed",
            delivery_method="email",
            status=NotificationStatus.PENDING,
        )
        db_session.add(notification)
        db_session.commit()

        notification.status = NotificationStatus.FAILED
        notification.error_message = "Failed to send email"
        db_session.commit()

        assert notification.status == NotificationStatus.FAILED
        assert notification.error_message is not None

    def test_notification_status_transition_to_read(
        self, db_session, test_customer
    ) -> None:
        """Test notification status transition to READ."""
        notification = Notification(
            customer_id=test_customer.id,
            type=NotificationType.ORDER_CONFIRMATION,
            title="Order Confirmed",
            message="Your order has been confirmed",
            delivery_method="email",
            status=NotificationStatus.DELIVERED,
            delivered_at=datetime.now(timezone.utc),
        )
        db_session.add(notification)
        db_session.commit()

        notification.status = NotificationStatus.READ
        notification.read_at = datetime.now(timezone.utc)
        db_session.commit()

        assert notification.status == NotificationStatus.READ
        assert notification.read_at is not None


class TestNotificationTypes:
    """Test different notification types."""

    def test_order_confirmation_notification(self, db_session, test_customer) -> None:
        """Test order confirmation notification."""
        notification = Notification(
            customer_id=test_customer.id,
            order_id=1,
            type=NotificationType.ORDER_CONFIRMATION,
            title="Order Confirmed",
            message="Your order #123 has been confirmed",
            delivery_method="email",
        )
        db_session.add(notification)
        db_session.commit()

        assert notification.type == NotificationType.ORDER_CONFIRMATION
        assert notification.order_id == 1

    def test_pickup_reminder_notification(self, db_session, test_customer) -> None:
        """Test pickup reminder notification."""
        notification = Notification(
            customer_id=test_customer.id,
            order_id=1,
            type=NotificationType.PICKUP_REMINDER,
            title="Pickup Reminder",
            message="Your order will be picked up tomorrow",
            delivery_method="sms",
        )
        db_session.add(notification)
        db_session.commit()

        assert notification.type == NotificationType.PICKUP_REMINDER

    def test_order_ready_notification(self, db_session, test_customer) -> None:
        """Test order ready notification."""
        notification = Notification(
            customer_id=test_customer.id,
            order_id=1,
            type=NotificationType.ORDER_READY,
            title="Order Ready",
            message="Your order is ready for pickup",
            delivery_method="sms",
        )
        db_session.add(notification)
        db_session.commit()

        assert notification.type == NotificationType.ORDER_READY

    def test_promotional_notification_no_order(self, db_session, test_customer) -> None:
        """Test promotional notification without order."""
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

        assert notification.type == NotificationType.PROMOTIONAL
        assert notification.order_id is None


class TestRetryLogic:
    """Test notification retry logic."""

    def test_retry_count_default_zero(self, db_session, test_customer) -> None:
        """Test that retry count defaults to 0."""
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

    def test_retry_count_increments(self, db_session, test_customer) -> None:
        """Test that retry count can be incremented."""
        notification = Notification(
            customer_id=test_customer.id,
            type=NotificationType.ORDER_CONFIRMATION,
            title="Order Confirmed",
            message="Your order has been confirmed",
            delivery_method="email",
            retry_count=0,
        )
        db_session.add(notification)
        db_session.commit()

        notification.retry_count += 1
        db_session.commit()

        assert notification.retry_count == 1

    def test_failed_notification_has_error_message(
        self, db_session, test_customer
    ) -> None:
        """Test that failed notification has error message."""
        notification = Notification(
            customer_id=test_customer.id,
            type=NotificationType.ORDER_CONFIRMATION,
            title="Order Confirmed",
            message="Your order has been confirmed",
            delivery_method="email",
            status=NotificationStatus.FAILED,
            error_message="SMTP server error",
            retry_count=3,
        )
        db_session.add(notification)
        db_session.commit()

        assert notification.status == NotificationStatus.FAILED
        assert notification.error_message == "SMTP server error"
        assert notification.retry_count == 3


class TestDeliveryMethods:
    """Test notification delivery methods."""

    def test_email_delivery_method(self, db_session, test_customer) -> None:
        """Test email delivery method."""
        notification = Notification(
            customer_id=test_customer.id,
            type=NotificationType.ORDER_CONFIRMATION,
            title="Order Confirmed",
            message="Your order has been confirmed",
            delivery_method="email",
        )
        db_session.add(notification)
        db_session.commit()

        assert notification.delivery_method == "email"

    def test_sms_delivery_method(self, db_session, test_customer) -> None:
        """Test SMS delivery method."""
        notification = Notification(
            customer_id=test_customer.id,
            type=NotificationType.PICKUP_REMINDER,
            title="Pickup Reminder",
            message="Your order will be picked up tomorrow",
            delivery_method="sms",
        )
        db_session.add(notification)
        db_session.commit()

        assert notification.delivery_method == "sms"

    def test_push_delivery_method(self, db_session, test_customer) -> None:
        """Test push notification delivery method."""
        notification = Notification(
            customer_id=test_customer.id,
            type=NotificationType.ORDER_STATUS_UPDATE,
            title="Status Update",
            message="Your order status has been updated",
            delivery_method="push",
        )
        db_session.add(notification)
        db_session.commit()

        assert notification.delivery_method == "push"

    def test_in_app_delivery_method(self, db_session, test_customer) -> None:
        """Test in-app notification delivery method."""
        notification = Notification(
            customer_id=test_customer.id,
            type=NotificationType.ORDER_STATUS_UPDATE,
            title="Status Update",
            message="Your order status has been updated",
            delivery_method="in_app",
        )
        db_session.add(notification)
        db_session.commit()

        assert notification.delivery_method == "in_app"
