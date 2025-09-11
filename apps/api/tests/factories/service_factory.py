"""
Factory for creating Service test data.
"""

import factory
from app.core.models.service import Service, ServiceCategory


class ServiceFactory(factory.Factory):
    """Factory for creating Service instances."""
    
    class Meta:
        model = Service
    
    name = factory.Sequence(lambda n: f"Service {n}")
    description = factory.Faker("text", max_nb_chars=200)
    category = factory.Iterator([cat.value for cat in ServiceCategory])
    base_price = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    price_per_pound = factory.Faker("pydecimal", left_digits=1, right_digits=2, positive=True)
    price_per_item = factory.Faker("pydecimal", left_digits=1, right_digits=2, positive=True)
    is_active = True
    requires_special_handling = False
    turnaround_hours = factory.Faker("random_int", min=12, max=72)
    special_instructions = factory.Faker("text", max_nb_chars=100)
    min_order_amount = factory.Faker("pydecimal", left_digits=1, right_digits=2, positive=True)


class WashFoldServiceFactory(ServiceFactory):
    """Factory for creating Wash & Fold service instances."""
    
    name = "Wash & Fold"
    description = "Standard wash and fold service"
    category = ServiceCategory.WASH_FOLD.value
    base_price = 15.00
    price_per_pound = 2.50
    turnaround_hours = 24
    min_order_amount = 10.00


class DryCleanServiceFactory(ServiceFactory):
    """Factory for creating Dry Clean service instances."""
    
    name = "Dry Clean Only"
    description = "Professional dry cleaning service"
    category = ServiceCategory.DRY_CLEAN.value
    base_price = 25.00
    price_per_item = 8.00
    requires_special_handling = True
    turnaround_hours = 48
    min_order_amount = 20.00


class InactiveServiceFactory(ServiceFactory):
    """Factory for creating inactive Service instances."""
    
    name = factory.Sequence(lambda n: f"Inactive Service {n}")
    is_active = False