"""Store repository implementation."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.store import Store
from app.core.repositories.base import BaseRepository
from app.core.repositories.exceptions import ResourceNotFoundError
from app.core.schemas.store import StoreCreate, StoreRead, StoreUpdate


class StoreRepository(BaseRepository):
    """
    Repository for Store entities.

    Implements the Repository protocol for CRUD operations on stores.
    """

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session."""
        super().__init__(session)

    def create(self, entity: StoreCreate) -> StoreRead:
        """Create a new store."""
        db_store = Store(**entity.model_dump())
        self.session.add(db_store)
        self.session.commit()
        self.session.refresh(db_store)
        return StoreRead.model_validate(db_store)

    def get_by_id(self, entity_id: UUID | str) -> StoreRead | None:
        """Get store by ID."""
        store = self.session.query(Store).filter(Store.id == entity_id).first()
        return StoreRead.model_validate(store) if store else None

    def list_by_organization(
        self, organization_id: UUID | str, skip: int = 0, limit: int = 50
    ) -> list[StoreRead]:
        """List stores for an organization."""
        stores = (
            self.session.query(Store)
            .filter(Store.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [StoreRead.model_validate(store) for store in stores]

    def list(self, skip: int = 0, limit: int = 50) -> list[StoreRead]:
        """List all stores."""
        stores = self.session.query(Store).offset(skip).limit(limit).all()
        return [StoreRead.model_validate(store) for store in stores]

    def update(self, entity_id: UUID | str, entity: StoreUpdate) -> StoreRead:
        """Update a store."""
        db_store = self.session.query(Store).filter(Store.id == entity_id).first()
        if not db_store:
            raise ResourceNotFoundError("Store", entity_id)

        update_data = entity.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_store, key, value)

        self.session.commit()
        self.session.refresh(db_store)
        return StoreRead.model_validate(db_store)

    def delete(self, entity_id: UUID | str) -> bool:
        """Delete a store."""
        db_store = self.session.query(Store).filter(Store.id == entity_id).first()
        if not db_store:
            return False

        self.session.delete(db_store)
        self.session.commit()
        return True
