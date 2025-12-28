"""Unit tests for OrderItem model."""
import pytest
from sqlalchemy.exc import IntegrityError

from app.core.models.order_item import OrderItem


class TestOrderItemModelCreation:
    """Test OrderItem model creation."""

    def test_order_item_creation_with_required_fields(
        self, db_session, test_service, test_customer
    ) -> None:
        """Test that order item can be created with required fields."""
        from datetime import datetime, timedelta, timezone

        from app.core.models.address import Address
        from app.core.models.order import Order, OrderStatus

        customer = test_customer

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
            order_number="ORD-134",
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
            service_id=test_service.id,
            item_name="Shirts",
            item_type="shirt",
            quantity=5,
            unit_price=10.0,
            total_price=50.0,
        )
        db_session.add(item)
        db_session.commit()

        assert item.id is not None
        assert item.order_id == order.id
        assert item.service_id == test_service.id
        assert item.item_name == "Shirts"
        assert item.quantity == 5
        assert item.unit_price == 10.0
        assert item.total_price == 50.0

    def test_order_item_creation_with_all_fields(
        self, db_session, test_service, test_customer
    ) -> None:
        """Test that order item can be created with all fields."""
        from datetime import datetime, timedelta, timezone

        from app.core.models.address import Address
        from app.core.models.order import Order, OrderStatus

        customer = test_customer

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
            order_number="ORD-135",
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
            service_id=test_service.id,
            item_name="Dress",
            item_type="dress",
            quantity=1,
            unit_price=25.0,
            total_price=25.0,
            weight=2.5,
            special_instructions="Handle with care",
            fabric_type="silk",
            color="blue",
        )
        db_session.add(item)
        db_session.commit()

        assert item.weight == 2.5
        assert item.special_instructions == "Handle with care"
        assert item.fabric_type == "silk"
        assert item.color == "blue"


class TestOrderItemConstraints:
    """Test OrderItem model constraints."""

    def test_order_item_order_id_is_required(self, db_session, test_service) -> None:
        """Test that order_id is required."""
        item = OrderItem(
            service_id=test_service.id,
            item_name="Shirts",
            item_type="shirt",
            quantity=5,
            unit_price=10.0,
            total_price=50.0,
        )
        db_session.add(item)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_order_item_service_id_is_required(self, db_session) -> None:
        """Test that service_id is required."""
        from datetime import datetime, timedelta, timezone

        from app.core.models.address import Address
        from app.core.models.customer import Customer
        from app.core.models.order import Order, OrderStatus
        from app.core.models.user import User

        user = User(phone="+1234567892")
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
            order_number="ORD-136",
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
            item_name="Shirts",
            item_type="shirt",
            quantity=5,
            unit_price=10.0,
            total_price=50.0,
        )
        db_session.add(item)
        with pytest.raises(IntegrityError):
            db_session.commit()


class TestOrderItemDefaults:
    """Test OrderItem model defaults."""

    def test_order_item_quantity_default(self, db_session, test_service) -> None:
        """Test that quantity defaults to 1."""
        from datetime import datetime, timedelta, timezone

        from app.core.models.address import Address
        from app.core.models.customer import Customer
        from app.core.models.order import Order, OrderStatus
        from app.core.models.user import User

        user = User(phone="+1234567893")
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
            order_number="ORD-137",
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
            service_id=test_service.id,
            item_name="Shirts",
            item_type="shirt",
            unit_price=10.0,
            total_price=10.0,
        )
        db_session.add(item)
        db_session.commit()

        assert item.quantity == 1

    def test_order_item_is_completed_default(self, db_session, test_service) -> None:
        """Test that is_completed defaults to False."""
        from datetime import datetime, timedelta, timezone

        from app.core.models.address import Address
        from app.core.models.customer import Customer
        from app.core.models.order import Order, OrderStatus
        from app.core.models.user import User

        user = User(phone="+1234567894")
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
            order_number="ORD-138",
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
            service_id=test_service.id,
            item_name="Shirts",
            item_type="shirt",
            quantity=5,
            unit_price=10.0,
            total_price=50.0,
        )
        db_session.add(item)
        db_session.commit()

        assert item.is_completed is False


class TestOrderItemRelationships:
    """Test OrderItem model relationships."""

    def test_order_item_has_order_relationship(self, db_session, test_service) -> None:
        """Test that order item has order relationship."""
        from datetime import datetime, timedelta, timezone

        from app.core.models.address import Address
        from app.core.models.customer import Customer
        from app.core.models.order import Order, OrderStatus
        from app.core.models.user import User

        user = User(phone="+1234567895")
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
            order_number="ORD-139",
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
            service_id=test_service.id,
            item_name="Shirts",
            item_type="shirt",
            quantity=5,
            unit_price=10.0,
            total_price=50.0,
        )
        db_session.add(item)
        db_session.commit()

        assert item.order is not None
        assert item.order.id == order.id

    def test_order_item_has_service_relationship(
        self, db_session, test_service
    ) -> None:
        """Test that order item has service relationship."""
        from datetime import datetime, timedelta, timezone

        from app.core.models.address import Address
        from app.core.models.customer import Customer
        from app.core.models.order import Order, OrderStatus
        from app.core.models.user import User

        user = User(phone="+1234567896")
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
            order_number="ORD-140",
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
            service_id=test_service.id,
            item_name="Shirts",
            item_type="shirt",
            quantity=5,
            unit_price=10.0,
            total_price=50.0,
        )
        db_session.add(item)
        db_session.commit()

        assert item.service is not None
        assert item.service.id == test_service.id


class TestOrderItemTimestamps:
    """Test OrderItem model timestamps."""

    def test_order_item_has_created_at(self, db_session, test_service) -> None:
        """Test that order item has created_at timestamp."""
        from datetime import datetime, timedelta, timezone

        from app.core.models.address import Address
        from app.core.models.customer import Customer
        from app.core.models.order import Order, OrderStatus
        from app.core.models.user import User

        user = User(phone="+1234567897")
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
            order_number="ORD-141",
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
            service_id=test_service.id,
            item_name="Shirts",
            item_type="shirt",
            quantity=5,
            unit_price=10.0,
            total_price=50.0,
        )
        db_session.add(item)
        db_session.commit()

        assert item.created_at is not None
