from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_async_session
from app.db.models.item import Item
from app.schemas.item import ItemResponse
from app.core.exceptions import get_object_or_404

router = APIRouter(prefix='', tags=["Item"])

@router.get("/items", response_model=List[ItemResponse],
            description="Get all items", summary="Get all items")
async def get_items(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Item))
    items = get_object_or_404(result.scalars().all(), detail="Items not found")
    return items

@router.get("/items/{item_id}", response_model=ItemResponse,
            description="Get item by item_id", summary="Get item")
async def get_item(item_id: str, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(
        select(Item).where(Item.item_id == item_id)
    )
    item = get_object_or_404(result.scalar_one_or_none(), detail="Item not found")
    return item