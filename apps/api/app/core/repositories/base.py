"""
Repository Protocol and Base Class

Defines the repository interface that accepts a database session dependency
and specifies CRUD operations to be implemented.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.orm import Session


class Repository(Protocol):
    """
    Repository protocol that defines CRUD operations.

    Implementations must accept a database session as a dependency
    and implement the specified CRUD methods.

    This protocol uses structural typing - any class that implements
    these methods with compatible signatures will be considered a
    Repository, even without explicit inheritance.

    Expected method signatures:
        - create(entity: CreateSchema) -> ReadSchema
        - get_by_id(entity_id: UUID | str | int) -> ReadSchema | None
        - list(skip: int = 0, limit: int = 100) -> list[ReadSchema]
        - update(entity_id: UUID | str | int, entity: UpdateSchema) -> ReadSchema
        - delete(entity_id: UUID | str | int) -> bool

    Where CreateSchema, ReadSchema, and UpdateSchema are Pydantic BaseModel subclasses.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the repository with a database session.

        Args:
            session: SQLAlchemy database session
        """
        ...

    def create(self, entity: BaseModel) -> BaseModel:
        """
        Create a new entity in the database.

        Args:
            entity: The create schema instance (subclass of BaseModel)

        Returns:
            The created entity as a read schema (subclass of BaseModel)
        """
        ...

    def get_by_id(self, entity_id: UUID | str | int) -> BaseModel | None:
        """
        Retrieve an entity by its primary key.

        Args:
            entity_id: The primary key value (UUID, string, or int)

        Returns:
            The entity if found, None otherwise (as a read schema subclass of BaseModel)
        """
        ...

    def list(self, skip: int = 0, limit: int = 100) -> list[BaseModel]:
        """
        Retrieve all entities with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of entities (as read schemas, subclasses of BaseModel)
        """
        ...

    def update(self, entity_id: UUID | str | int, entity: BaseModel) -> BaseModel:
        """
        Update an existing entity in the database.

        Args:
            entity_id: The primary key value (UUID, string, or int)
            entity: The update schema with new values (subclass of BaseModel)

        Returns:
            The updated entity as a read schema (subclass of BaseModel)
        """
        ...

    def delete(self, entity_id: UUID | str | int) -> bool:
        """
        Delete an entity by its primary key.

        Args:
            entity_id: The primary key value (UUID, string, or int)

        Returns:
            True if entity was deleted, False if not found
        """
        ...


class BaseRepository(ABC):
    """
    Abstract base class for repository implementations.

    Provides a concrete base class that repositories can inherit from,
    ensuring they implement all required CRUD operations. This complements
    the Repository Protocol by providing explicit inheritance.

    Subclasses must implement all abstract methods with the appropriate
    schema types (CreateSchema, ReadSchema, UpdateSchema).
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the repository with a database session.

        Args:
            session: SQLAlchemy database session
        """
        self.session = session

    @abstractmethod
    def create(self, entity: BaseModel) -> BaseModel:
        """
        Create a new entity in the database.

        Args:
            entity: The create schema instance (subclass of BaseModel)

        Returns:
            The created entity as a read schema (subclass of BaseModel)
        """
        ...

    @abstractmethod
    def get_by_id(self, entity_id: UUID | str | int) -> BaseModel | None:
        """
        Retrieve an entity by its primary key.

        Args:
            entity_id: The primary key value (UUID, string, or int)

        Returns:
            The entity if found, None otherwise (as a read schema subclass of BaseModel)
        """
        ...

    @abstractmethod
    def list(self, skip: int = 0, limit: int = 100) -> list[BaseModel]:
        """
        Retrieve all entities with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of entities (as read schemas, subclasses of BaseModel)
        """
        ...

    @abstractmethod
    def update(self, entity_id: UUID | str | int, entity: BaseModel) -> BaseModel:
        """
        Update an existing entity in the database.

        Args:
            entity_id: The primary key value (UUID, string, or int)
            entity: The update schema with new values (subclass of BaseModel)

        Returns:
            The updated entity as a read schema (subclass of BaseModel)
        """
        ...

    @abstractmethod
    def delete(self, entity_id: UUID | str | int) -> bool:
        """
        Delete an entity by its primary key.

        Args:
            entity_id: The primary key value (UUID, string, or int)

        Returns:
            True if entity was deleted, False if not found
        """
        ...
