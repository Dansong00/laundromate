"""User-Organization repository implementation."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.user_organization import UserOrganization
from app.core.repositories.base import BaseRepository
from app.core.repositories.exceptions import ResourceNotFoundError
from app.core.schemas.user_organization import (
    UserOrganizationCreate,
    UserOrganizationRead,
)


class UserOrganizationRepository(BaseRepository):
    """
    Repository for UserOrganization entities.

    Implements the Repository protocol for CRUD operations
    on user-organization associations.
    """

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session."""
        super().__init__(session)

    def create(self, entity: UserOrganizationCreate) -> UserOrganizationRead:
        """Create a new user-organization association."""
        db_user_org = UserOrganization(**entity.model_dump())
        self.session.add(db_user_org)
        self.session.commit()
        self.session.refresh(db_user_org)
        return UserOrganizationRead.model_validate(db_user_org)

    def get_by_id(self, entity_id: UUID | str) -> UserOrganizationRead | None:
        """Get user-organization association by ID."""
        user_org = (
            self.session.query(UserOrganization)
            .filter(UserOrganization.id == entity_id)
            .first()
        )
        return UserOrganizationRead.model_validate(user_org) if user_org else None

    def find_by_user_and_organization(
        self, user_id: UUID, organization_id: UUID
    ) -> UserOrganizationRead | None:
        """Find user-organization association by user ID and organization ID."""
        user_org = (
            self.session.query(UserOrganization)
            .filter(
                UserOrganization.user_id == user_id,
                UserOrganization.organization_id == organization_id,
            )
            .first()
        )
        return UserOrganizationRead.model_validate(user_org) if user_org else None

    def list(self, skip: int = 0, limit: int = 100) -> list[UserOrganizationRead]:
        """List all user-organization associations."""
        user_orgs = self.session.query(UserOrganization).offset(skip).limit(limit).all()
        return [UserOrganizationRead.model_validate(user_org) for user_org in user_orgs]

    def update(
        self, entity_id: UUID | str, entity: UserOrganizationCreate
    ) -> UserOrganizationRead:
        """Update a user-organization association."""
        db_user_org = (
            self.session.query(UserOrganization)
            .filter(UserOrganization.id == entity_id)
            .first()
        )
        if not db_user_org:
            raise ResourceNotFoundError("UserOrganization", entity_id)

        update_data = entity.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user_org, key, value)

        self.session.commit()
        self.session.refresh(db_user_org)
        return UserOrganizationRead.model_validate(db_user_org)

    def delete(self, entity_id: UUID | str) -> bool:
        """Delete a user-organization association."""
        db_user_org = (
            self.session.query(UserOrganization)
            .filter(UserOrganization.id == entity_id)
            .first()
        )
        if not db_user_org:
            return False

        self.session.delete(db_user_org)
        self.session.commit()
        return True
