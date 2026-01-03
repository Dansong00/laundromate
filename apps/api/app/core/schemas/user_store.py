"""User-Store association Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.core.models.user_store import UserStoreRole


class UserStoreBase(BaseModel):
    """Base user-store association schema."""

    user_id: UUID
    store_id: UUID
    role: UserStoreRole


class UserStoreCreate(UserStoreBase):
    """Schema for creating a new user-store association."""

    pass


class UserStoreRead(UserStoreBase):
    """Schema for reading a user-store association."""

    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
