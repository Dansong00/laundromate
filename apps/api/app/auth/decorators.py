"""Authentication and authorization decorators for API endpoints."""

from functools import wraps
from typing import Callable

from fastapi import HTTPException, status


def require_auth(func: Callable) -> Callable:
    """Decorator to require authentication for an endpoint.

    This decorator validates that current_user is authenticated.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        current_user = kwargs.get('current_user')

        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )

        return await func(*args, **kwargs)

    return wrapper


def require_admin(func: Callable) -> Callable:
    """Decorator to require admin privileges for an endpoint.

    This decorator validates that current_user is an admin.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        current_user = kwargs.get('current_user')

        if not current_user or not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin privileges required"
            )

        return await func(*args, **kwargs)

    return wrapper


def require_owner_or_admin(func: Callable) -> Callable:
    """Decorator to require ownership or admin privileges.

    This decorator validates that current_user owns the resource
    or is an admin.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        current_user = kwargs.get('current_user')
        resource_user_id = kwargs.get('user_id') or kwargs.get('customer_id')

        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )

        if not current_user.is_admin and current_user.id != resource_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this resource"
            )

        return await func(*args, **kwargs)

    return wrapper
