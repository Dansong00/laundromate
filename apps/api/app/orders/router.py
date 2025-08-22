from typing import List

from app.auth.decorators import require_auth
from app.auth.security import get_current_user
from app.core.database.session import get_db
from app.core.models.order import Order
from app.core.models.user import User
from app.core.schemas.order import OrderRead
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("", response_model=List[OrderRead])
@require_auth
async def list_orders(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders


@router.get("/{order_id}", response_model=OrderRead)
@require_auth
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return order
