import uuid
from decimal import Decimal

from pydantic import BaseModel


class ItemBase(BaseModel):
    item_name: str
    item_price: Decimal
    item_description: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    item_id: uuid.UUID

    class Config:
        from_attributes = True


class ItemResponse(Item):
    pass


class ItemsID(BaseModel):
    item_id: uuid.UUID
