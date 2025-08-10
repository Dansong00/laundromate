from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.models import Base
import enum


class NotificationType(str, enum.Enum):
    ORDER_CONFIRMATION = "order_confirmation"
    PICKUP_REMINDER = "pickup_reminder"
    ORDER_READY = "order_ready"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERY_CONFIRMATION = "delivery_confirmation"
    ORDER_STATUS_UPDATE = "order_status_update"
    PROMOTIONAL = "promotional"


class NotificationStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    READ = "read"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)  # Optional for promotional notifications
    
    # Notification details
    type = Column(Enum(NotificationType), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    
    # Delivery details
    status = Column(Enum(NotificationStatus), default=NotificationStatus.PENDING, nullable=False)
    delivery_method = Column(String(50), nullable=False)  # "email", "sms", "push", "in_app"
    
    # Tracking
    sent_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    read_at = Column(DateTime(timezone=True), nullable=True)
    
    # Metadata
    external_id = Column(String(255), nullable=True)  # For tracking with external services (Twilio, SendGrid)
    retry_count = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    customer = relationship("Customer", back_populates="notifications")
    order = relationship("Order", back_populates="notifications")
