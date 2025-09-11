"""
Factory for creating Order and OrderItem test data.
"""

import factory
from datetime import datetime, timedelta
from app.core.models.order import Order, OrderStatus
from app.core.models.order_item import OrderItem
from .customer_factory import CustomerFactory
from .address_factory import AddressFactory
from .service_factory import ServiceFactory


class OrderItemFactory(factory.Factory):
    """Factory for creating OrderItem instances."""
    
    class Meta:
        model = OrderItem
    
    service = factory.SubFactory(ServiceFactory)
    item_name = factory.Faker("word")
    item_type = factory.Iterator(["shirt", "pants", "dress", "jacket", "sweater"])
    quantity = factory.Faker("random_int", min=1, max=10)
    unit_price = factory.Faker("pydecimal", left_digits=1, right_digits=2, positive=True)
    total_price = factory.LazyAttribute(lambda obj: obj.unit_price * obj.quantity)
    weight = factory.Faker("pydecimal", left_digits=1, right_digits=2, positive=True)
    special_instructions = factory.Faker("text", max_nb_chars=100)
    fabric_type = factory.Iterator(["cotton", "polyester", "wool", "silk", "linen"])
    color = factory.Faker("color_name")


class OrderFactory(factory.Factory):
    """Factory for creating Order instances."""
    
    class Meta:
        model = Order
    
    customer = factory.SubFactory(CustomerFactory)
    pickup_address = factory.SubFactory(AddressFactory)
    delivery_address = factory.SubFactory(AddressFactory)
    status = OrderStatus.PENDING.value
    total_amount = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    tax_amount = factory.Faker("pydecimal", left_digits=1, right_digits=2, positive=True)
    tip_amount = factory.Faker("pydecimal", left_digits=1, right_digits=2, positive=True)
    final_amount = factory.LazyAttribute(lambda obj: obj.total_amount + obj.tax_amount + obj.tip_amount)
    
    # Pickup details
    pickup_date = factory.LazyFunction(lambda: datetime.now() + timedelta(days=1))
    pickup_time_slot = factory.Iterator(["9:00 AM - 11:00 AM", "11:00 AM - 1:00 PM", "1:00 PM - 3:00 PM"])
    pickup_instructions = factory.Faker("text", max_nb_chars=100)
    
    # Delivery details
    delivery_date = factory.LazyFunction(lambda: datetime.now() + timedelta(days=2))
    delivery_time_slot = factory.Iterator(["9:00 AM - 11:00 AM", "11:00 AM - 1:00 PM", "1:00 PM - 3:00 PM"])
    delivery_instructions = factory.Faker("text", max_nb_chars=100)
    
    # Service preferences
    special_requests = factory.Faker("text", max_nb_chars=200)
    is_rush_order = False
    rush_fee = 0.0


class RushOrderFactory(OrderFactory):
    """Factory for creating rush Order instances."""
    
    is_rush_order = True
    rush_fee = factory.Faker("pydecimal", left_digits=1, right_digits=2, positive=True)
    pickup_date = factory.LazyFunction(lambda: datetime.now() + timedelta(hours=2))
    delivery_date = factory.LazyFunction(lambda: datetime.now() + timedelta(days=1))


class ConfirmedOrderFactory(OrderFactory):
    """Factory for creating confirmed Order instances."""
    
    status = OrderStatus.CONFIRMED.value


class CompletedOrderFactory(OrderFactory):
    """Factory for creating completed Order instances."""
    
    status = OrderStatus.DELIVERED.value
    completed_at = factory.LazyFunction(lambda: datetime.now() - timedelta(hours=1))
    delivered_at = factory.LazyFunction(lambda: datetime.now() - timedelta(hours=1))