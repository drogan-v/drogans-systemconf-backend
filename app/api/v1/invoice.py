from typing import Annotated

from fastapi import APIRouter, Depends, Header
from telegram import Bot, LabeledPrice

from app.dependencies import telegram_bot
from app.schemas.product import Product
from app.schemas.invoice import Invoice
from app.core.config import Settings

router = APIRouter(prefix="", tags=["Invoice"])


@router.post("/make_invoice")
async def make_invoice(
    x_telegram_webapp_initdata: Annotated[str, Header()], 
    product: Product,
    bot: Bot = Depends(telegram_bot)
) -> Invoice:
    settings = Settings() # type: ignore
    invoice_link = await bot.create_invoice_link(
        title=product.product_name,
        description=product.description if product.description else "",
        payload=settings.PAYLOAD_SECRET,
        provider_token=settings.PAYMENT_PROVIDER_TOKEN,
        currency="RUB",
        prices=[
            LabeledPrice(label=product.product_name, amount=product.price * 100),
            LabeledPrice(label="Доставка", amount=5000),
        ],
        need_name=True,
        need_phone_number=True,
    )
    return Invoice(invoice_link=invoice_link)
