"""
Factory for creating Customer test data.
"""

import factory
from app.core.models.customer import Customer
from .user_factory import UserFactory


class CustomerFactory(factory.Factory):
    """Factory for creating Customer instances."""
    
    class Meta:
        model = Customer
    
    user = factory.SubFactory(UserFactory)
    preferred_pickup_time = factory.Iterator(["morning", "afternoon", "evening"])
    special_instructions = factory.Faker("text", max_nb_chars=200)
    loyalty_points = factory.Faker("random_int", min=0, max=1000)
    is_vip = False
    email_notifications = True
    sms_notifications = True


class VIPCustomerFactory(CustomerFactory):
    """Factory for creating VIP Customer instances."""
    
    loyalty_points = factory.Faker("random_int", min=500, max=2000)
    is_vip = True


class CustomerWithoutNotificationsFactory(CustomerFactory):
    """Factory for creating Customer instances without notifications."""
    
    email_notifications = False
    sms_notifications = False