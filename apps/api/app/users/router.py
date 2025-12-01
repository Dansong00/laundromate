from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.decorators import require_auth, require_super_admin
from app.auth.security import get_current_user
from app.core.database.session import get_db
from app.core.models.user import User
from app.core.schemas.user import (
    UserActivateRequest,
    UserCreateByAdmin,
    UserRead,
    UserUpdate,
)

router = APIRouter()


@router.get("", response_model=List[UserRead])
@require_auth
@require_super_admin
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """List all users with pagination (super admin only)"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserRead)
@require_auth
@require_super_admin
async def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """Get a specific user by ID (super admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
@require_auth
@require_super_admin
async def create_user(
    user_data: UserCreateByAdmin,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """Create a new user (super admin only)"""
    # Check if user with phone already exists
    existing_user = db.query(User).filter(User.phone == user_data.phone).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this phone number already exists",
        )

    # Check if user with email already exists (if email provided)
    if user_data.email:
        existing_email_user = (
            db.query(User).filter(User.email == user_data.email).first()
        )
        if existing_email_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

    # Create user
    user = User(**user_data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.put("/{user_id}", response_model=UserRead)
@require_auth
@require_super_admin
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """Update a user (super admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Prevent self-demotion from super_admin
    if user_id == current_user.id and user_data.is_super_admin is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove super admin privileges from yourself",
        )

    # Check for duplicate phone if phone is being updated
    if user_data.phone and user_data.phone != user.phone:
        existing_phone_user = (
            db.query(User).filter(User.phone == user_data.phone).first()
        )
        if existing_phone_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this phone number already exists",
            )

    # Check for duplicate email if email is being updated
    if user_data.email and user_data.email != user.email:
        existing_email_user = (
            db.query(User).filter(User.email == user_data.email).first()
        )
        if existing_email_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

    # Update fields
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@require_auth
@require_super_admin
async def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Delete/deactivate a user (super admin only) - soft delete by setting is_active=False
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Prevent self-deletion
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete yourself"
        )

    # Soft delete - set is_active to False
    user.is_active = False  # type: ignore
    db.commit()
    return None


@router.patch("/{user_id}/activate", response_model=UserRead)
@require_auth
@require_super_admin
async def toggle_user_active(
    user_id: UUID,
    request: UserActivateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """Activate or deactivate a user (super admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user.is_active = request.is_active  # type: ignore
    db.commit()
    db.refresh(user)
    return user
