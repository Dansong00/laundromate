"""Store model for Super-User Admin Dashboard."""

import enum
import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.models import Base


class StoreStatus(str, enum.Enum):
    """Store status enum."""

    ACTIVE = "active"
    INACTIVE = "inactive"


class Store(Base):
    """Store model representing a physical laundromat location."""

    __tablename__ = "stores"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name = Column(String(255), nullable=False)
    street_address = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(2), nullable=False)  # ISO 3166-1 alpha-2
    status = Column(Enum(StoreStatus), nullable=False, default=StoreStatus.ACTIVE)
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
    organization = relationship("Organization", back_populates="stores")
    iot_controllers = relationship(
        "IoTController", back_populates="store", cascade="all, delete-orphan"
    )
    agent_configuration = relationship(
        "AgentConfiguration",
        back_populates="store",
        uselist=False,
        cascade="all, delete-orphan",
    )
    user_stores = relationship(
        "UserStore", back_populates="store", cascade="all, delete-orphan"
    )

    # Constraints
    __table_args__ = (
        UniqueConstraint("organization_id", "name", name="uq_store_org_name"),
    )
