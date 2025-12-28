"""Agent Configuration Pydantic schemas for Super-Admin Dashboard."""

from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, field_validator


class AgentConfigurationBase(BaseModel):
    """Base agent configuration schema."""

    enabled_agents: List[str] = []

    @field_validator("enabled_agents")
    @classmethod
    def validate_enabled_agents(cls, v: List[str]) -> List[str]:
        """Validate that enabled_agents contains valid agent identifiers."""
        # This will be validated against ai_agents table in the service layer
        return v


class AgentConfigurationUpdate(AgentConfigurationBase):
    """Schema for updating agent configuration."""

    pass


class AgentConfigurationRead(AgentConfigurationBase):
    """Schema for reading agent configuration."""

    id: UUID
    store_id: UUID
    last_updated_at: datetime
    last_updated_by: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
