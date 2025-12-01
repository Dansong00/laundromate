from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.decorators import require_admin, require_auth
from app.auth.security import get_current_user
from app.core.database.session import get_db
from app.core.models.service import Service
from app.core.models.user import User
from app.core.schemas.service import ServiceCreate, ServiceRead, ServiceUpdate

router = APIRouter()


@router.get("", response_model=List[ServiceRead])
@require_auth
async def list_services(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[ServiceRead]:
    """List all services with optional filtering"""
    query = db.query(Service)

    if active_only:
        query = query.filter(Service.is_active == True)  # noqa: E712

    services = query.offset(skip).limit(limit).all()
    return services


@router.get("/{service_id}", response_model=ServiceRead)
@require_auth
async def get_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ServiceRead:
    """Get a specific service by ID"""
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service not found"
        )
    return service


@router.post("", response_model=ServiceRead, status_code=status.HTTP_201_CREATED)
@require_auth
@require_admin
async def create_service(
    service_data: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ServiceRead:
    """Create a new service (admin only)"""
    # Check if service name already exists
    existing_service = (
        db.query(Service).filter(Service.name == service_data.name).first()
    )
    if existing_service:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Service with this name already exists",
        )

    # Create service
    service = Service(**service_data.dict())
    db.add(service)
    db.commit()
    db.refresh(service)

    return service


@router.put("/{service_id}", response_model=ServiceRead)
@require_auth
@require_admin
async def update_service(
    service_id: int,
    service_data: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ServiceRead:
    """Update a service (admin only)"""

    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service not found"
        )

    # Check if name change conflicts with existing service
    if service_data.name and service_data.name != service.name:
        existing_service = (
            db.query(Service).filter(Service.name == service_data.name).first()
        )
        if existing_service:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Service with this name already exists",
            )

    # Update fields
    update_data = service_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(service, field, value)

    db.commit()
    db.refresh(service)
    return service


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
@require_auth
@require_admin
async def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a service (admin only)"""

    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service not found"
        )

    # Soft delete - just mark as inactive
    service.is_active = False
    db.commit()

    return None


@router.get("/category/{category}", response_model=List[ServiceRead])
@require_auth
async def get_services_by_category(
    category: str,
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[ServiceRead]:
    """Get services by category"""
    query = db.query(Service).filter(Service.category == category)

    if active_only:
        query = query.filter(Service.is_active == True)  # noqa: E712

    services = query.all()
    return services
