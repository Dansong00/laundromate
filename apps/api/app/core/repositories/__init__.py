"""
Repository Pattern Interface

This module provides a generic repository interface for data access operations.

All repository implementations should follow the Repository protocol defined in base.py.
The protocol uses structural typing, so repositories don't need to explicitly inherit
from it - they just need to implement the required methods with compatible signatures.

Standard repository methods:
    - create(entity: CreateSchema) -> ReadSchema
    - get_by_id(entity_id: UUID | str | int) -> ReadSchema | None
    - list(skip: int = 0, limit: int = 100) -> list[ReadSchema]
    - update(entity_id: UUID | str | int, entity: UpdateSchema) -> ReadSchema
    - delete(entity_id: UUID | str | int) -> bool

Repositories may also include entity-specific query methods (e.g., list_by_store,
list_by_organization) as needed.
"""

from app.core.repositories.base import BaseRepository, Repository
from app.core.repositories.exceptions import (
    DuplicateResourceError,
    RepositoryError,
    ResourceNotFoundError,
)

__all__ = [
    "Repository",
    "BaseRepository",
    "RepositoryError",
    "ResourceNotFoundError",
    "DuplicateResourceError",
]
