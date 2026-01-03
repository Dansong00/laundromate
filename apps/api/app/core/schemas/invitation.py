"""Invitation Pydantic schemas for organization member invitations."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.core.models.invitation import InvitationStatus
from app.core.models.user_organization import UserOrganizationRole


class InvitationBase(BaseModel):
    """Base invitation schema."""

    email: EmailStr
    organization_id: UUID


class InvitationCreate(InvitationBase):
    """Schema for creating a new invitation."""

    token: str
    organization_role: UserOrganizationRole = UserOrganizationRole.OWNER
    invited_by: UUID
    expires_at: datetime
    status: InvitationStatus = InvitationStatus.PENDING


class InvitationRead(InvitationBase):
    """Schema for reading an invitation."""

    id: UUID
    token: str
    organization_role: UserOrganizationRole
    invited_by: UUID
    status: InvitationStatus
    expires_at: datetime
    accepted_at: datetime | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class InvitationValidateResponse(BaseModel):
    """Schema for invitation validation response."""

    valid: bool
    email: str | None = None
    organization_id: str | None = None
    organization_name: str | None = None
    organization_role: UserOrganizationRole | None = None
    reason: str | None = None


class InvitationUpdate(BaseModel):
    """Schema for updating an invitation."""

    status: InvitationStatus | None = None
    accepted_at: datetime | None = None


class InvitationAcceptRequest(BaseModel):
    """Schema for accepting an invitation request."""

    password: str


class InviteMemberRequest(BaseModel):
    """Schema for inviting an organization member."""

    email: EmailStr
    organization_role: UserOrganizationRole = UserOrganizationRole.OWNER
