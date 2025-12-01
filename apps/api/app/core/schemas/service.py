from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    base_price: float
    price_per_pound: Optional[float] = None
    price_per_item: Optional[float] = None
    is_active: bool = True
    requires_special_handling: bool = False
    turnaround_hours: int
    special_instructions: Optional[str] = None
    min_order_amount: float = 0.0

    @validator("category")
    def validate_category(cls, v):
        valid_categories = ["wash_fold", "dry_clean", "press_only", "starch"]
        if v not in valid_categories:
            raise ValueError(f"category must be one of {valid_categories}")
        return v

    @validator("base_price", "price_per_pound", "price_per_item", "min_order_amount")
    def validate_positive_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("price must be non-negative")
        return v

    @validator("turnaround_hours")
    def validate_turnaround_hours(cls, v):
        if v <= 0:
            raise ValueError("turnaround_hours must be positive")
        return v


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    base_price: Optional[float] = None
    price_per_pound: Optional[float] = None
    price_per_item: Optional[float] = None
    is_active: Optional[bool] = None
    requires_special_handling: Optional[bool] = None
    turnaround_hours: Optional[int] = None
    special_instructions: Optional[str] = None
    min_order_amount: Optional[float] = None


class ServiceRead(ServiceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
