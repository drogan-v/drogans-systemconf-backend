from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal


class OrderItemBase(BaseModel):
    order_id: UUID
    item_id: UUID
    order_item_quantity: int
    order_item_price: Decimal

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    order_item_id: UUID

    class Config:
        from_attributes = True
