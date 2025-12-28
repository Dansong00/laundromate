"""Unit tests for Pydantic schema validation."""
import pytest
from pydantic import ValidationError

from app.core.schemas.service import ServiceBase, ServiceCreate, ServiceUpdate
from app.core.schemas.user import (
    OTPRequest,
    OTPVerify,
    UserCreate,
    UserCreateByAdmin,
    UserRead,
    UserUpdate,
)


class TestServiceSchemaValidation:
    """Test Service schema validation."""

    def test_service_base_valid_data(self) -> None:
        """Test that ServiceBase accepts valid data."""
        service_data = {
            "name": "Wash & Fold",
            "description": "Wash and fold service",
            "category": "wash_fold",
            "base_price": 10.0,
            "price_per_pound": 2.5,
            "turnaround_hours": 24,
        }
        service = ServiceBase(**service_data)
        assert service.name == "Wash & Fold"
        assert service.category == "wash_fold"
        assert service.base_price == 10.0

    def test_service_base_invalid_category(self) -> None:
        """Test that ServiceBase rejects invalid category."""
        service_data = {
            "name": "Service",
            "category": "invalid_category",
            "base_price": 10.0,
            "turnaround_hours": 24,
        }
        with pytest.raises(ValidationError) as exc_info:
            ServiceBase(**service_data)
        assert "category must be one of" in str(exc_info.value)

    def test_service_base_valid_categories(self) -> None:
        """Test that ServiceBase accepts all valid categories."""
        valid_categories = ["wash_fold", "dry_clean", "press_only", "starch"]
        for category in valid_categories:
            service_data = {
                "name": f"Service {category}",
                "category": category,
                "base_price": 10.0,
                "turnaround_hours": 24,
            }
            service = ServiceBase(**service_data)
            assert service.category == category

    def test_service_base_negative_price(self) -> None:
        """Test that ServiceBase rejects negative prices."""
        service_data = {
            "name": "Service",
            "category": "wash_fold",
            "base_price": -10.0,
            "turnaround_hours": 24,
        }
        with pytest.raises(ValidationError) as exc_info:
            ServiceBase(**service_data)
        assert "price must be non-negative" in str(exc_info.value)

    def test_service_base_zero_price_allowed(self) -> None:
        """Test that ServiceBase allows zero price."""
        service_data = {
            "name": "Free Service",
            "category": "wash_fold",
            "base_price": 0.0,
            "turnaround_hours": 24,
        }
        service = ServiceBase(**service_data)
        assert service.base_price == 0.0

    def test_service_base_invalid_turnaround_hours(self) -> None:
        """Test that ServiceBase rejects invalid turnaround hours."""
        service_data = {
            "name": "Service",
            "category": "wash_fold",
            "base_price": 10.0,
            "turnaround_hours": 0,
        }
        with pytest.raises(ValidationError):
            ServiceBase(**service_data)

    def test_service_base_negative_turnaround_hours(self) -> None:
        """Test that ServiceBase rejects negative turnaround hours."""
        service_data = {
            "name": "Service",
            "category": "wash_fold",
            "base_price": 10.0,
            "turnaround_hours": -1,
        }
        with pytest.raises(ValidationError):
            ServiceBase(**service_data)

    def test_service_create_inherits_base(self) -> None:
        """Test that ServiceCreate inherits from ServiceBase."""
        service_data = {
            "name": "Wash & Fold",
            "category": "wash_fold",
            "base_price": 10.0,
            "turnaround_hours": 24,
        }
        service = ServiceCreate(**service_data)
        assert isinstance(service, ServiceBase)

    def test_service_update_all_fields_optional(self) -> None:
        """Test that ServiceUpdate makes all fields optional."""
        # Empty update should be valid
        update = ServiceUpdate()
        assert update.name is None
        assert update.category is None

    def test_service_update_partial_update(self) -> None:
        """Test that ServiceUpdate allows partial updates."""
        update = ServiceUpdate(name="Updated Name")
        assert update.name == "Updated Name"
        assert update.category is None
        assert update.base_price is None


class TestUserSchemaValidation:
    """Test User schema validation."""

    def test_user_create_requires_phone(self) -> None:
        """Test that UserCreate requires phone."""
        user_data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
        }
        with pytest.raises(ValidationError):
            UserCreate(**user_data)

    def test_user_create_with_phone(self) -> None:
        """Test that UserCreate accepts phone."""
        user_data = {"phone": "+1234567890"}
        user = UserCreate(**user_data)
        assert user.phone == "+1234567890"

    def test_user_create_optional_fields(self) -> None:
        """Test that UserCreate has optional fields."""
        user_data = {
            "phone": "+1234567890",
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
        }
        user = UserCreate(**user_data)
        assert user.email == "test@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"

    def test_user_create_by_admin_all_fields(self) -> None:
        """Test that UserCreateByAdmin has all fields."""
        user_data = {
            "phone": "+1234567890",
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "is_admin": True,
            "is_super_admin": False,
            "is_active": True,
        }
        user = UserCreateByAdmin(**user_data)
        assert user.phone == "+1234567890"
        assert user.is_admin is True
        assert user.is_super_admin is False
        assert user.is_active is True

    def test_user_create_by_admin_defaults(self) -> None:
        """Test that UserCreateByAdmin has correct defaults."""
        user_data = {"phone": "+1234567890"}
        user = UserCreateByAdmin(**user_data)
        assert user.is_admin is False
        assert user.is_super_admin is False
        assert user.is_active is True

    def test_user_update_all_fields_optional(self) -> None:
        """Test that UserUpdate makes all fields optional."""
        update = UserUpdate()
        assert update.email is None
        assert update.phone is None
        assert update.is_admin is None

    def test_user_update_partial_update(self) -> None:
        """Test that UserUpdate allows partial updates."""
        update = UserUpdate(email="new@example.com")
        assert update.email == "new@example.com"
        assert update.phone is None


class TestOTPSchemaValidation:
    """Test OTP schema validation."""

    def test_otp_request_requires_phone(self) -> None:
        """Test that OTPRequest requires phone."""
        with pytest.raises(ValidationError):
            OTPRequest()

    def test_otp_request_with_phone(self) -> None:
        """Test that OTPRequest accepts phone."""
        otp_request = OTPRequest(phone="+1234567890")
        assert otp_request.phone == "+1234567890"

    def test_otp_verify_requires_phone_and_code(self) -> None:
        """Test that OTPVerify requires both phone and code."""
        with pytest.raises(ValidationError):
            OTPVerify()

        with pytest.raises(ValidationError):
            OTPVerify(phone="+1234567890")

        with pytest.raises(ValidationError):
            OTPVerify(code="123456")

    def test_otp_verify_with_phone_and_code(self) -> None:
        """Test that OTPVerify accepts phone and code."""
        otp_verify = OTPVerify(phone="+1234567890", code="123456")
        assert otp_verify.phone == "+1234567890"
        assert otp_verify.code == "123456"


class TestSchemaSerialization:
    """Test schema serialization and deserialization."""

    def test_service_base_serialization(self) -> None:
        """Test that ServiceBase can be serialized to dict."""
        service = ServiceBase(
            name="Wash & Fold",
            category="wash_fold",
            base_price=10.0,
            turnaround_hours=24,
        )
        service_dict = service.dict()
        assert service_dict["name"] == "Wash & Fold"
        assert service_dict["category"] == "wash_fold"
        assert service_dict["base_price"] == 10.0

    def test_service_base_json_serialization(self) -> None:
        """Test that ServiceBase can be serialized to JSON."""
        service = ServiceBase(
            name="Wash & Fold",
            category="wash_fold",
            base_price=10.0,
            turnaround_hours=24,
        )
        service_json = service.json()
        assert "Wash & Fold" in service_json
        assert "wash_fold" in service_json

    def test_user_read_from_attributes(self) -> None:
        """Test that UserRead can be created from attributes."""
        from datetime import datetime, timezone
        from uuid import uuid4

        user_id = uuid4()
        user_data = {
            "id": user_id,
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567890",
            "is_active": True,
            "is_admin": False,
            "is_super_admin": False,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        user = UserRead(**user_data)
        assert user.id == user_id
        assert user.email == "test@example.com"
