"""
Test data utilities for LaundroMate API tests.
"""

from typing import Dict, Any
from datetime import datetime, timedelta


def get_sample_user_data() -> Dict[str, Any]:
    """Get sample user registration data."""
    return {
        "email": "testuser@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "phone": "+1234567890"
    }


def get_sample_customer_data() -> Dict[str, Any]:
    """Get sample customer creation data."""
    return {
        "preferred_pickup_time": "morning",
        "special_instructions": "Ring doorbell twice",
        "loyalty_points": 100,
        "is_vip": False,
        "email_notifications": True,
        "sms_notifications": True
    }


def get_sample_service_data() -> Dict[str, Any]:
    """Get sample service creation data."""
    return {
        "name": "Wash & Fold",
        "description": "Standard wash and fold service",
        "category": "wash_fold",
        "base_price": 15.00,
        "price_per_pound": 2.50,
        "is_active": True,
        "requires_special_handling": False,
        "turnaround_hours": 24,
        "min_order_amount": 10.00
    }


def get_sample_address_data() -> Dict[str, Any]:
    """Get sample address creation data."""
    return {
        "address_type": "pickup",
        "street_address": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip_code": "12345",
        "country": "US",
        "is_default": True,
        "special_instructions": "Ring doorbell twice"
    }


def get_sample_order_data() -> Dict[str, Any]:
    """Get sample order creation data."""
    pickup_date = datetime.now() + timedelta(days=1)
    delivery_date = datetime.now() + timedelta(days=2)
    
    return {
        "customer_id": 1,  # Will be set in tests
        "pickup_address_id": 1,  # Will be set in tests
        "delivery_address_id": 2,  # Will be set in tests
        "pickup_date": pickup_date.isoformat(),
        "pickup_time_slot": "9:00 AM - 11:00 AM",
        "pickup_instructions": "Ring doorbell twice",
        "delivery_date": delivery_date.isoformat(),
        "delivery_time_slot": "1:00 PM - 3:00 PM",
        "delivery_instructions": "Leave at front door",
        "special_requests": "Please handle with care",
        "is_rush_order": False,
        "rush_fee": 0.0,
        "items": [
            {
                "service_id": 1,  # Will be set in tests
                "item_name": "T-Shirt",
                "item_type": "shirt",
                "quantity": 2,
                "unit_price": 5.00,
                "weight": 0.5,
                "special_instructions": "Cold wash only",
                "fabric_type": "cotton",
                "color": "blue"
            }
        ]
    }


def get_sample_order_item_data() -> Dict[str, Any]:
    """Get sample order item data."""
    return {
        "service_id": 1,  # Will be set in tests
        "item_name": "Dress Shirt",
        "item_type": "shirt",
        "quantity": 1,
        "unit_price": 8.00,
        "weight": 0.3,
        "special_instructions": "Hang dry only",
        "fabric_type": "cotton",
        "color": "white"
    }


def get_sample_notification_data() -> Dict[str, Any]:
    """Get sample notification data."""
    return {
        "customer_id": 1,  # Will be set in tests
        "order_id": 1,  # Will be set in tests
        "type": "order_confirmation",
        "title": "Order Confirmed",
        "message": "Your order has been confirmed and will be picked up tomorrow.",
        "delivery_method": "email",
        "status": "pending"
    }


def get_invalid_email_data() -> Dict[str, Any]:
    """Get invalid email data for testing validation."""
    return {
        "email": "invalid-email",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }


def get_invalid_phone_data() -> Dict[str, Any]:
    """Get invalid phone data for testing validation."""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "phone": "invalid-phone"
    }


def get_weak_password_data() -> Dict[str, Any]:
    """Get weak password data for testing validation."""
    return {
        "email": "test@example.com",
        "password": "123",  # Too short
        "first_name": "Test",
        "last_name": "User"
    }