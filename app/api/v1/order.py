from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db_session
from app.db.models.order import Order
from app.schemas.order import OrderResponse
from app.core.exceptions import get_object_or_404

router = APIRouter(prefix='', tags=["Order"])

@router.get("/orders", response_model=List[OrderResponse],
            description="Get all orders", summary="Get all orders")
async def get_all_orders(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(Order))
    orders = get_object_or_404(result.scalars().all(), detail="Orders not found")
    return orders

@router.get("/orders/{user_id}", response_model=List[OrderResponse],
            description="Get all orders of user by user_id", summary="Get all orders of user")
async def get_orders(user_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(
        select(Order).where(Order.user_id == user_id)
    )
    orders = get_object_or_404(result.scalars().all(), detail="Orders not found")
    return orders

@router.get("/orders/{user_id}/{order_id}", response_model=OrderResponse,
            description="Get order of user by user_id and order_id", summary="Get order of user")
async def get_order(user_id: int, order_id: str, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(
        select(Order).where(
            Order.user_id == user_id,
            Order.order_id == order_id
        )
    )
    order = get_object_or_404(result.scalar_one_or_none(), detail="Order not found")
    return order