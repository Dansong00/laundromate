from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.models import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    
    # Address fields
    address_line_1 = Column(String(255), nullable=False)
    address_line_2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    zip_code = Column(String(20), nullable=False)
    country = Column(String(100), default="USA")
    
    # Address type and preferences
    address_type = Column(String(50), nullable=False)  # "home", "work", "pickup", "delivery"
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Additional details
    instructions = Column(Text, nullable=True)  # e.g., "Ring doorbell twice", "Leave with doorman"
    latitude = Column(String(20), nullable=True)
    longitude = Column(String(20), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    customer = relationship("Customer", back_populates="addresses")
    pickup_orders = relationship("Order", foreign_keys="Order.pickup_address_id", back_populates="pickup_address")
    delivery_orders = relationship("Order", foreign_keys="Order.delivery_address_id", back_populates="delivery_address")
