"""
Repository Pattern Interface

This module provides a generic repository interface for data access operations.
"""

from app.core.repositories.base import Repository
from app.core.repositories.exceptions import (
    DuplicateResourceError,
    RepositoryError,
    ResourceNotFoundError,
)

__all__ = [
    "Repository",
    "RepositoryError",
    "ResourceNotFoundError",
    "DuplicateResourceError",
]
