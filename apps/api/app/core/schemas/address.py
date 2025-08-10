from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class AddressBase(BaseModel):
    address_line_1: str
    address_line_2: Optional[str] = None
    city: str
    state: str
    zip_code: str
    country: str = "USA"
    address_type: str
    is_default: bool = False
    is_active: bool = True
    instructions: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None

    @validator('address_type')
    def validate_address_type(cls, v):
        valid_types = ["home", "work", "pickup", "delivery"]
        if v not in valid_types:
            raise ValueError(f'address_type must be one of {valid_types}')
        return v

    @validator('zip_code')
    def validate_zip_code(cls, v):
        if not v.isdigit() or len(v) != 5:
            raise ValueError('zip_code must be 5 digits')
        return v


class AddressCreate(AddressBase):
    customer_id: int


class AddressUpdate(BaseModel):
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    address_type: Optional[str] = None
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None
    instructions: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None


class AddressRead(AddressBase):
    id: int
    customer_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
