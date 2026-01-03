"""User repository implementation."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.user import User
from app.core.repositories.base import BaseRepository
from app.core.repositories.exceptions import ResourceNotFoundError
from app.core.schemas.user import UserCreate, UserRead, UserUpdate


class UserRepository(BaseRepository):
    """
    Repository for User entities.

    Implements the Repository protocol for CRUD operations on users.
    """

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session."""
        super().__init__(session)

    def create(self, entity: UserCreate) -> UserRead:
        """Create a new user."""
        db_user = User(**entity.model_dump())
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return UserRead.model_validate(db_user)

    def get_by_id(self, entity_id: UUID | str | int) -> UserRead | None:
        """Get user by ID."""
        user = self.session.query(User).filter(User.id == entity_id).first()
        return UserRead.model_validate(user) if user else None

    def get_by_email(self, email: str) -> UserRead | None:
        """Get user by email."""
        user = self.session.query(User).filter(User.email == email).first()
        return UserRead.model_validate(user) if user else None

    def list(self, skip: int = 0, limit: int = 100) -> list[UserRead]:
        """List all users."""
        users = self.session.query(User).offset(skip).limit(limit).all()
        return [UserRead.model_validate(user) for user in users]

    def update(self, entity_id: UUID | str | int, entity: UserUpdate) -> UserRead:
        """Update a user."""
        db_user = self.session.query(User).filter(User.id == entity_id).first()
        if not db_user:
            raise ResourceNotFoundError("User", entity_id)

        update_data = entity.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)

        self.session.commit()
        self.session.refresh(db_user)
        return UserRead.model_validate(db_user)

    def delete(self, entity_id: UUID | str | int) -> bool:
        """Delete a user."""
        db_user = self.session.query(User).filter(User.id == entity_id).first()
        if not db_user:
            return False

        self.session.delete(db_user)
        self.session.commit()
        return True
