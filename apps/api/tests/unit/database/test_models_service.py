"""Unit tests for Service model."""
import pytest
from sqlalchemy.exc import IntegrityError

from app.core.models.service import Service, ServiceCategory


class TestServiceModelCreation:
    """Test Service model creation."""

    def test_service_creation_with_required_fields(self, db_session) -> None:
        """Test that service can be created with required fields."""
        service = Service(
            name="Wash & Fold",
            description="Wash and fold service",
            category=ServiceCategory.WASH_FOLD,
            base_price=10.0,
            turnaround_hours=24,
        )
        db_session.add(service)
        db_session.commit()

        assert service.id is not None
        assert service.name == "Wash & Fold"
        assert service.category == ServiceCategory.WASH_FOLD
        assert service.base_price == 10.0
        assert service.turnaround_hours == 24

    def test_service_creation_with_all_fields(self, db_session) -> None:
        """Test that service can be created with all fields."""
        service = Service(
            name="Dry Clean",
            description="Professional dry cleaning",
            category=ServiceCategory.DRY_CLEAN,
            base_price=15.0,
            price_per_pound=None,
            price_per_item=8.0,
            is_active=True,
            requires_special_handling=True,
            turnaround_hours=48,
            special_instructions="Handle with care",
            min_order_amount=20.0,
        )
        db_session.add(service)
        db_session.commit()

        assert service.price_per_item == 8.0
        assert service.is_active is True
        assert service.requires_special_handling is True
        assert service.min_order_amount == 20.0


class TestServiceCategoryEnum:
    """Test ServiceCategory enum."""

    def test_service_category_enum_values(self) -> None:
        """Test that ServiceCategory enum has all expected values."""
        assert ServiceCategory.WASH_FOLD == "wash_fold"
        assert ServiceCategory.DRY_CLEAN == "dry_clean"
        assert ServiceCategory.PRESS_ONLY == "press_only"
        assert ServiceCategory.STARCH == "starch"


class TestServiceConstraints:
    """Test Service model constraints."""

    def test_service_name_is_required(self, db_session) -> None:
        """Test that name is required."""
        service = Service(
            category=ServiceCategory.WASH_FOLD,
            base_price=10.0,
            turnaround_hours=24,
        )
        db_session.add(service)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_service_name_unique(self, db_session) -> None:
        """Test that name must be unique."""
        service1 = Service(
            name="Wash & Fold",
            category=ServiceCategory.WASH_FOLD,
            base_price=10.0,
            turnaround_hours=24,
        )
        service2 = Service(
            name="Wash & Fold",
            category=ServiceCategory.WASH_FOLD,
            base_price=12.0,
            turnaround_hours=24,
        )
        db_session.add(service1)
        db_session.commit()

        db_session.add(service2)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_service_category_is_required(self, db_session) -> None:
        """Test that category is required."""
        service = Service(
            name="Service",
            base_price=10.0,
            turnaround_hours=24,
        )
        db_session.add(service)
        with pytest.raises(IntegrityError):
            db_session.commit()


class TestServiceDefaults:
    """Test Service model defaults."""

    def test_service_is_active_default(self, db_session) -> None:
        """Test that is_active defaults to True."""
        service = Service(
            name="Service",
            category=ServiceCategory.WASH_FOLD,
            base_price=10.0,
            turnaround_hours=24,
        )
        db_session.add(service)
        db_session.commit()

        assert service.is_active is True

    def test_service_requires_special_handling_default(self, db_session) -> None:
        """Test that requires_special_handling defaults to False."""
        service = Service(
            name="Service",
            category=ServiceCategory.WASH_FOLD,
            base_price=10.0,
            turnaround_hours=24,
        )
        db_session.add(service)
        db_session.commit()

        assert service.requires_special_handling is False

    def test_service_min_order_amount_default(self, db_session) -> None:
        """Test that min_order_amount defaults to 0.0."""
        service = Service(
            name="Service",
            category=ServiceCategory.WASH_FOLD,
            base_price=10.0,
            turnaround_hours=24,
        )
        db_session.add(service)
        db_session.commit()

        assert service.min_order_amount == 0.0


class TestServiceRelationships:
    """Test Service model relationships."""

    def test_service_has_order_items_relationship(self, db_session) -> None:
        """Test that service has order_items relationship."""
        from datetime import datetime, timedelta, timezone

        from app.core.models.order import Order, OrderStatus
        from app.core.models.order_item import OrderItem

        service = Service(
            name="Wash & Fold",
            category=ServiceCategory.WASH_FOLD,
            base_price=10.0,
            turnaround_hours=24,
        )
        db_session.add(service)
        db_session.commit()

        # Create a customer and order for the relationship
        from app.core.models.address import Address
        from app.core.models.customer import Customer
        from app.core.models.user import User

        user = User(phone="+1234567890")
        db_session.add(user)
        db_session.commit()

        customer = Customer(user_id=user.id)
        db_session.add(customer)
        db_session.commit()

        address = Address(
            customer_id=customer.id,
            address_line_1="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
            address_type="home",
        )
        db_session.add(address)
        db_session.commit()

        order = Order(
            order_number="ORD-131",
            customer_id=customer.id,
            status=OrderStatus.PENDING,
            total_amount=50.0,
            final_amount=50.0,
            pickup_address_id=address.id,
            pickup_date=datetime.now(timezone.utc),
            pickup_time_slot="9:00 AM - 11:00 AM",
            delivery_address_id=address.id,
            delivery_date=datetime.now(timezone.utc) + timedelta(days=1),
            delivery_time_slot="2:00 PM - 4:00 PM",
        )
        db_session.add(order)
        db_session.commit()

        item = OrderItem(
            order_id=order.id,
            service_id=service.id,
            item_name="Shirts",
            item_type="shirt",
            quantity=5,
            unit_price=10.0,
            total_price=50.0,
        )
        db_session.add(item)
        db_session.commit()

        assert len(service.order_items) == 1
        assert service.order_items[0].id == item.id


class TestServiceTimestamps:
    """Test Service model timestamps."""

    def test_service_has_created_at(self, db_session) -> None:
        """Test that service has created_at timestamp."""
        service = Service(
            name="Service",
            category=ServiceCategory.WASH_FOLD,
            base_price=10.0,
            turnaround_hours=24,
        )
        db_session.add(service)
        db_session.commit()

        assert service.created_at is not None

    def test_service_has_updated_at(self, db_session) -> None:
        """Test that service has updated_at timestamp."""
        service = Service(
            name="Service",
            category=ServiceCategory.WASH_FOLD,
            base_price=10.0,
            turnaround_hours=24,
        )
        db_session.add(service)
        db_session.commit()

        assert service.updated_at is not None

    def test_service_updated_at_changes_on_update(self, db_session) -> None:
        """Test that updated_at changes when service is updated."""
        service = Service(
            name="Service",
            category=ServiceCategory.WASH_FOLD,
            base_price=10.0,
            turnaround_hours=24,
        )
        db_session.add(service)
        db_session.commit()

        original_updated_at = service.updated_at
        service.base_price = 12.0
        db_session.commit()

        assert service.updated_at != original_updated_at
