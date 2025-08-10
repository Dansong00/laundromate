from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.models import Base
from sqlalchemy.dialects.postgresql import UUID


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)

    # Customer-specific fields
    preferred_pickup_time = Column(String(50), nullable=True)  # e.g., "morning", "afternoon", "evening"
    special_instructions = Column(Text, nullable=True)
    loyalty_points = Column(Integer, default=0)
    is_vip = Column(Boolean, default=False)

    # Contact preferences
    email_notifications = Column(Boolean, default=True)
    sms_notifications = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="customer")
    addresses = relationship("Address", back_populates="customer")
    orders = relationship("Order", back_populates="customer")
