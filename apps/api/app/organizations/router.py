"""Organization router for Super-Admin Dashboard."""
from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth.decorators import require_auth, require_super_admin
from app.auth.security import get_current_user
from app.core.constants import DEFAULT_LIMIT, DEFAULT_SKIP, MAX_LIMIT, MIN_LIMIT
from app.core.database.session import get_db
from app.core.dependencies import get_email_service, get_invitation_service
from app.core.models.user import User
from app.core.repositories.organization_repository import OrganizationRepository
from app.core.schemas.invitation import InvitationRead, InviteMemberRequest
from app.core.schemas.organization import (
    OrganizationCreate,
    OrganizationRead,
    OrganizationUpdate,
)
from app.core.services.email_service import EmailService
from app.core.services.invitation_service import InvitationService

router = APIRouter()


@router.get("", response_model=List[OrganizationRead])
@require_auth
@require_super_admin
async def list_organizations(
    skip: int = Query(DEFAULT_SKIP, ge=DEFAULT_SKIP),
    limit: int = Query(DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
    status: str | None = Query(None, description="Filter by status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """List all organizations with optional filtering and pagination."""
    repo = OrganizationRepository(db)
    return repo.list(skip=skip, limit=limit, status=status)


@router.get("/{organization_id}", response_model=OrganizationRead)
@require_auth
@require_super_admin
async def get_organization(
    organization_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrganizationRead:
    """Get a specific organization by ID."""
    repo = OrganizationRepository(db)
    org = repo.get_by_id(organization_id)

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    return org


@router.post("", response_model=OrganizationRead, status_code=status.HTTP_201_CREATED)
@require_auth
@require_super_admin
async def create_organization(
    org_data: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrganizationRead:
    """Create a new organization."""
    repo = OrganizationRepository(db)
    return repo.create(org_data)


@router.put("/{organization_id}", response_model=OrganizationRead)
@require_auth
@require_super_admin
async def update_organization(
    organization_id: UUID,
    org_data: OrganizationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrganizationRead:
    """Update an existing organization."""
    repo = OrganizationRepository(db)
    return repo.update(organization_id, org_data)


@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
@require_auth
@require_super_admin
async def delete_organization(
    organization_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete an organization."""
    repo = OrganizationRepository(db)
    deleted = repo.delete(organization_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )


@router.post(
    "/{organization_id}/invite-member",
    response_model=InvitationRead,
    status_code=status.HTTP_201_CREATED,
)
@require_auth
@require_super_admin
async def invite_organization_member(
    organization_id: UUID,
    payload: InviteMemberRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    invitation_service: InvitationService = Depends(get_invitation_service),
    email_service: EmailService = Depends(get_email_service),
) -> InvitationRead:
    """Invite an organization member via email."""
    # Verify organization exists
    org_repo = OrganizationRepository(db)
    org = org_repo.get_by_id(organization_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    # Create invitation using service
    invitation = invitation_service.create_invitation(
        email=payload.email,
        organization_id=organization_id,
        organization_role=payload.organization_role,
        invited_by=current_user.id,
    )

    # Send invitation email
    try:
        expiration_days = invitation_service.get_expiration_days()
        # Email template uses store_name but we'll use organization name
        # TODO: Update email templates to be organization-focused
        email_service.send_invitation_email(
            to_email=payload.email,
            store_name=org.name,  # Using org name as placeholder
            organization_name=org.name,
            invitation_token=invitation.token,
            expiration_days=expiration_days,
        )
    except Exception as e:
        # Log error but don't fail the request
        # The invitation is already created in the database
        print(f"Failed to send invitation email: {e}")

    return invitation
