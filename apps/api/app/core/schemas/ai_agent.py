"""AI Agent Pydantic schemas for Super-Admin Dashboard."""

from datetime import datetime

from pydantic import BaseModel

from app.core.models.ai_agent import AgentCategory


class AIAgentRead(BaseModel):
    """Schema for reading an AI agent."""

    id: str
    name: str
    description: str | None = None
    category: AgentCategory
    is_available: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
