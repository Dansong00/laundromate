"""User-Store repository implementation."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.user_store import UserStore
from app.core.repositories.base import BaseRepository
from app.core.repositories.exceptions import ResourceNotFoundError
from app.core.schemas.user_store import UserStoreCreate, UserStoreRead


class UserStoreRepository(BaseRepository):
    """
    Repository for User-Store association entities.

    Implements the Repository protocol for CRUD operations on user-store associations.
    """

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session."""
        super().__init__(session)

    def create(self, entity: UserStoreCreate) -> UserStoreRead:
        """Create a new user-store association."""
        db_user_store = UserStore(**entity.model_dump())
        self.session.add(db_user_store)
        self.session.commit()
        self.session.refresh(db_user_store)
        return UserStoreRead.model_validate(db_user_store)

    def get_by_id(self, entity_id: UUID | str) -> UserStoreRead | None:
        """Get user-store association by ID."""
        user_store = (
            self.session.query(UserStore).filter(UserStore.id == entity_id).first()
        )
        return UserStoreRead.model_validate(user_store) if user_store else None

    def find_by_user_and_store(
        self, user_id: UUID, store_id: UUID
    ) -> UserStoreRead | None:
        """Find user-store association by user ID and store ID (returns schema)."""
        user_store = (
            self.session.query(UserStore)
            .filter(
                UserStore.user_id == user_id,
                UserStore.store_id == store_id,
            )
            .first()
        )
        return UserStoreRead.model_validate(user_store) if user_store else None

    def get_model_by_user_and_store(
        self, user_id: UUID, store_id: UUID
    ) -> UserStore | None:
        """
        Get user-store association by user ID and store ID.

        Returns model instance for internal service use.
        """
        return (
            self.session.query(UserStore)
            .filter(
                UserStore.user_id == user_id,
                UserStore.store_id == store_id,
            )
            .first()
        )

    def list(self, skip: int = 0, limit: int = 100) -> list[UserStoreRead]:
        """List all user-store associations."""
        user_stores = self.session.query(UserStore).offset(skip).limit(limit).all()
        return [UserStoreRead.model_validate(user_store) for user_store in user_stores]

    def update(self, entity_id: UUID | str, entity: UserStoreRead) -> UserStoreRead:
        """Update a user-store association."""
        db_user_store = (
            self.session.query(UserStore).filter(UserStore.id == entity_id).first()
        )
        if not db_user_store:
            raise ResourceNotFoundError("UserStore", entity_id)

        update_data = entity.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user_store, key, value)

        self.session.commit()
        self.session.refresh(db_user_store)
        return UserStoreRead.model_validate(db_user_store)

    def delete(self, entity_id: UUID | str) -> bool:
        """Delete a user-store association."""
        db_user_store = (
            self.session.query(UserStore).filter(UserStore.id == entity_id).first()
        )
        if not db_user_store:
            return False

        self.session.delete(db_user_store)
        self.session.commit()
        return True
