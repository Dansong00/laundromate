from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator

from .service import ServiceRead


class OrderItemBase(BaseModel):
    item_name: str
    item_type: str
    quantity: int = 1
    unit_price: float
    weight: Optional[float] = None
    special_instructions: Optional[str] = None
    fabric_type: Optional[str] = None
    color: Optional[str] = None

    @validator("quantity")
    def validate_quantity(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("quantity must be positive")
        return v

    @validator("unit_price")
    def validate_unit_price(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("unit_price must be positive")
        return v

    @validator("weight")
    def validate_weight(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("weight must be positive")
        return v


class OrderItemCreate(OrderItemBase):
    service_id: int


class OrderItemUpdate(BaseModel):
    item_name: Optional[str] = None
    item_type: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    weight: Optional[float] = None
    special_instructions: Optional[str] = None
    fabric_type: Optional[str] = None
    color: Optional[str] = None


class OrderItemRead(OrderItemBase):
    id: int
    order_id: int
    service_id: int
    total_price: float
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OrderItemWithService(OrderItemRead):
    service: ServiceRead

    class Config:
        from_attributes = True
