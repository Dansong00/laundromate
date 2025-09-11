"""
Factory for creating User test data.
"""

import factory
from app.core.models.user import User
from app.auth.security import get_password_hash


class UserFactory(factory.Factory):
    """Factory for creating User instances."""
    
    class Meta:
        model = User
    
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    hashed_password = factory.LazyFunction(lambda: get_password_hash("testpassword123"))
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone = factory.Faker("phone_number")
    is_active = True
    is_admin = False


class AdminUserFactory(UserFactory):
    """Factory for creating admin User instances."""
    
    email = factory.Sequence(lambda n: f"admin{n}@example.com")
    is_admin = True


class InactiveUserFactory(UserFactory):
    """Factory for creating inactive User instances."""
    
    email = factory.Sequence(lambda n: f"inactive{n}@example.com")
    is_active = False