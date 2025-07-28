from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class OrderItemBase(BaseModel):
    order_id: UUID
    item_id: UUID
    order_item_quantity: int
    order_item_price: Decimal


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    order_item_id: UUID

    class Config:
        from_attributes = True


class OrderItemResponse(OrderItem):
    pass
