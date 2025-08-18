from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from .address import AddressRead
from .user import UserRead


class CustomerBase(BaseModel):
    preferred_pickup_time: Optional[str] = None
    special_instructions: Optional[str] = None
    loyalty_points: int = 0
    is_vip: bool = False
    email_notifications: bool = True
    sms_notifications: bool = True


class CustomerCreate(CustomerBase):
    user_id: UUID


class CustomerUpdate(BaseModel):
    preferred_pickup_time: Optional[str] = None
    special_instructions: Optional[str] = None
    loyalty_points: Optional[int] = None
    is_vip: Optional[bool] = None
    email_notifications: Optional[bool] = None
    sms_notifications: Optional[bool] = None


class CustomerRead(CustomerBase):
    id: int
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    user: UserRead

    class Config:
        from_attributes = True


class CustomerWithAddresses(CustomerRead):
    addresses: List[AddressRead] = []

    class Config:
        from_attributes = True
