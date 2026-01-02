"""User-Organization association model for many-to-many relationship."""

import enum
import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Index, Uuid
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.models import Base


class UserOrganizationRole(str, enum.Enum):
    """User-Organization role enum."""

    OWNER = "owner"
    EMPLOYEE = "employee"
    ADMIN = "admin"


class UserOrganization(Base):
    """User-Organization association model for many-to-many relationship."""

    __tablename__ = "user_organizations"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    organization_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role = Column(
        Enum(UserOrganizationRole), nullable=False, default=UserOrganizationRole.OWNER
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    user = relationship("User")
    organization = relationship("Organization", back_populates="user_organizations")

    # Constraints
    __table_args__ = (
        Index(
            "ix_user_organizations_user_org", "user_id", "organization_id", unique=True
        ),
    )
