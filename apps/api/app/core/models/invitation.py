"""Invitation model for organization member invitations."""

import enum
import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, Uuid
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.models import Base
from app.core.models.user_organization import UserOrganizationRole


class InvitationStatus(str, enum.Enum):
    """Invitation status enum."""

    PENDING = "pending"
    ACCEPTED = "accepted"
    EXPIRED = "expired"
    REVOKED = "revoked"


class Invitation(Base):
    """Invitation model for organization member email invitations."""

    __tablename__ = "invitations"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = Column(String(255), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False, index=True)
    organization_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    organization_role = Column(
        Enum(UserOrganizationRole),
        nullable=False,
        default=UserOrganizationRole.OWNER,
    )
    invited_by = Column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    status = Column(
        Enum(InvitationStatus),
        nullable=False,
        default=InvitationStatus.PENDING,
        index=True,
    )
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    accepted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    organization = relationship("Organization")
    inviter = relationship("User", foreign_keys=[invited_by])
