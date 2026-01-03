from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.security import create_access_token, generate_otp, get_current_user
from app.core.database.session import get_db
from app.core.dependencies import get_invitation_service
from app.core.models.user import User
from app.core.models.verification_code import VerificationCode
from app.core.schemas.invitation import (
    InvitationAcceptRequest,
    InvitationValidateResponse,
)
from app.core.schemas.user import OTPRequest, OTPVerify, TokenWithUser, UserRead
from app.core.services.invitation_service import InvitationService

router = APIRouter()


@router.post("/otp/request")
def request_otp(payload: OTPRequest, db: Session = Depends(get_db)) -> dict:
    """
    Request an OTP for the given phone number.
    If user doesn't exist, they will be created upon verification.
    """
    # 1. Generate OTP
    code = generate_otp()

    # 2. Store in DB
    # Invalidate old codes for this phone
    db.query(VerificationCode).filter(
        VerificationCode.phone == payload.phone,
        VerificationCode.is_used == False,  # noqa: E712
    ).update({"is_used": True})

    otp_entry = VerificationCode(
        phone=payload.phone,
        code=code,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
    )
    db.add(otp_entry)
    db.commit()

    # 3. Send SMS (Mock for now)
    print(f"🔐 OTP for {payload.phone}: {code}")

    return {"message": "OTP sent successfully"}


@router.post("/otp/verify", response_model=TokenWithUser)
def verify_otp(payload: OTPVerify, db: Session = Depends(get_db)) -> Any:
    """
    Verify the OTP and return an access token.
    Creates a new user if one doesn't exist.
    """
    # 1. Find valid OTP
    otp_record = (
        db.query(VerificationCode)
        .filter(
            VerificationCode.phone == payload.phone,
            VerificationCode.code == payload.code,
            VerificationCode.is_used == False,  # noqa: E712
            VerificationCode.expires_at > datetime.now(timezone.utc),
        )
        .first()
    )

    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP"
        )

    # 2. Mark as used
    otp_record.is_used = True  # type: ignore
    db.commit()

    # 3. Find or Create User
    user = db.query(User).filter(User.phone == payload.phone).first()
    if not user:
        user = User(phone=payload.phone)
        db.add(user)
        db.commit()
        db.refresh(user)

    # 4. Generate Token
    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer", "user": user}


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
