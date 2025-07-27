from pydantic import BaseModel
from uuid import UUID


class ShippingAddressBase(BaseModel):
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str


class ShippingAddress(ShippingAddressBase):
    shipping_address_id: UUID

    class Config:
        orm_mode = True
