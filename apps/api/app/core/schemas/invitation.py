"""Invitation Pydantic schemas for store owner invitations."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.core.models.invitation import InvitationStatus


class InvitationBase(BaseModel):
    """Base invitation schema."""

    email: EmailStr
    store_id: UUID


class InvitationCreate(InvitationBase):
    """Schema for creating a new invitation."""

    pass


class InvitationRead(InvitationBase):
    """Schema for reading an invitation."""

    id: UUID
    token: str
    invited_by: UUID
    status: InvitationStatus
    expires_at: datetime
    accepted_at: datetime | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class InvitationValidate(BaseModel):
    """Schema for validating an invitation token."""

    token: str
    is_valid: bool
    status: InvitationStatus | None = None
    expires_at: datetime | None = None
    message: str | None = None


class InvitationAccept(BaseModel):
    """Schema for accepting an invitation."""

    token: str
    password: str
