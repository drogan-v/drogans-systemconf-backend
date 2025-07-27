from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class OrderBase(BaseModel):
    user_id: int


class Order(OrderBase):
    order_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
