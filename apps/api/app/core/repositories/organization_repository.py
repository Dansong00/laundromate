"""Organization repository implementation."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.organization import Organization
from app.core.repositories.base import BaseRepository
from app.core.repositories.exceptions import ResourceNotFoundError
from app.core.schemas.organization import (
    OrganizationCreate,
    OrganizationRead,
    OrganizationUpdate,
)


class OrganizationRepository(BaseRepository):
    """
    Repository for Organization entities.

    Implements the Repository protocol for CRUD operations on organizations.
    """

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session."""
        super().__init__(session)

    def create(self, entity: OrganizationCreate) -> OrganizationRead:
        """Create a new organization."""
        db_org = Organization(**entity.model_dump())
        self.session.add(db_org)
        self.session.commit()
        self.session.refresh(db_org)
        return OrganizationRead.model_validate(db_org)

    def get_by_id(self, entity_id: UUID | str) -> OrganizationRead | None:
        """Get organization by ID."""
        org = (
            self.session.query(Organization)
            .filter(Organization.id == entity_id)
            .first()
        )
        return OrganizationRead.model_validate(org) if org else None

    def list(
        self, skip: int = 0, limit: int = 50, status: str | None = None
    ) -> list[OrganizationRead]:
        """List organizations with optional filtering."""
        query = self.session.query(Organization)
        if status:
            from app.core.models.organization import OrganizationStatus

            query = query.filter(Organization.status == OrganizationStatus(status))
        orgs = query.offset(skip).limit(limit).all()
        return [OrganizationRead.model_validate(org) for org in orgs]

    def update(
        self, entity_id: UUID | str, entity: OrganizationUpdate
    ) -> OrganizationRead:
        """Update an organization."""
        db_org = (
            self.session.query(Organization)
            .filter(Organization.id == entity_id)
            .first()
        )
        if not db_org:
            raise ResourceNotFoundError("Organization", entity_id)

        update_data = entity.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_org, key, value)

        self.session.commit()
        self.session.refresh(db_org)
        return OrganizationRead.model_validate(db_org)

    def delete(self, entity_id: UUID | str) -> bool:
        """Delete an organization."""
        db_org = (
            self.session.query(Organization)
            .filter(Organization.id == entity_id)
            .first()
        )
        if not db_org:
            return False

        self.session.delete(db_org)
        self.session.commit()
        return True
