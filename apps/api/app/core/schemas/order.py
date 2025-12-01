from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, validator

from .address import AddressRead
from .customer import CustomerRead
from .order_item import OrderItemCreate, OrderItemRead


class OrderBase(BaseModel):
    pickup_date: datetime
    pickup_time_slot: str
    pickup_instructions: Optional[str] = None
    delivery_date: datetime
    delivery_time_slot: str
    delivery_instructions: Optional[str] = None
    special_requests: Optional[str] = None
    is_rush_order: bool = False
    rush_fee: float = 0.0

    @validator("delivery_date")
    def validate_delivery_after_pickup(cls, v, values):
        if "pickup_date" in values and v <= values["pickup_date"]:
            raise ValueError("delivery_date must be after pickup_date")
        return v

    @validator("rush_fee")
    def validate_rush_fee(cls, v, values):
        if values.get("is_rush_order", False) and v <= 0:
            raise ValueError("rush_fee must be positive for rush orders")
        return v


class OrderCreate(OrderBase):
    customer_id: int
    pickup_address_id: int
    delivery_address_id: int
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    pickup_date: Optional[datetime] = None
    pickup_time_slot: Optional[str] = None
    pickup_instructions: Optional[str] = None
    delivery_date: Optional[datetime] = None
    delivery_time_slot: Optional[str] = None
    delivery_instructions: Optional[str] = None
    special_requests: Optional[str] = None
    is_rush_order: Optional[bool] = None
    rush_fee: Optional[float] = None


class OrderRead(OrderBase):
    id: int
    order_number: str
    customer_id: int
    status: str
    total_amount: float
    tax_amount: float
    tip_amount: float
    final_amount: float
    pickup_address_id: int
    delivery_address_id: int
    created_at: datetime
    updated_at: datetime
    picked_up_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OrderWithDetails(OrderRead):
    customer: CustomerRead
    pickup_address: AddressRead
    delivery_address: AddressRead
    items: List[OrderItemRead] = []

    class Config:
        from_attributes = True


class OrderSummary(BaseModel):
    id: int
    order_number: str
    status: str
    total_amount: float
    pickup_date: datetime
    delivery_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True
