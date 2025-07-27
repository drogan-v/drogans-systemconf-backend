from pydantic import BaseModel, Field
import uuid
from decimal import Decimal


class ItemBase(BaseModel):
    item_name: str
    item_price: Decimal
    item_description: str | None = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    item_id: uuid.UUID

    class Config:
        from_attributes = True

class ItemResponse(Item):
    pass
