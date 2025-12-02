from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.decorators import require_auth
from app.auth.security import get_current_user
from app.core.database.session import get_db
from app.core.models.order import Order
from app.core.models.user import User
from app.core.schemas.order import OrderCreate, OrderRead, OrderUpdate, OrderWithDetails

router = APIRouter()


@router.get("", response_model=List[OrderRead])
@require_auth
async def list_orders(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> Any:
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders


@router.get("/{order_id}", response_model=OrderRead)
@require_auth
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> OrderRead:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return order


@router.get("/{order_id}/detail", response_model=OrderWithDetails)
@require_auth
async def get_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> OrderWithDetails:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    # relationships will load lazily when accessed if configured; return as is
    return order


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
@require_auth
async def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> OrderRead:
    # Basic validation: addresses belong to the customer
    from app.core.models.address import Address

    pickup_addr = (
        db.query(Address)
        .filter(
            Address.id == payload.pickup_address_id,
            Address.customer_id == payload.customer_id,
        )
        .first()
    )
    delivery_addr = (
        db.query(Address)
        .filter(
            Address.id == payload.delivery_address_id,
            Address.customer_id == payload.customer_id,
        )
        .first()
    )
    if not pickup_addr or not delivery_addr:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Addresses must belong to the customer",
        )

    # Create order number (simple placeholder)
    from datetime import datetime as dt

    order_number = f"ORD-{int(dt.utcnow().timestamp())}"

    order = Order(
        order_number=order_number,
        customer_id=payload.customer_id,
        status="pending",
        total_amount=0.0,
        tax_amount=0.0,
        tip_amount=0.0,
        final_amount=0.0,
        pickup_address_id=payload.pickup_address_id,
        pickup_date=payload.pickup_date,
        pickup_time_slot=payload.pickup_time_slot,
        pickup_instructions=payload.pickup_instructions,
        delivery_address_id=payload.delivery_address_id,
        delivery_date=payload.delivery_date,
        delivery_time_slot=payload.delivery_time_slot,
        delivery_instructions=payload.delivery_instructions,
        special_requests=payload.special_requests,
        is_rush_order=payload.is_rush_order,
        rush_fee=payload.rush_fee,
    )
    db.add(order)
    db.flush()

    # Add items and compute totals
    from app.core.models.order_item import OrderItem

    total = 0.0
    for item in payload.items:
        item_total = item.unit_price * max(1, item.quantity)
        total += item_total
        db.add(
            OrderItem(
                order_id=order.id,
                service_id=item.service_id,
                item_name=item.item_name,
                item_type=item.item_type,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item_total,
                weight=item.weight,
                special_instructions=item.special_instructions,
                fabric_type=item.fabric_type,
                color=item.color,
            )
        )

    order.total_amount = total  # type: ignore
    order.final_amount = float(
        total + (float(order.tax_amount or 0.0)) + (float(order.rush_fee or 0.0))
    )  # type: ignore[assignment]

    db.commit()
    db.refresh(order)
    return order


@router.put("/{order_id}/status", response_model=OrderRead)
@require_auth
async def update_order_status(
    order_id: int,
    status_value: str,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> OrderRead:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    order.status = status_value  # type: ignore
    db.commit()
    db.refresh(order)
    return order


@router.put("/{order_id}", response_model=OrderRead)
@require_auth
async def update_order(
    order_id: int,
    payload: OrderUpdate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> OrderRead:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)
    db.commit()
    db.refresh(order)
    return order
