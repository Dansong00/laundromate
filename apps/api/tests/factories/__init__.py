"""
Test data factories for LaundroMate API tests.

This module provides Factory Boy factories for creating test data
across all database models.
"""

from .user_factory import UserFactory, AdminUserFactory, InactiveUserFactory
from .customer_factory import CustomerFactory, VIPCustomerFactory, CustomerWithoutNotificationsFactory
from .service_factory import ServiceFactory, WashFoldServiceFactory, DryCleanServiceFactory, InactiveServiceFactory
from .address_factory import AddressFactory, DefaultAddressFactory, PickupAddressFactory, DeliveryAddressFactory
from .order_factory import OrderFactory, OrderItemFactory, RushOrderFactory, ConfirmedOrderFactory, CompletedOrderFactory
from .notification_factory import NotificationFactory, EmailNotificationFactory, SMSNotificationFactory, SentNotificationFactory, FailedNotificationFactory

__all__ = [
    "UserFactory",
    "AdminUserFactory", 
    "InactiveUserFactory",
    "CustomerFactory",
    "VIPCustomerFactory",
    "CustomerWithoutNotificationsFactory",
    "ServiceFactory",
    "WashFoldServiceFactory",
    "DryCleanServiceFactory", 
    "InactiveServiceFactory",
    "AddressFactory",
    "DefaultAddressFactory",
    "PickupAddressFactory",
    "DeliveryAddressFactory",
    "OrderFactory",
    "OrderItemFactory",
    "RushOrderFactory",
    "ConfirmedOrderFactory",
    "CompletedOrderFactory",
    "NotificationFactory",
    "EmailNotificationFactory",
    "SMSNotificationFactory",
    "SentNotificationFactory",
    "FailedNotificationFactory",
]