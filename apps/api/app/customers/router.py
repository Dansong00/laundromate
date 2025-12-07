from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.decorators import require_admin, require_auth, require_owner_or_admin
from app.auth.security import get_current_user
from app.core.database.session import get_db
from app.core.models.customer import Customer
from app.core.models.user import User
from app.core.schemas.customer import (
    CustomerCreate,
    CustomerRead,
    CustomerUpdate,
    CustomerWithAddresses,
)

router = APIRouter()


@router.get("", response_model=List[CustomerRead])
@require_auth
@require_admin
async def list_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """List all customers with pagination"""

    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers


@router.get("/me", response_model=CustomerWithAddresses)
@require_auth
async def get_current_customer(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> CustomerWithAddresses:
    """Get current user's customer profile"""
    customer = db.query(Customer).filter(Customer.user_id == current_user.id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer profile not found"
        )
    return customer


@router.get("/{customer_id}", response_model=CustomerRead)
@require_auth
@require_owner_or_admin
async def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CustomerRead:
    """Get a specific customer by ID"""

    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return customer


@router.post("", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
@require_auth
@require_owner_or_admin
async def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CustomerRead:
    """Create a new customer profile"""
    # Check if customer already exists for this user
    existing_customer = (
        db.query(Customer).filter(Customer.user_id == customer_data.user_id).first()
    )
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer profile already exists for this user",
        )

    # Verify user exists
    user = db.query(User).filter(User.id == customer_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Create customer
    customer = Customer(**customer_data.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


@router.put("/{customer_id}", response_model=CustomerRead)
@require_auth
@require_owner_or_admin
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CustomerRead:
    """Update a customer profile"""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )

    # Update fields
    update_data = customer_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)
    return customer


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
@require_auth
@require_admin
async def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a customer profile (admin only)"""

    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )

    db.delete(customer)
    db.commit()
    return None
