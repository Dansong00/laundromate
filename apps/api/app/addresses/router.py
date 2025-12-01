from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.core.database.session import get_db
from app.core.models.address import Address
from app.core.models.customer import Customer
from app.core.models.user import User
from app.core.schemas.address import AddressCreate, AddressRead, AddressUpdate

router = APIRouter()


@router.get("", response_model=List[AddressRead])
async def list_customer_addresses(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """List all addresses for a specific customer"""
    # Check if user can access this customer's addresses
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )

    if not current_user.is_admin and current_user.id != customer.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these addresses",
        )

    addresses = db.query(Address).filter(Address.customer_id == customer_id).all()
    return addresses


@router.get("/{address_id}", response_model=AddressRead)
async def get_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AddressRead:
    """Get a specific address by ID"""
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )

    # Check authorization
    customer = db.query(Customer).filter(Customer.id == address.customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    if not current_user.is_admin and current_user.id != customer.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this address",
        )

    return address


@router.post("", response_model=AddressRead, status_code=status.HTTP_201_CREATED)
async def create_address(
    address_data: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AddressRead:
    """Create a new address for a customer"""
    # Check if user can create addresses for this customer
    customer = (
        db.query(Customer).filter(Customer.id == address_data.customer_id).first()
    )
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )

    if not current_user.is_admin and current_user.id != customer.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create addresses for this customer",
        )

    if address_data.is_default:
        db.query(Address).filter(
            Address.customer_id == address_data.customer_id,
            Address.is_default == True,  # noqa: E712
        ).update({"is_default": False})

    address = Address(**address_data.model_dump())
    db.add(address)
    db.commit()
    db.refresh(address)

    return address


@router.put("/{address_id}", response_model=AddressRead)
async def update_address(
    address_id: int,
    address_data: AddressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AddressRead:
    """Update an address"""
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )

    customer = db.query(Customer).filter(Customer.id == address.customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    if not current_user.is_admin and current_user.id != customer.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this address",
        )

    if address_data.is_default:
        db.query(Address).filter(
            Address.customer_id == address.customer_id,
            Address.id != address_id,
            Address.is_default == True,  # noqa: E712
        ).update({"is_default": False})

    update_data = address_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(address, field, value)

    db.commit()
    db.refresh(address)
    return address


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete an address"""
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )

        customer = db.query(Customer).filter(Customer.id == address.customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    if not current_user.is_admin and current_user.id != customer.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this address",
        )

    db.delete(address)
    db.commit()
    return None
