"""
Custom assertions for LaundroMate API tests.
"""

from typing import Dict, Any, List
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.models.user import User
from app.core.models.customer import Customer
from app.core.models.order import Order
from app.core.models.service import Service
from app.core.models.address import Address


def assert_user_response_valid(response_data: Dict[str, Any]) -> None:
    """Assert that user response data is valid."""
    required_fields = ["id", "email", "first_name", "last_name", "is_active", "is_admin"]
    for field in required_fields:
        assert field in response_data, f"Missing required field: {field}"
    
    # Should not expose sensitive data
    assert "hashed_password" not in response_data
    assert "password" not in response_data


def assert_customer_response_valid(response_data: Dict[str, Any]) -> None:
    """Assert that customer response data is valid."""
    required_fields = ["id", "user_id", "loyalty_points", "is_vip", "email_notifications", "sms_notifications"]
    for field in required_fields:
        assert field in response_data, f"Missing required field: {field}"


def assert_order_response_valid(response_data: Dict[str, Any]) -> None:
    """Assert that order response data is valid."""
    required_fields = ["id", "order_number", "customer_id", "status", "total_amount", "final_amount"]
    for field in required_fields:
        assert field in response_data, f"Missing required field: {field}"
    
    # Validate order number format
    assert response_data["order_number"].startswith("ORD-")


def assert_service_response_valid(response_data: Dict[str, Any]) -> None:
    """Assert that service response data is valid."""
    required_fields = ["id", "name", "description", "category", "base_price", "is_active"]
    for field in required_fields:
        assert field in response_data, f"Missing required field: {field}"


def assert_address_response_valid(response_data: Dict[str, Any]) -> None:
    """Assert that address response data is valid."""
    required_fields = ["id", "customer_id", "address_type", "street_address", "city", "state", "zip_code"]
    for field in required_fields:
        assert field in response_data, f"Missing required field: {field}"


def assert_order_totals_correct(order_data: Dict[str, Any], expected_total: float) -> None:
    """Assert that order totals are calculated correctly."""
    assert order_data["total_amount"] == expected_total
    assert order_data["final_amount"] == (
        expected_total + 
        order_data.get("tax_amount", 0.0) + 
        order_data.get("rush_fee", 0.0)
    )


def assert_pagination_response_valid(response_data: Dict[str, Any], expected_count: int = None) -> None:
    """Assert that paginated response data is valid."""
    assert "items" in response_data
    assert isinstance(response_data["items"], list)
    
    if expected_count is not None:
        assert len(response_data["items"]) == expected_count


def assert_error_response_valid(response_data: Dict[str, Any], expected_status: int = None) -> None:
    """Assert that error response data is valid."""
    assert "detail" in response_data
    assert isinstance(response_data["detail"], str)
    assert len(response_data["detail"]) > 0


def assert_user_in_database(db: Session, email: str, should_exist: bool = True) -> None:
    """Assert that user exists or doesn't exist in database."""
    user = db.query(User).filter(User.email == email).first()
    if should_exist:
        assert user is not None, f"User with email {email} should exist in database"
        assert user.email == email
    else:
        assert user is None, f"User with email {email} should not exist in database"


def assert_customer_in_database(db: Session, user_id: str, should_exist: bool = True) -> None:
    """Assert that customer exists or doesn't exist in database."""
    customer = db.query(Customer).filter(Customer.user_id == user_id).first()
    if should_exist:
        assert customer is not None, f"Customer with user_id {user_id} should exist in database"
        assert customer.user_id == user_id
    else:
        assert customer is None, f"Customer with user_id {user_id} should not exist in database"


def assert_order_in_database(db: Session, order_number: str, should_exist: bool = True) -> None:
    """Assert that order exists or doesn't exist in database."""
    order = db.query(Order).filter(Order.order_number == order_number).first()
    if should_exist:
        assert order is not None, f"Order with number {order_number} should exist in database"
        assert order.order_number == order_number
    else:
        assert order is None, f"Order with number {order_number} should not exist in database"


def assert_service_in_database(db: Session, name: str, should_exist: bool = True) -> None:
    """Assert that service exists or doesn't exist in database."""
    service = db.query(Service).filter(Service.name == name).first()
    if should_exist:
        assert service is not None, f"Service with name {name} should exist in database"
        assert service.name == name
    else:
        assert service is None, f"Service with name {name} should not exist in database"


def assert_address_in_database(db: Session, address_id: int, should_exist: bool = True) -> None:
    """Assert that address exists or doesn't exist in database."""
    address = db.query(Address).filter(Address.id == address_id).first()
    if should_exist:
        assert address is not None, f"Address with id {address_id} should exist in database"
        assert address.id == address_id
    else:
        assert address is None, f"Address with id {address_id} should not exist in database"


def assert_authorization_required(client: TestClient, method: str, url: str, data: Dict[str, Any] = None) -> None:
    """Assert that endpoint requires authorization."""
    if method.upper() == "GET":
        response = client.get(url)
    elif method.upper() == "POST":
        response = client.post(url, json=data or {})
    elif method.upper() == "PUT":
        response = client.put(url, json=data or {})
    elif method.upper() == "DELETE":
        response = client.delete(url)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")
    
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
    assert "detail" in response.json()


def assert_admin_required(client: TestClient, method: str, url: str, headers: Dict[str, str], data: Dict[str, Any] = None) -> None:
    """Assert that endpoint requires admin privileges."""
    if method.upper() == "GET":
        response = client.get(url, headers=headers)
    elif method.upper() == "POST":
        response = client.post(url, json=data or {}, headers=headers)
    elif method.upper() == "PUT":
        response = client.put(url, json=data or {}, headers=headers)
    elif method.upper() == "DELETE":
        response = client.delete(url, headers=headers)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")
    
    assert response.status_code == 403, f"Expected 403 Forbidden, got {response.status_code}"
    assert "detail" in response.json()