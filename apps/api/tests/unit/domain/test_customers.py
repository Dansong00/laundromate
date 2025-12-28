"""Unit tests for customer domain logic."""

from app.core.models.customer import Customer


class TestCustomerCreation:
    """Test customer creation logic."""

    def test_customer_creation_with_defaults(self, db_session, test_user) -> None:
        """Test that customer can be created with default values."""
        customer = Customer(
            user_id=test_user.id,
            preferred_pickup_time="morning",
            special_instructions="Ring doorbell twice",
        )
        db_session.add(customer)
        db_session.commit()

        assert customer.user_id == test_user.id
        assert customer.loyalty_points == 0
        assert customer.is_vip is False
        assert customer.email_notifications is True
        assert customer.sms_notifications is True

    def test_customer_one_to_one_with_user(self, db_session, test_user) -> None:
        """Test that customer has one-to-one relationship with user."""
        customer = Customer(
            user_id=test_user.id,
            preferred_pickup_time="afternoon",
        )
        db_session.add(customer)
        db_session.commit()

        assert customer.user is not None
        assert customer.user.id == test_user.id


class TestLoyaltyPoints:
    """Test loyalty points calculations."""

    def test_loyalty_points_initial_value(self, db_session, test_user) -> None:
        """Test that loyalty points start at 0."""
        customer = Customer(
            user_id=test_user.id,
            loyalty_points=0,
        )
        db_session.add(customer)
        db_session.commit()

        assert customer.loyalty_points == 0

    def test_loyalty_points_can_be_set(self, db_session, test_user) -> None:
        """Test that loyalty points can be set."""
        customer = Customer(
            user_id=test_user.id,
            loyalty_points=100,
        )
        db_session.add(customer)
        db_session.commit()

        assert customer.loyalty_points == 100

    def test_loyalty_points_can_be_updated(self, db_session, test_user) -> None:
        """Test that loyalty points can be updated."""
        customer = Customer(
            user_id=test_user.id,
            loyalty_points=50,
        )
        db_session.add(customer)
        db_session.commit()

        customer.loyalty_points = 150
        db_session.commit()

        assert customer.loyalty_points == 150


class TestVIPStatus:
    """Test VIP status logic."""

    def test_vip_status_default_false(self, db_session, test_user) -> None:
        """Test that VIP status defaults to False."""
        customer = Customer(
            user_id=test_user.id,
        )
        db_session.add(customer)
        db_session.commit()

        assert customer.is_vip is False

    def test_vip_status_can_be_set(self, db_session, test_user) -> None:
        """Test that VIP status can be set."""
        customer = Customer(
            user_id=test_user.id,
            is_vip=True,
        )
        db_session.add(customer)
        db_session.commit()

        assert customer.is_vip is True

    def test_vip_status_can_be_updated(self, db_session, test_user) -> None:
        """Test that VIP status can be updated."""
        customer = Customer(
            user_id=test_user.id,
            is_vip=False,
        )
        db_session.add(customer)
        db_session.commit()

        customer.is_vip = True
        db_session.commit()

        assert customer.is_vip is True


class TestCustomerPreferences:
    """Test customer preference settings."""

    def test_preferred_pickup_time(self, db_session, test_user) -> None:
        """Test that preferred pickup time can be set."""
        customer = Customer(
            user_id=test_user.id,
            preferred_pickup_time="evening",
        )
        db_session.add(customer)
        db_session.commit()

        assert customer.preferred_pickup_time == "evening"

    def test_special_instructions(self, db_session, test_user) -> None:
        """Test that special instructions can be set."""
        instructions = "Leave with doorman"
        customer = Customer(
            user_id=test_user.id,
            special_instructions=instructions,
        )
        db_session.add(customer)
        db_session.commit()

        assert customer.special_instructions == instructions

    def test_notification_preferences_defaults(self, db_session, test_user) -> None:
        """Test that notification preferences default to True."""
        customer = Customer(
            user_id=test_user.id,
        )
        db_session.add(customer)
        db_session.commit()

        assert customer.email_notifications is True
        assert customer.sms_notifications is True

    def test_notification_preferences_can_be_disabled(
        self, db_session, test_user
    ) -> None:
        """Test that notification preferences can be disabled."""
        customer = Customer(
            user_id=test_user.id,
            email_notifications=False,
            sms_notifications=False,
        )
        db_session.add(customer)
        db_session.commit()

        assert customer.email_notifications is False
        assert customer.sms_notifications is False


class TestAddressManagement:
    """Test address management for customers."""

    def test_customer_has_addresses_relationship(self, db_session, test_user) -> None:
        """Test that customer has addresses relationship."""
        from app.core.models.address import Address

        customer = Customer(
            user_id=test_user.id,
        )
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

        assert len(customer.addresses) == 1
        assert customer.addresses[0].id == address.id

    def test_customer_can_have_multiple_addresses(self, db_session, test_user) -> None:
        """Test that customer can have multiple addresses."""
        from app.core.models.address import Address

        customer = Customer(
            user_id=test_user.id,
        )
        db_session.add(customer)
        db_session.commit()

        address1 = Address(
            customer_id=customer.id,
            address_line_1="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
            address_type="home",
        )
        address2 = Address(
            customer_id=customer.id,
            address_line_1="456 Work Ave",
            city="New York",
            state="NY",
            zip_code="10002",
            address_type="work",
        )
        db_session.add(address1)
        db_session.add(address2)
        db_session.commit()

        assert len(customer.addresses) == 2
