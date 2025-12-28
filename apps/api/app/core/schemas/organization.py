"""Organization Pydantic schemas for Super-Admin Dashboard."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.core.models.organization import OrganizationStatus


class OrganizationBase(BaseModel):
    """Base organization schema with common fields."""

    name: str
    billing_address: str
    city: str
    state: str
    postal_code: str
    country: str
    contact_email: EmailStr | None = None
    contact_phone: str | None = None
    status: OrganizationStatus = OrganizationStatus.ACTIVE


class OrganizationCreate(OrganizationBase):
    """Schema for creating a new organization."""

    pass


class OrganizationUpdate(BaseModel):
    """Schema for updating an organization."""

    name: str | None = None
    billing_address: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country: str | None = None
    contact_email: EmailStr | None = None
    contact_phone: str | None = None
    status: OrganizationStatus | None = None


class OrganizationRead(OrganizationBase):
    """Schema for reading an organization."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
