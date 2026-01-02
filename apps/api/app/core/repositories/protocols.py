"""Repository protocols for dependency injection.

These protocols define the minimal interface that services need from repositories,
following the Interface Segregation Principle. Services depend on protocols rather
than concrete implementations, enabling loose coupling and better testability.
"""

from __future__ import annotations

from datetime import datetime
from typing import Protocol
from uuid import UUID

from app.core.models.user_store import UserStore
from app.core.schemas.invitation import InvitationCreate, InvitationRead
from app.core.schemas.organization import OrganizationRead
from app.core.schemas.user import UserCreate, UserRead
from app.core.schemas.user_organization import (
    UserOrganizationCreate,
    UserOrganizationRead,
)
from app.core.schemas.user_store import UserStoreCreate, UserStoreRead


class InvitationRepositoryProtocol(Protocol):
    """Protocol for invitation repository operations."""

    def find_pending_by_email_and_organization(
        self, email: str, organization_id: UUID
    ) -> InvitationRead | None:
        """Find pending invitation by email and organization ID."""
        ...

    def create(self, entity: InvitationCreate) -> InvitationRead:
        """Create a new invitation."""
        ...

    def get_by_token(self, token: str) -> InvitationRead | None:
        """Get invitation by token."""
        ...

    def mark_as_expired(self, invitation_id: UUID | str) -> InvitationRead:
        """Mark an invitation as expired."""
        ...

    def mark_as_accepted(
        self, invitation_id: UUID | str, accepted_at: datetime
    ) -> InvitationRead:
        """Mark an invitation as accepted."""
        ...


class UserOrganizationRepositoryProtocol(Protocol):
    """Protocol for user-organization repository operations."""

    def find_by_user_and_organization(
        self, user_id: UUID, organization_id: UUID
    ) -> UserOrganizationRead | None:
        """Find user-organization association by user ID and organization ID."""
        ...

    def create(self, entity: UserOrganizationCreate) -> UserOrganizationRead:
        """Create a new user-organization association."""
        ...


class OrganizationRepositoryProtocol(Protocol):
    """Protocol for organization repository operations."""

    def get_by_id(self, entity_id: UUID) -> OrganizationRead | None:
        """Get organization by ID."""
        ...


class UserRepositoryProtocol(Protocol):
    """Protocol for user repository operations."""

    def get_by_email(self, email: str) -> UserRead | None:
        """Get user by email."""
        ...

    def create(self, entity: UserCreate) -> UserRead:
        """Create a new user."""
        ...


class UserStoreRepositoryProtocol(Protocol):
    """Protocol for user-store repository operations."""

    def get_model_by_user_and_store(
        self, user_id: UUID, store_id: UUID
    ) -> UserStore | None:
        """
        Get user-store association by user ID and store ID.

        Returns model instance for internal service use.
        """
        ...

    def create(self, entity: UserStoreCreate) -> UserStoreRead:
        """Create a new user-store association."""
        ...
