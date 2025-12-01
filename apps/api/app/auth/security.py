import secrets
import string
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID as UUIDType

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config.settings import settings
from app.core.database.session import get_db
from app.core.models.user import User


def generate_otp(length: int = 6) -> str:
    """Generate a random numeric OTP"""
    return "".join(secrets.choice(string.digits) for _ in range(length))


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    expire_minutes = expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    to_encode = {"sub": subject, "exp": expire}
    token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return token


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )


# OAuth2 scheme for token authentication
oauth2_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Get the current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT token
        payload = decode_access_token(credentials.credentials)
        subject = payload.get("sub")
        if subject is None:
            raise credentials_exception
        # Treat subject as user ID (UUID)
        user_id = UUIDType(str(subject))
    except (JWTError, ValueError) as exc:
        raise credentials_exception from exc

    # Get user from database by ID
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user


def is_super_admin(user: User) -> bool:
    """Check if user is a super admin."""
    return user.is_super_admin


def is_admin_or_super_admin(user: User) -> bool:
    """Check if user is an admin or super admin."""
    return user.is_admin or user.is_super_admin
