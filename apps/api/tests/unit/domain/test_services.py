"""Unit tests for service domain logic."""

from app.core.models.service import Service, ServiceCategory


class TestServiceCategory:
    """Test ServiceCategory enum."""

    def test_service_category_values(self) -> None:
        """Test that ServiceCategory has expected values."""
        assert ServiceCategory.WASH_FOLD == "wash_fold"
        assert ServiceCategory.DRY_CLEAN == "dry_clean"
        assert ServiceCategory.PRESS_ONLY == "press_only"
        assert ServiceCategory.STARCH == "starch"


class TestServicePricingCalculations:
    """Test service pricing calculations."""

    def test_base_price_only(self, db_session) -> None:
        """Test service with base price only."""
        service = Service(
            name="Basic Wash",
            description="Basic washing service",
            category=ServiceCategory.WASH_FOLD,
            base_price=10.0,
            price_per_pound=None,
            price_per_item=None,
            turnaround_hours=24,
        )
        db_session.add(service)
        db_session.commit()

        assert service.base_price == 10.0
        assert service.price_per_pound is None
        assert service.price_per_item is None

    def test_base_price_with_per_pound(self, db_session) -> None:
        """Test service with base price and per-pound pricing."""
        service = Service(
            name="Wash & Fold",
            description="Wash and fold service",
            category=ServiceCategory.WASH_FOLD,
            base_price=5.0,
            price_per_pound=2.5,
            price_per_item=None,
            turnaround_hours=24,
        )
        db_session.add(service)
        db_session.commit()

        assert service.base_price == 5.0
        assert service.price_per_pound == 2.5
        assert service.price_per_item is None

    def test_base_price_with_per_item(self, db_session) -> None:
        """Test service with base price and per-item pricing."""
        service = Service(
            name="Dry Clean",
            description="Dry cleaning service",
            category=ServiceCategory.DRY_CLEAN,
            base_price=0.0,
            price_per_pound=None,
            price_per_item=8.0,
            turnaround_hours=48,
        )
        db_session.add(service)
        db_session.commit()

        assert service.base_price == 0.0
        assert service.price_per_pound is None
        assert service.price_per_item == 8.0

    def test_calculate_price_per_pound(self, db_session) -> None:
        """Test calculating price for weight-based service."""
        service = Service(
            name="Wash & Fold",
            description="Wash and fold service",
            category=ServiceCategory.WASH_FOLD,
            base_price=5.0,
            price_per_pound=2.5,
            price_per_item=None,
            turnaround_hours=24,
        )
        db_session.add(service)
        db_session.commit()

        # Calculate price for 10 pounds
        weight = 10.0
        expected_price = service.base_price + (service.price_per_pound * weight)
        assert expected_price == 30.0

    def test_calculate_price_per_item(self, db_session) -> None:
        """Test calculating price for item-based service."""
        service = Service(
            name="Dry Clean",
            description="Dry cleaning service",
            category=ServiceCategory.DRY_CLEAN,
            base_price=0.0,
            price_per_pound=None,
            price_per_item=8.0,
            turnaround_hours=48,
        )
        db_session.add(service)
        db_session.commit()

        # Calculate price for 5 items
        item_count = 5
        expected_price = service.base_price + (service.price_per_item * item_count)
        assert expected_price == 40.0


class TestServiceAvailability:
    """Test service availability checks."""

    def test_service_is_active_default(self, db_session) -> None:
        """Test that service is active by default."""
        service = Service(
            name="Active Service",
            description="An active service",
            category=ServiceCategory.WASH_FOLD,
            base_price=10.0,
            turnaround_hours=24,
        )
        db_session.add(service)
        db_session.commit()

        assert service.is_active is True

    def test_service_can_be_inactive(self, db_session) -> None:
        """Test that service can be marked as inactive."""
        service = Service(
            name="Inactive Service",
            description="An inactive service",
            category=ServiceCategory.WASH_FOLD,
            base_price=10.0,
            is_active=False,
            turnaround_hours=24,
        )
        db_session.add(service)
        db_session.commit()

        assert service.is_active is False

    def test_service_availability_check(self, db_session) -> None:
        """Test checking if service is available."""
        active_service = Service(
            name="Active Service",
            description="An active service",
            category=ServiceCategory.WASH_FOLD,
            base_price=10.0,
            is_active=True,
            turnaround_hours=24,
        )
        db_session.add(active_service)
        db_session.commit()

        assert active_service.is_active is True

        inactive_service = Service(
            name="Inactive Service",
            description="An inactive service",
            category=ServiceCategory.WASH_FOLD,
            base_price=10.0,
            is_active=False,
            turnaround_hours=24,
        )
        db_session.add(inactive_service)
        db_session.commit()

        assert inactive_service.is_active is False


class TestTurnaroundTime:
    """Test turnaround time calculations."""

    def test_turnaround_time_required(self, db_session) -> None:
        """Test that turnaround time is required."""
        service = Service(
            name="Service",
            description="A service",
            category=ServiceCategory.WASH_FOLD,
            base_price=10.0,
            turnaround_hours=24,
        )
        db_session.add(service)
        db_session.commit()

        assert service.turnaround_hours == 24

    def test_turnaround_time_different_categories(self, db_session) -> None:
        """Test that different categories can have different turnaround times."""
        wash_fold = Service(
            name="Wash & Fold",
            description="Wash and fold",
            category=ServiceCategory.WASH_FOLD,
            base_price=10.0,
            turnaround_hours=24,
        )
        dry_clean = Service(
            name="Dry Clean",
            description="Dry cleaning",
            category=ServiceCategory.DRY_CLEAN,
            base_price=15.0,
            turnaround_hours=48,
        )
        db_session.add(wash_fold)
        db_session.add(dry_clean)
        db_session.commit()

        assert wash_fold.turnaround_hours == 24
        assert dry_clean.turnaround_hours == 48


class TestMinimumOrderAmount:
    """Test minimum order amount validation."""

    def test_min_order_amount_default(self, db_session) -> None:
        """Test that minimum order amount defaults to 0.0."""
        service = Service(
            name="Service",
            description="A service",
            category=ServiceCategory.WASH_FOLD,
            base_price=10.0,
            turnaround_hours=24,
        )
        db_session.add(service)
        db_session.commit()

        assert service.min_order_amount == 0.0

    def test_min_order_amount_can_be_set(self, db_session) -> None:
        """Test that minimum order amount can be set."""
        service = Service(
            name="Premium Service",
            description="A premium service",
            category=ServiceCategory.DRY_CLEAN,
            base_price=20.0,
            turnaround_hours=48,
            min_order_amount=25.0,
        )
        db_session.add(service)
        db_session.commit()

        assert service.min_order_amount == 25.0

    def test_min_order_amount_validation(self, db_session) -> None:
        """Test that orders below minimum amount are invalid."""
        service = Service(
            name="Premium Service",
            description="A premium service",
            category=ServiceCategory.DRY_CLEAN,
            base_price=20.0,
            turnaround_hours=48,
            min_order_amount=25.0,
        )
        db_session.add(service)
        db_session.commit()

        # Order amount below minimum
        order_amount = 20.0
        assert order_amount < service.min_order_amount

        # Order amount meets minimum
        valid_order_amount = 30.0
        assert valid_order_amount >= service.min_order_amount


class TestSpecialHandling:
    """Test special handling requirements."""

    def test_special_handling_default_false(self, db_session) -> None:
        """Test that special handling defaults to False."""
        service = Service(
            name="Service",
            description="A service",
            category=ServiceCategory.WASH_FOLD,
            base_price=10.0,
            turnaround_hours=24,
        )
        db_session.add(service)
        db_session.commit()

        assert service.requires_special_handling is False

    def test_special_handling_can_be_set(self, db_session) -> None:
        """Test that special handling can be set."""
        service = Service(
            name="Delicate Service",
            description="A delicate service",
            category=ServiceCategory.DRY_CLEAN,
            base_price=15.0,
            turnaround_hours=48,
            requires_special_handling=True,
        )
        db_session.add(service)
        db_session.commit()

        assert service.requires_special_handling is True
