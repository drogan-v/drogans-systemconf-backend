from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_async_session
from app.db.models.order import Order
from app.schemas.order import OrderResponse
from app.core.exceptions import get_object_or_404

router = APIRouter(prefix='', tags=["Item"])

@router.get("/orders/{user_id}", response_model=List[OrderResponse])
async def get_items(user_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(
        select(Order).where(Order.user_id == user_id)
    )
    items = get_object_or_404(result.scalars().all(), detail="Orders not found")
    return items

@router.get("/orders/{user_id}/{order_id}", response_model=OrderResponse)
async def get_item(user_id: int, order_id: str, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(
        select(Order).where(
            Order.user_id == user_id,
            Order.order_id == order_id
        )
    )
    item = get_object_or_404(result.scalar_one_or_none(), detail="Order not found")
    return item