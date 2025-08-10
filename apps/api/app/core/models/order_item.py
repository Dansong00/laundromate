from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.models import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)

    # Item details
    item_name = Column(String(255), nullable=False)
    item_type = Column(String(100), nullable=False)  # e.g., "shirt", "pants", "dress", "bedding"
    quantity = Column(Integer, nullable=False, default=1)

    # Pricing
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

    # Service-specific details
    weight = Column(Float, nullable=True)  # in pounds
    special_instructions = Column(Text, nullable=True)
    fabric_type = Column(String(100), nullable=True)
    color = Column(String(50), nullable=True)

    # Status tracking
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    order = relationship("Order", back_populates="items")
    service = relationship("Service", back_populates="order_items")
