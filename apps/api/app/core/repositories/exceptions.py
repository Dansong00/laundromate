"""
Repository-specific exceptions for error handling.
"""


class RepositoryError(Exception):
    """Base exception for repository operations."""

    pass


class ResourceNotFoundError(RepositoryError):
    """Raised when an entity is not found."""

    def __init__(self, entity_type: str, entity_id: int | str):
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} with id {entity_id} not found")


class DuplicateResourceError(RepositoryError):
    """Raised when attempting to create a duplicate entity."""

    def __init__(self, entity_type: str, field: str, value: str):
        self.entity_type = entity_type
        self.field = field
        self.value = value
        super().__init__(f"{entity_type} with {field} '{value}' already exists")
