from pydantic import BaseModel


class InvoiceBase(BaseModel):
    from_user_id: int
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: str | None = None
    order_info_id: str | None = None


class Invoice(InvoiceBase):
    invoice_id: str

    class Config:
        orm_mode = True
