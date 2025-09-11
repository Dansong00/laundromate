"""
Factory for creating Address test data.
"""

import factory
from app.core.models.address import Address
from .customer_factory import CustomerFactory


class AddressFactory(factory.Factory):
    """Factory for creating Address instances."""
    
    class Meta:
        model = Address
    
    customer = factory.SubFactory(CustomerFactory)
    address_type = factory.Iterator(["home", "work", "pickup", "delivery"])
    address_line_1 = factory.Faker("street_address")
    address_line_2 = factory.Faker("secondary_address")
    city = factory.Faker("city")
    state = factory.Faker("state_abbr")
    zip_code = factory.Faker("postcode")
    country = "USA"
    is_default = False
    is_active = True
    instructions = factory.Faker("text", max_nb_chars=100)


class DefaultAddressFactory(AddressFactory):
    """Factory for creating default Address instances."""
    
    is_default = True


class PickupAddressFactory(AddressFactory):
    """Factory for creating pickup Address instances."""
    
    address_type = "pickup"
    instructions = "Ring doorbell twice"


class DeliveryAddressFactory(AddressFactory):
    """Factory for creating delivery Address instances."""
    
    address_type = "delivery"
    instructions = "Leave at front door"