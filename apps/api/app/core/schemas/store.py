"""Store Pydantic schemas for Super-Admin Dashboard."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.core.models.store import StoreStatus


class StoreBase(BaseModel):
    """Base store schema with common fields."""

    name: str
    street_address: str
    city: str
    state: str
    postal_code: str
    country: str
    status: StoreStatus = StoreStatus.ACTIVE


class StoreCreate(StoreBase):
    """Schema for creating a new store."""

    organization_id: UUID


class StoreUpdate(BaseModel):
    """Schema for updating a store."""

    name: str | None = None
    street_address: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country: str | None = None
    status: StoreStatus | None = None


class StoreRead(StoreBase):
    """Schema for reading a store."""

    id: UUID
    organization_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
