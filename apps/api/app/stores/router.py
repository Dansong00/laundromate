"""Store router for Super-Admin Dashboard."""
from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth.decorators import require_auth, require_super_admin
from app.auth.security import get_current_user
from app.core.constants import DEFAULT_LIMIT, DEFAULT_SKIP, MAX_LIMIT, MIN_LIMIT
from app.core.database.session import get_db
from app.core.models.organization import Organization
from app.core.models.user import User
from app.core.repositories.store_repository import StoreRepository
from app.core.schemas.store import StoreCreate, StoreRead, StoreUpdate

router = APIRouter()


@router.get("/organizations/{organization_id}/stores", response_model=List[StoreRead])
@require_auth
@require_super_admin
async def list_stores_by_organization(
    organization_id: UUID,
    skip: int = Query(DEFAULT_SKIP, ge=DEFAULT_SKIP),
    limit: int = Query(DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """List all stores for a specific organization."""
    # Verify organization exists
    org = db.query(Organization).filter(Organization.id == organization_id).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    repo = StoreRepository(db)
    return repo.list_by_organization(organization_id, skip=skip, limit=limit)


@router.post(
    "/organizations/{organization_id}/stores",
    response_model=StoreRead,
    status_code=status.HTTP_201_CREATED,
)
@require_auth
@require_super_admin
async def create_store(
    organization_id: UUID,
    store_data: StoreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> StoreRead:
    """Create a new store for an organization."""
    # Verify organization exists
    org = db.query(Organization).filter(Organization.id == organization_id).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    # Ensure store_data.organization_id matches the path parameter
    store_data.organization_id = organization_id

    repo = StoreRepository(db)
    return repo.create(store_data)


@router.get("/{store_id}", response_model=StoreRead)
@require_auth
@require_super_admin
async def get_store(
    store_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> StoreRead:
    """Get a specific store by ID."""
    repo = StoreRepository(db)
    store = repo.get_by_id(store_id)

    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )

    return store


@router.put("/{store_id}", response_model=StoreRead)
@require_auth
@require_super_admin
async def update_store(
    store_id: UUID,
    store_data: StoreUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> StoreRead:
    """Update an existing store."""
    repo = StoreRepository(db)
    return repo.update(store_id, store_data)


@router.delete("/{store_id}", status_code=status.HTTP_204_NO_CONTENT)
@require_auth
@require_super_admin
async def delete_store(
    store_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a store."""
    repo = StoreRepository(db)
    deleted = repo.delete(store_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )
