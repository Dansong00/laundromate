from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.models import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    
    # Service details
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False)  # "wash_fold", "dry_clean", "press_only", "starch"
    
    # Pricing
    base_price = Column(Float, nullable=False)
    price_per_pound = Column(Float, nullable=True)  # For weight-based pricing
    price_per_item = Column(Float, nullable=True)   # For item-based pricing
    
    # Service options
    is_active = Column(Boolean, default=True)
    requires_special_handling = Column(Boolean, default=False)
    turnaround_hours = Column(Integer, nullable=False)  # Standard turnaround time
    
    # Additional details
    special_instructions = Column(Text, nullable=True)
    min_order_amount = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    order_items = relationship("OrderItem", back_populates="service")
