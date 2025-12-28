"""Agent Configuration model for Super-User Admin Dashboard."""

import uuid

from sqlalchemy import ARRAY, Column, DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.models import Base


class AgentConfiguration(Base):
    """Agent Configuration model for store subscription settings."""

    __tablename__ = "agent_configurations"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    enabled_agents = Column(ARRAY(String), nullable=False, default=list)
    last_updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_updated_by = Column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
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
    store = relationship("Store", back_populates="agent_configuration")
    updated_by_user = relationship("User", foreign_keys=[last_updated_by])
