from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal


class ItemBase(BaseModel):
    item_name: str
    item_price: Decimal
    item_description: str | None = None


class Item(ItemBase):
    item_id: UUID

    class Config:
        orm_mode = True
