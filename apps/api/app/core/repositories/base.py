"""
Repository Protocol

Defines the repository interface that accepts a database session dependency
and specifies CRUD operations to be implemented.
"""

from __future__ import annotations

from typing import Protocol, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

# Type variable for the model type
ModelType = TypeVar("ModelType", bound=BaseModel)


class Repository(Protocol[ModelType]):
    """
    Repository protocol that defines CRUD operations.

    Implementations must accept a database session as a dependency
    and implement the specified CRUD methods.

    Type Parameters:
        ModelType: The Pydantic model class that inherits from BaseModel
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the repository with a database session.

        Args:
            session: SQLAlchemy database session
        """
        ...

    def create(self, entity: ModelType) -> ModelType:
        """
        Create a new entity in the database.

        Args:
            entity: The entity instance to create

        Returns:
            The created entity with database-generated fields populated
        """
        ...

    def get_by_id(self, entity_id: int | str) -> ModelType | None:
        """
        Retrieve an entity by its primary key.

        Args:
            entity_id: The primary key value (int or UUID string)

        Returns:
            The entity if found, None otherwise
        """
        ...

    def list(self) -> list[ModelType]:
        """
        Retrieve all entities.

        Returns:
            List of entities
        """
        ...

    def update(self, entity: ModelType) -> ModelType:
        """
        Update an existing entity in the database.

        Args:
            entity: The entity instance with updated values

        Returns:
            The updated entity
        """
        ...

    def delete(self, entity_id: int | str) -> bool:
        """
        Delete an entity by its primary key.

        Args:
            entity_id: The primary key value (int or UUID string)

        Returns:
            True if entity was deleted, False if not found
        """
        ...
