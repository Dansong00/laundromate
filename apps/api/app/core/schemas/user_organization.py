"""User-Organization Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.core.models.user_organization import UserOrganizationRole


class UserOrganizationBase(BaseModel):
    """Base user-organization association schema."""

    user_id: UUID
    organization_id: UUID
    role: UserOrganizationRole


class UserOrganizationCreate(UserOrganizationBase):
    """Schema for creating a new user-organization association."""

    pass


class UserOrganizationRead(UserOrganizationBase):
    """Schema for reading a user-organization association."""

    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
