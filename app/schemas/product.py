from pydantic import BaseModel


class Product(BaseModel):
    product_id: int
    product_name: str
    price: int
    description: str | None