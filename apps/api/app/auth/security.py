from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID as UUIDType

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config.settings import settings
from app.core.database.session import get_db
from app.core.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    expire_minutes = expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    to_encode = {"sub": subject, "exp": expire}
    token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return str(token)


def decode_access_token(token: str) -> dict:
    return dict(
        jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    )


# OAuth2 scheme for token authentication
oauth2_scheme = HTTPBearer()


def _resolve_user_from_idp_payload(
    db: Session, payload: dict, credentials_exception: HTTPException
) -> User:
    """Resolve or create User from IdP (Clerk) JWT payload."""
    sub = payload.get("sub")
    if not sub:
        raise credentials_exception
    email = payload.get("email") or (
        payload.get("email_address")
        if isinstance(payload.get("email_address"), str)
        else None
    )
    first_name = payload.get("first_name") or payload.get("given_name")
    last_name = payload.get("last_name") or payload.get("family_name")

    user = (
        db.query(User)
        .filter(
            User.auth_provider == "clerk",
            User.auth_provider_sub == sub,
        )
        .first()
    )
    if user:
        return user
    # Link existing user by email if present
    if email:
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.auth_provider = "clerk"
            user.auth_provider_sub = sub
            if first_name is not None:
                user.first_name = first_name
            if last_name is not None:
                user.last_name = last_name
            db.commit()
            db.refresh(user)
            return user
    # Create new user (placeholder phone; IdP identity only)
    user = User(
        phone=f"+idp-{sub}",
        email=email or None,
        first_name=first_name,
        last_name=last_name,
        auth_provider="clerk",
        auth_provider_sub=sub,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Get the current authenticated user from JWT token (Clerk or our own)."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = credentials.credentials

    # 1. Try Clerk / IdP token if configured
    from app.auth.idp_jwt import decode_idp_token

    idp_payload = decode_idp_token(token)
    if idp_payload is not None:
        return _resolve_user_from_idp_payload(db, idp_payload, credentials_exception)

    # 2. Fall back to our own JWT (invitation flow, etc.)
    try:
        payload = decode_access_token(token)
        subject = payload.get("sub")
        if subject is None:
            raise credentials_exception
        user_id = UUIDType(str(subject))
    except (JWTError, ValueError) as exc:
        raise credentials_exception from exc

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user


def is_super_admin(user: User) -> bool:
    """Check if user is a super admin."""
    return bool(user.is_super_admin)


def is_admin_or_super_admin(user: User) -> bool:
    """Check if user is an admin or super admin."""
    return bool(user.is_admin or user.is_super_admin)


def is_support_agent(user: User) -> bool:
    """Check if user is a support agent or super admin."""
    return bool(user.is_super_admin or user.is_support_agent)


def is_provisioning_specialist(user: User) -> bool:
    """Check if user is a provisioning specialist or super admin."""
    return bool(user.is_super_admin or user.is_provisioning_specialist)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bool(pwd_context.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    return str(pwd_context.hash(password))
