"""Invitation repository implementation."""

from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.invitation import Invitation, InvitationStatus
from app.core.repositories.base import BaseRepository
from app.core.repositories.exceptions import ResourceNotFoundError
from app.core.schemas.invitation import (
    InvitationCreate,
    InvitationRead,
    InvitationUpdate,
)


class InvitationRepository(BaseRepository):
    """
    Repository for Invitation entities.

    Implements the Repository protocol for CRUD operations on invitations.
    """

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session."""
        super().__init__(session)

    def create(self, entity: InvitationCreate) -> InvitationRead:
        """Create a new invitation."""
        db_invitation = Invitation(**entity.model_dump())
        self.session.add(db_invitation)
        self.session.commit()
        self.session.refresh(db_invitation)
        return InvitationRead.model_validate(db_invitation)

    def get_by_id(self, entity_id: UUID | str) -> InvitationRead | None:
        """Get invitation by ID."""
        invitation = (
            self.session.query(Invitation).filter(Invitation.id == entity_id).first()
        )
        return InvitationRead.model_validate(invitation) if invitation else None

    def get_by_token(self, token: str) -> InvitationRead | None:
        """Get invitation by token."""
        invitation = (
            self.session.query(Invitation).filter(Invitation.token == token).first()
        )
        return InvitationRead.model_validate(invitation) if invitation else None

    def find_pending_by_email_and_organization(
        self, email: str, store_id: UUID
    ) -> InvitationRead | None:
        """Find pending invitation by email and store ID."""
        invitation = (
            self.session.query(Invitation)
            .filter(
                Invitation.email == email,
                Invitation.store_id == store_id,
                Invitation.status == InvitationStatus.PENDING,
            )
            .first()
        )
        return InvitationRead.model_validate(invitation) if invitation else None

    def list(self, skip: int = 0, limit: int = 50) -> list[InvitationRead]:
        """List all invitations."""
        invitations = self.session.query(Invitation).offset(skip).limit(limit).all()
        return [InvitationRead.model_validate(invitation) for invitation in invitations]

    def update(self, entity_id: UUID | str, entity: InvitationUpdate) -> InvitationRead:
        """Update an invitation."""
        db_invitation = (
            self.session.query(Invitation).filter(Invitation.id == entity_id).first()
        )
        if not db_invitation:
            raise ResourceNotFoundError("Invitation", entity_id)

        update_data = entity.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_invitation, key, value)

        self.session.commit()
        self.session.refresh(db_invitation)
        return InvitationRead.model_validate(db_invitation)

    def mark_as_expired(self, invitation_id: UUID | str) -> InvitationRead:
        """Mark an invitation as expired."""
        return self.update(
            invitation_id,
            InvitationUpdate(status=InvitationStatus.EXPIRED),
        )

    def mark_as_accepted(
        self, invitation_id: UUID | str, accepted_at: datetime
    ) -> InvitationRead:
        """Mark an invitation as accepted."""
        return self.update(
            invitation_id,
            InvitationUpdate(status=InvitationStatus.ACCEPTED, accepted_at=accepted_at),
        )

    def delete(self, entity_id: UUID | str) -> bool:
        """Delete an invitation."""
        db_invitation = (
            self.session.query(Invitation).filter(Invitation.id == entity_id).first()
        )
        if not db_invitation:
            return False

        self.session.delete(db_invitation)
        self.session.commit()
        return True
