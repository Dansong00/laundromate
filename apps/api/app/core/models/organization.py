"""Organization model for Super-User Admin Dashboard."""

import enum
import uuid

from sqlalchemy import Column, DateTime, Enum, Index, String, Uuid
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, text

from app.core.models import Base


class OrganizationStatus(str, enum.Enum):
    """Organization status enum."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class Organization(Base):
    """Organization model representing a parent company."""

    __tablename__ = "organizations"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    billing_address = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(2), nullable=False)  # ISO 3166-1 alpha-2
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    status = Column(
        Enum(OrganizationStatus),
        nullable=False,
        default=OrganizationStatus.ACTIVE,
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    stores = relationship(
        "Store", back_populates="organization", cascade="all, delete-orphan"
    )

    # Indexes
    __table_args__ = (
        Index(
            "ix_organizations_name_active",
            "name",
            postgresql_where=text("status = 'active'"),
            unique=True,
        ),
    )
