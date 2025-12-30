"""Agent Configuration repository implementation."""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.agent_configuration import AgentConfiguration
from app.core.schemas.agent_configuration import (
    AgentConfigurationRead,
    AgentConfigurationUpdate,
)


class AgentConfigurationRepository:
    """
    Repository for Agent Configuration entities.

    Note: This repository uses a specialized pattern (upsert/create_or_update)
    rather than standard CRUD, as agent configurations are store-specific
    singletons. It does not fully implement the Repository protocol but follows
    similar patterns for consistency.
    """

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session."""
        self.session = session

    def get_by_store_id(self, store_id: UUID | str) -> AgentConfigurationRead | None:
        """Get agent configuration by store ID."""
        config = (
            self.session.query(AgentConfiguration)
            .filter(AgentConfiguration.store_id == store_id)
            .first()
        )
        return AgentConfigurationRead.model_validate(config) if config else None

    def create_or_update(
        self, store_id: UUID | str, entity: AgentConfigurationUpdate, updated_by: UUID
    ) -> AgentConfigurationRead:
        """Create or update agent configuration for a store."""
        db_config = (
            self.session.query(AgentConfiguration)
            .filter(AgentConfiguration.store_id == store_id)
            .first()
        )

        if not db_config:
            # Create new configuration
            db_config = AgentConfiguration(
                store_id=store_id,
                enabled_agents=entity.enabled_agents,
                last_updated_by=updated_by,
                last_updated_at=datetime.now(timezone.utc),
            )
            self.session.add(db_config)
        else:
            # Update existing configuration
            db_config.enabled_agents = entity.enabled_agents
            db_config.last_updated_by = updated_by
            db_config.last_updated_at = datetime.now(timezone.utc)

        self.session.commit()
        self.session.refresh(db_config)
        return AgentConfigurationRead.model_validate(db_config)

    def update(
        self, store_id: UUID | str, entity: AgentConfigurationUpdate, updated_by: UUID
    ) -> AgentConfigurationRead:
        """Update agent configuration."""
        return self.create_or_update(store_id, entity, updated_by)
