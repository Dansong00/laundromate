"""
Pytest configuration and fixtures for LaundroMate API tests.

This module provides shared fixtures for database setup, authentication,
and test data creation across all test modules.
"""

import asyncio
import os
from typing import Generator

import pytest
from app.auth.security import create_access_token, get_password_hash
from app.core.database.session import get_db
from app.core.models import Base
from app.core.models.address import Address
from app.core.models.customer import Customer
from app.core.models.order import Order
from app.core.models.service import Service, ServiceCategory
from app.core.models.user import User
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

# Import factories
from tests.factories import (
    UserFactory, AdminUserFactory, InactiveUserFactory,
    CustomerFactory, VIPCustomerFactory,
    ServiceFactory, WashFoldServiceFactory, DryCleanServiceFactory,
    AddressFactory, DefaultAddressFactory,
    OrderFactory, OrderItemFactory, RushOrderFactory,
    NotificationFactory
)

# Test database URL - using SQLite for tests
TEST_DATABASE_URL = "sqlite:///./test_laundromate.db"

# Create test database engine
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session factory
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Create a fresh database session for each test.
    Automatically rolls back after each test to keep tests isolated.
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create session
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> TestClient:
    """
    Create a test client with overridden database dependency.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session: Session) -> User:
    """Create a test user in the database."""
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword123"),
        first_name="Test",
        last_name="User",
        phone="+1234567890",
        is_active=True,
        is_admin=False
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def admin_user(db_session: Session) -> User:
    """Create a test admin user in the database."""
    user = User(
        email="admin@example.com",
        hashed_password=get_password_hash("adminpassword123"),
        first_name="Admin",
        last_name="User",
        phone="+1234567891",
        is_active=True,
        is_admin=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_customer(db_session: Session, test_user: User) -> Customer:
    """Create a test customer linked to a test user."""
    customer = Customer(
        user_id=test_user.id,
        preferred_pickup_time="morning",
        special_instructions="Ring doorbell twice",
        loyalty_points=100,
        is_vip=False,
        email_notifications=True,
        sms_notifications=True
    )
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)
    return customer


@pytest.fixture
def test_service(db_session: Session) -> Service:
    """Create a test service."""
    service = Service(
        name="Wash & Fold",
        description="Standard wash and fold service",
        category=ServiceCategory.WASH_FOLD,
        base_price=15.00,
        price_per_pound=2.50,
        is_active=True,
        requires_special_handling=False,
        turnaround_hours=24,
        min_order_amount=10.00
    )
    db_session.add(service)
    db_session.commit()
    db_session.refresh(service)
    return service


@pytest.fixture
def auth_headers(test_user: User) -> dict:
    """Create authentication headers for test requests."""
    access_token = create_access_token(subject=str(test_user.id))
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def admin_auth_headers(admin_user: User) -> dict:
    """Create authentication headers for admin test requests."""
    access_token = create_access_token(subject=str(admin_user.id))
    return {"Authorization": f"Bearer {access_token}"}


# Test data fixtures
@pytest.fixture
def sample_user_data() -> dict:
    """Sample user registration data."""
    return {
        "email": "newuser@example.com",
        "password": "newpassword123",
        "first_name": "New",
        "last_name": "User",
        "phone": "+1234567892"
    }


@pytest.fixture
def sample_service_data() -> dict:
    """Sample service creation data."""
    return {
        "name": "Dry Clean Only",
        "description": "Professional dry cleaning service",
        "category": "dry_clean",
        "base_price": 25.00,
        "price_per_item": 8.00,
        "is_active": True,
        "requires_special_handling": True,
        "turnaround_hours": 48,
        "special_instructions": "Handle with care",
        "min_order_amount": 20.00
    }


@pytest.fixture
def sample_login_data() -> dict:
    """Sample login data."""
    return {
        "email": "test@example.com",
        "password": "testpassword123"
    }


# Factory-based fixtures for more flexible test data
@pytest.fixture
def factory_user(db_session: Session) -> User:
    """Create a user using factory."""
    user = UserFactory()
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def factory_admin_user(db_session: Session) -> User:
    """Create an admin user using factory."""
    user = AdminUserFactory()
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def factory_customer(db_session: Session) -> Customer:
    """Create a customer using factory."""
    customer = CustomerFactory()
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)
    return customer


@pytest.fixture
def factory_service(db_session: Session) -> Service:
    """Create a service using factory."""
    service = ServiceFactory()
    db_session.add(service)
    db_session.commit()
    db_session.refresh(service)
    return service


@pytest.fixture
def factory_wash_fold_service(db_session: Session) -> Service:
    """Create a wash & fold service using factory."""
    service = WashFoldServiceFactory()
    db_session.add(service)
    db_session.commit()
    db_session.refresh(service)
    return service


@pytest.fixture
def factory_address(db_session: Session) -> Address:
    """Create an address using factory."""
    address = AddressFactory()
    db_session.add(address)
    db_session.commit()
    db_session.refresh(address)
    return address


@pytest.fixture
def factory_order(db_session: Session) -> Order:
    """Create an order using factory."""
    order = OrderFactory()
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)
    return order


@pytest.fixture
def factory_rush_order(db_session: Session) -> Order:
    """Create a rush order using factory."""
    order = RushOrderFactory()
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)
    return order
