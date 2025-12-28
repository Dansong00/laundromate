import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.models import Base


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PICKED_UP = "picked_up"
    IN_PROGRESS = "in_progress"
    READY = "ready"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    # Order details
    status: Column[OrderStatus] = Column(
        Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False
    )
    total_amount = Column(Float, nullable=False)
    tax_amount = Column(Float, default=0.0)
    tip_amount = Column(Float, default=0.0)
    final_amount = Column(Float, nullable=False)

    # Pickup details
    pickup_address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
    pickup_date = Column(DateTime(timezone=True), nullable=False)
    pickup_time_slot = Column(String(50), nullable=False)  # e.g., "9:00 AM - 11:00 AM"
    pickup_instructions = Column(Text, nullable=True)

    # Delivery details
    delivery_address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
    delivery_date = Column(DateTime(timezone=True), nullable=False)
    delivery_time_slot = Column(String(50), nullable=False)
    delivery_instructions = Column(Text, nullable=True)

    # Service preferences
    special_requests = Column(Text, nullable=True)
    is_rush_order = Column(Boolean, default=False)
    rush_fee = Column(Float, default=0.0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    picked_up_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    pickup_address = relationship(
        "Address", foreign_keys=[pickup_address_id], back_populates="pickup_orders"
    )
    delivery_address = relationship(
        "Address", foreign_keys=[delivery_address_id], back_populates="delivery_orders"
    )
    items = relationship("OrderItem", back_populates="order")
    notifications = relationship("Notification", back_populates="order")
