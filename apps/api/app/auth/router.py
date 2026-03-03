from fastapi import APIRouter, Depends

from app.auth.security import get_current_user
from app.core.dependencies import get_invitation_service
from app.core.models.user import User
from app.core.schemas.invitation import (
    InvitationAcceptRequest,
    InvitationValidateResponse,
)
from app.core.schemas.user import TokenWithUser, UserRead
from app.core.services.invitation_service import InvitationService

router = APIRouter()


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)) -> UserRead:
    return current_user


@router.get("/invitations/{token}/validate", response_model=InvitationValidateResponse)
def validate_invitation(
    token: str,
    invitation_service: InvitationService = Depends(get_invitation_service),
) -> InvitationValidateResponse:
    """
    Validate an invitation token.

    Returns invitation details if valid, or error reason if invalid.
    """
    return invitation_service.validate_invitation(token)


@router.post("/invitations/{token}/accept", response_model=TokenWithUser)
def accept_invitation(
    token: str,
    payload: InvitationAcceptRequest,
    invitation_service: InvitationService = Depends(get_invitation_service),
) -> TokenWithUser:
    """
    Accept an invitation and create user account.

    Creates a new user if one doesn't exist with the invitation email,
    or associates existing user with the store.
    """
    return invitation_service.accept_invitation(token, payload.password)
