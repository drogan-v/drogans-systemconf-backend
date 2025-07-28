from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class OrderBase(BaseModel):
    user_id: int


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    order_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class OrderResponse(Order):
    pass
