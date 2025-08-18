from enum import Enum

from app.core.models import Base
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class ServiceCategory(str, Enum):
    """Service categories available in the system"""
    WASH_FOLD = "wash_fold"
    DRY_CLEAN = "dry_clean"
    PRESS_ONLY = "press_only"
    STARCH = "starch"


class Service(Base):
    """Service offerings provided by the laundromat.

    This model represents the catalog of laundry services available to
    customers, including pricing, turnaround times, and service options.
    These are the services that customers can order, not individual
    service requests.

    Examples:
        - Wash & Fold service with base price + per-pound pricing
        - Dry cleaning service with flat-rate pricing
        - Press-only service with special handling requirements
    """
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)

    # Service details
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    category = Column(SQLEnum(ServiceCategory), nullable=False)

    # Pricing
    base_price = Column(Float, nullable=False)
    price_per_pound = Column(Float, nullable=True)  # For weight-based pricing
    price_per_item = Column(Float, nullable=True)   # For item-based pricing

    # Service options
    is_active = Column(Boolean, default=True)
    requires_special_handling = Column(Boolean, default=False)
    # Standard turnaround time
    turnaround_hours = Column(Integer, nullable=False)

    # Additional details
    special_instructions = Column(Text, nullable=True)
    min_order_amount = Column(Float, default=0.0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now)

    # Relationships
    order_items = relationship("OrderItem", back_populates="service")
