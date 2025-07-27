from pydantic import BaseModel
from uuid import UUID


class OrderInfoBase(BaseModel):
    name: str | None = None
    phone_number: str | None = None
    email: str | None = None
    shipping_address_id: UUID | None = None


class OrderInfo(OrderInfoBase):
    order_info_id: str

    class Config:
        orm_mode = True
