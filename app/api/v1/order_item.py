from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import get_object_or_404
from app.db.models.order_item import OrderItem
from app.db.session import get_db_session
from app.schemas.order_item import OrderItemResponse

router = APIRouter(prefix="", tags=["Order Item"])


@router.get(
    "/orders/{order_id}/items",
    response_model=List[OrderItemResponse],
    description="Get all items of order",
    summary="Get all items of order",
)
async def get_order_items(order_id: str, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(OrderItem).where(OrderItem.order_id == order_id))
    items = get_object_or_404(result.scalars().all(), detail="Order items not found")
    return items


@router.get(
    "/orders/{order_id}/items/{item_id}",
    response_model=OrderItemResponse,
    description="Get item of order by item_id",
    summary="Get item of order",
)
async def get_order_item(
    order_id: str, item_id: str, db: AsyncSession = Depends(get_db_session)
):
    result = await db.execute(
        select(OrderItem).where(
            OrderItem.order_id == order_id, OrderItem.item_id == item_id
        )
    )
    item = get_object_or_404(result.scalar_one_or_none(), detail="Order item not found")
    return item
