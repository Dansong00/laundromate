"""AI Agent model for Super-User Admin Dashboard."""

import enum

from sqlalchemy import Boolean, Column, DateTime, Enum, String
from sqlalchemy.sql import func

from app.core.models import Base


class AgentCategory(str, enum.Enum):
    """Agent category enum."""

    MAINTENANCE = "maintenance"
    PRICING = "pricing"
    SCHEDULING = "scheduling"
    ANALYTICS = "analytics"
    OTHER = "other"


class AIAgent(Base):
    """AI Agent model representing an available intelligent agent feature."""

    __tablename__ = "ai_agents"

    id = Column(String(100), primary_key=True)  # e.g., "maintenance_prophet"
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    category = Column(Enum(AgentCategory), nullable=False)
    is_available = Column(Boolean, nullable=False, default=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
