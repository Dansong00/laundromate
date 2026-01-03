"""Invitation service for handling invitation business logic."""
import re
import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import HTTPException, status

from app.auth.security import create_access_token
from app.core.config.settings import settings
from app.core.models.invitation import InvitationStatus
from app.core.models.user_organization import UserOrganizationRole
from app.core.repositories.protocols import (
    InvitationRepositoryProtocol,
    OrganizationRepositoryProtocol,
    UserOrganizationRepositoryProtocol,
    UserRepositoryProtocol,
    UserStoreRepositoryProtocol,
)
from app.core.schemas.invitation import (
    InvitationCreate,
    InvitationRead,
    InvitationValidateResponse,
)
from app.core.schemas.user import TokenWithUser, UserCreate
from app.core.schemas.user_organization import UserOrganizationCreate


class InvitationService:
    """Service for managing invitation business logic."""

    # Token format: URL-safe base64, 32 bytes = ~43 characters
    # Characters: A-Z, a-z, 0-9, -, _
    _TOKEN_MIN_LENGTH = 32
    _TOKEN_MAX_LENGTH = 64  # Allow some margin for encoding variations
    _TOKEN_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")

    def __init__(
        self,
        invitation_repo: InvitationRepositoryProtocol,
        user_repo: UserRepositoryProtocol,
        user_org_repo: UserOrganizationRepositoryProtocol,
        user_store_repo: UserStoreRepositoryProtocol,
        org_repo: OrganizationRepositoryProtocol,
    ) -> None:
        """
        Initialize invitation service with repositories.

        Args:
            invitation_repo: Repository for invitation operations
            user_repo: Repository for user operations
            user_org_repo: Repository for user-organization association operations
            user_store_repo: Repository for user-store association operations
            org_repo: Repository for organization operations
        """
        self.invitation_repo = invitation_repo
        self.user_repo = user_repo
        self.user_org_repo = user_org_repo
        self.user_store_repo = user_store_repo
        self.org_repo = org_repo

    def _validate_token_format(self, token: str) -> None:
        """
        Validate invitation token format before database operations.

        Args:
            token: The token to validate

        Raises:
            HTTPException: If token format is invalid (400 Bad Request)
        """
        if len(token) < self._TOKEN_MIN_LENGTH or len(token) > self._TOKEN_MAX_LENGTH:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid invitation token format",
            )

        if not self._TOKEN_PATTERN.match(token):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid invitation token format",
            )

    def generate_token(self) -> str:
        """
        Generate a secure, URL-safe invitation token.

        Uses secrets.token_urlsafe() to generate a 32-byte token
        encoded in URL-safe base64 (approximately 43 characters).

        Returns:
            str: A secure, URL-safe token string
        """
        return secrets.token_urlsafe(32)

    def is_valid(self, invitation: InvitationRead) -> bool:
        """
        Check if an invitation is valid for acceptance.

        An invitation is valid if:
        - Status is PENDING
        - Not expired (expires_at >= now)

        Args:
            invitation: The invitation to validate (schema)

        Returns:
            bool: True if invitation is valid, False otherwise
        """
        return (
            invitation.status == InvitationStatus.PENDING
            and invitation.expires_at >= datetime.now(timezone.utc)
        )

    def get_expiration_days(self) -> int:
        """
        Get the number of days until invitation expires.

        Defaults to 7 days, configurable via INVITATION_EXPIRATION_DAYS
        environment variable.

        Returns:
            int: Number of days until expiration
        """
        return getattr(settings, "INVITATION_EXPIRATION_DAYS", 7)

    def calculate_expiration(self) -> datetime:
        """
        Calculate the expiration datetime for a new invitation.

        Returns:
            datetime: Expiration datetime in UTC
        """
        expiration_days = self.get_expiration_days()
        return datetime.now(timezone.utc) + timedelta(days=expiration_days)

    def mark_as_expired(self, invitation_id: UUID) -> None:
        """
        Mark an invitation as expired.

        Args:
            invitation_id: The ID of the invitation to mark as expired
        """
        # Use repository to update the invitation status
        self.invitation_repo.mark_as_expired(invitation_id)

    def create_invitation(
        self,
        email: str,
        organization_id: UUID,
        organization_role: UserOrganizationRole,
        invited_by: UUID,
    ) -> InvitationRead:
        """
        Create a new invitation with token and expiration.

        Args:
            email: Email address of the invitee
            organization_id: ID of the organization to invite to
            organization_role: Role for the user in the organization
                (OWNER, EMPLOYEE, ADMIN)
            invited_by: ID of the user creating the invitation

        Returns:
            InvitationRead: The created invitation schema

        Raises:
            HTTPException: If invitation already exists for this email and organization
        """
        # Check for existing pending invitation
        existing_invitation = (
            self.invitation_repo.find_pending_by_email_and_organization(
                email, organization_id
            )
        )

        if existing_invitation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"An invitation has already been sent to {email} "
                    f"for this organization"
                ),
            )

        # Generate token and calculate expiration
        token = self.generate_token()
        expires_at = self.calculate_expiration()

        # Create invitation using repository
        invitation_create = InvitationCreate(
            email=email,
            organization_id=organization_id,
            organization_role=organization_role,
            token=token,
            invited_by=invited_by,
            expires_at=expires_at,
        )
        invitation = self.invitation_repo.create(invitation_create)

        return invitation

    def validate_invitation(self, token: str) -> InvitationValidateResponse:
        """
        Validate an invitation token and return details.

        Args:
            token: The invitation token to validate

        Returns:
            InvitationValidateResponse: Validation result with invitation details

        Raises:
            HTTPException: If token format is invalid (400)
                or invitation not found (404)
        """
        # Validate token format before database query
        self._validate_token_format(token)

        # Get invitation schema
        invitation = self.invitation_repo.get_by_token(token)

        if not invitation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invitation not found",
            )

        # Check if invitation is valid
        if not self.is_valid(invitation):
            # Determine reason for invalidity
            if invitation.status == InvitationStatus.ACCEPTED:
                reason = "This invitation has already been accepted"
            elif invitation.status == InvitationStatus.REVOKED:
                reason = "This invitation has been revoked"
            elif invitation.expires_at < datetime.now(timezone.utc):
                reason = "This invitation has expired"
                # Mark as expired if not already marked
                if invitation.status == InvitationStatus.PENDING:
                    self.mark_as_expired(invitation.id)
            else:
                reason = "This invitation is not valid"

            return InvitationValidateResponse(
                valid=False,
                reason=reason,
            )

        # Fetch organization for response
        organization = self.org_repo.get_by_id(invitation.organization_id)

        return InvitationValidateResponse(
            valid=True,
            email=invitation.email,
            organization_id=str(invitation.organization_id),
            organization_name=organization.name if organization else None,
            organization_role=invitation.organization_role,
        )

    def accept_invitation(self, token: str, password: str) -> TokenWithUser:
        """
        Accept an invitation and create user account.

        Creates a new user if one doesn't exist with the invitation email,
        and creates a UserOrganization association. For EMPLOYEE/ADMIN roles,
        UserStore entries may be created separately by admins.

        Args:
            token: The invitation token
            password: Password for the new/existing user account

        Returns:
            TokenWithUser: Access token and user information

        Raises:
            HTTPException: If token format is invalid (400), invitation not found (404),
                          invalid, expired, or already accepted (400)
        """
        # Validate token format before database query
        self._validate_token_format(token)

        # Get invitation schema
        invitation = self.invitation_repo.get_by_token(token)

        if not invitation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invitation not found",
            )

        # Validate invitation
        if not self.is_valid(invitation):
            if invitation.status == InvitationStatus.ACCEPTED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This invitation has already been accepted",
                )
            elif invitation.status == InvitationStatus.REVOKED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This invitation has been revoked",
                )
            elif invitation.expires_at < datetime.now(timezone.utc):
                self.mark_as_expired(invitation.id)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This invitation has expired",
                )

        # Find or create user
        user = self.user_repo.get_by_email(invitation.email)

        if not user:
            # Create new user with email
            # Note: User model needs password_hash field - will be added via migration
            # For now, we'll create user without password (phone is required)
            # TODO: Add password_hash field to User model via migration
            # Generate a temporary phone number (required field)
            temp_phone = f"+1{secrets.randbelow(10**9):09d}"
            user_create = UserCreate(
                email=invitation.email,
                phone=temp_phone,
            )
            user = self.user_repo.create(user_create)
            # Set password hash when password_hash field is available
            # user.password_hash = get_password_hash(password)
        else:
            # Update existing user password if password_hash field exists
            # user.password_hash = get_password_hash(password)
            # For now, we skip password update as password_hash field doesn't exist
            pass

        # Create user-organization association if it doesn't exist
        existing_user_org = self.user_org_repo.find_by_user_and_organization(
            user.id, invitation.organization_id
        )

        if not existing_user_org:
            user_org_create = UserOrganizationCreate(
                user_id=user.id,
                organization_id=invitation.organization_id,
                role=invitation.organization_role,
            )
            self.user_org_repo.create(user_org_create)

        # Mark invitation as accepted using repository
        self.invitation_repo.mark_as_accepted(invitation.id, datetime.now(timezone.utc))

        # Generate access token - user is already a UserRead schema
        access_token = create_access_token(subject=str(user.id))
        return TokenWithUser(
            access_token=access_token,
            token_type="bearer",
            user=user,
        )
