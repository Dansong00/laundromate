"""
Factory for creating Notification test data.
"""

import factory
from app.core.models.notification import Notification, NotificationType, NotificationStatus
from .customer_factory import CustomerFactory
from .order_factory import OrderFactory


class NotificationFactory(factory.Factory):
    """Factory for creating Notification instances."""
    
    class Meta:
        model = Notification
    
    customer = factory.SubFactory(CustomerFactory)
    order = factory.SubFactory(OrderFactory)
    type = factory.Iterator([notif_type.value for notif_type in NotificationType])
    title = factory.Faker("sentence", nb_words=4)
    message = factory.Faker("text", max_nb_chars=200)
    delivery_method = factory.Iterator(["email", "sms", "push", "in_app"])
    status = factory.Iterator([status.value for status in NotificationStatus])
    sent_at = factory.LazyFunction(lambda: None)  # Will be set when sent


class EmailNotificationFactory(NotificationFactory):
    """Factory for creating email Notification instances."""
    
    delivery_method = "email"
    title = factory.Faker("sentence", nb_words=3)
    message = factory.Faker("text", max_nb_chars=150)


class SMSNotificationFactory(NotificationFactory):
    """Factory for creating SMS Notification instances."""
    
    delivery_method = "sms"
    title = factory.Faker("sentence", nb_words=2)
    message = factory.Faker("text", max_nb_chars=100)


class SentNotificationFactory(NotificationFactory):
    """Factory for creating sent Notification instances."""
    
    status = NotificationStatus.SENT.value
    sent_at = factory.Faker("date_time_between", start_date="-1h", end_date="now")


class FailedNotificationFactory(NotificationFactory):
    """Factory for creating failed Notification instances."""
    
    status = NotificationStatus.FAILED.value
    error_message = factory.Faker("sentence", nb_words=5)