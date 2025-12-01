from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class NotificationBase(BaseModel):
    type: str
    title: str
    message: str
    delivery_method: str

    @validator("type")
    def validate_type(cls, v):
        valid_types = [
            "order_confirmation",
            "pickup_reminder",
            "order_ready",
            "out_for_delivery",
            "delivery_confirmation",
            "order_status_update",
            "promotional",
        ]
        if v not in valid_types:
            raise ValueError(f"type must be one of {valid_types}")
        return v

    @validator("delivery_method")
    def validate_delivery_method(cls, v):
        valid_methods = ["email", "sms", "push", "in_app"]
        if v not in valid_methods:
            raise ValueError(f"delivery_method must be one of {valid_methods}")
        return v


class NotificationCreate(NotificationBase):
    customer_id: int
    order_id: Optional[int] = None


class NotificationUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    delivery_method: Optional[str] = None


class NotificationRead(NotificationBase):
    id: int
    customer_id: int
    order_id: Optional[int] = None
    status: str
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    external_id: Optional[str] = None
    retry_count: int
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotificationStatusUpdate(BaseModel):
    status: str

    @validator("status")
    def validate_status(cls, v):
        valid_statuses = ["pending", "sent", "delivered", "failed", "read"]
        if v not in valid_statuses:
            raise ValueError(f"status must be one of {valid_statuses}")
        return v
