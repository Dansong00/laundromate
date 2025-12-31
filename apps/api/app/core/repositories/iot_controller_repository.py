"""IoT Controller repository implementation."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.iot_controller import IoTController
from app.core.repositories.base import BaseRepository
from app.core.repositories.exceptions import ResourceNotFoundError
from app.core.schemas.iot_controller import (
    IoTControllerCreate,
    IoTControllerRead,
    IoTControllerUpdate,
)


class IoTControllerRepository(BaseRepository):
    """
    Repository for IoT Controller entities.

    Implements the Repository protocol for CRUD operations on IoT controllers.
    Note: This repository includes entity-specific methods like list_by_store()
    in addition to the standard CRUD operations.
    """

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session."""
        super().__init__(session)

    def create(self, entity: IoTControllerCreate) -> IoTControllerRead:
        """Create a new IoT controller."""
        db_controller = IoTController(**entity.model_dump())
        self.session.add(db_controller)
        self.session.commit()
        self.session.refresh(db_controller)
        return IoTControllerRead.model_validate(db_controller)

    def get_by_id(self, entity_id: UUID | str) -> IoTControllerRead | None:
        """Get IoT controller by ID."""
        controller = (
            self.session.query(IoTController)
            .filter(IoTController.id == entity_id)
            .first()
        )
        return IoTControllerRead.model_validate(controller) if controller else None

    def list_by_store(
        self, store_id: UUID | str, skip: int = 0, limit: int = 100
    ) -> list[IoTControllerRead]:
        """List IoT controllers for a store."""
        controllers = (
            self.session.query(IoTController)
            .filter(IoTController.store_id == store_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [
            IoTControllerRead.model_validate(controller) for controller in controllers
        ]

    def update(
        self, entity_id: UUID | str, entity: IoTControllerUpdate
    ) -> IoTControllerRead:
        """Update an IoT controller."""
        db_controller = (
            self.session.query(IoTController)
            .filter(IoTController.id == entity_id)
            .first()
        )
        if not db_controller:
            raise ResourceNotFoundError("IoTController", entity_id)

        update_data = entity.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_controller, key, value)

        self.session.commit()
        self.session.refresh(db_controller)
        return IoTControllerRead.model_validate(db_controller)

    def delete(self, entity_id: UUID | str) -> bool:
        """Delete an IoT controller."""
        db_controller = (
            self.session.query(IoTController)
            .filter(IoTController.id == entity_id)
            .first()
        )
        if not db_controller:
            return False

        self.session.delete(db_controller)
        self.session.commit()
        return True
