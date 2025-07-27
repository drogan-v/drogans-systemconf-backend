from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


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