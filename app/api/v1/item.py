from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.item import Item
from app.db.session import get_db_session
from app.schemas.item import ItemCreate, ItemResponse

router = APIRouter(prefix="/item", tags=["Item"])


@router.post("")
async def create_item(
    item_create: ItemCreate, session: AsyncSession = Depends(get_db_session)
) -> ItemResponse:
    item = Item(
        item_name=item_create.item_name,
        item_price=item_create.item_price,
        item_description=item_create.item_description,
    )
    session.add(item)
    await session.commit()
    return ItemResponse.model_validate(item)


@router.get("/{item_id}")
async def get_item(
    item_id: UUID4, session: AsyncSession = Depends(get_db_session)
) -> ItemResponse:
    item = await session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse.model_validate(item)


@router.get("")
async def get_items(
    session: AsyncSession = Depends(get_db_session),
) -> List[ItemResponse]:
    try:
        result = (await session.execute(select(Item))).scalars().all()
        return [ItemResponse.model_validate(item) for item in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching items: {str(e)}")
