from pydantic import BaseModel


class Invoice(BaseModel):
    invoice_link: str
