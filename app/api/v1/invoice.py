import json
from typing import Annotated

from fastapi import APIRouter, Depends, Header
from telegram import Bot, LabeledPrice

from app.dependencies import telegram_bot
from app.schemas.item import ItemResponse
from app.schemas.invoice import Invoice
from app.core.config import Settings

router = APIRouter(prefix="", tags=["Invoice"])


@router.post("/make_invoice")
async def make_invoice(
    x_telegram_webapp_initdata: Annotated[str, Header()], 
    item: ItemResponse,
    bot: Bot = Depends(telegram_bot)
) -> Invoice:
    settings = Settings() # type: ignore
    try:
        print(len(item.model_dump_json().encode('utf-8')))
        invoice_link = await bot.create_invoice_link(
            title=item.item_name,
            description=item.item_description if item.item_description else "",
            payload=json.dumps({
                "item_id": str(item.item_id)
            }),
            provider_token=settings.PAYMENT_PROVIDER_TOKEN,
            currency="RUB",
            prices=[
                LabeledPrice(label=item.item_name, amount=int(item.item_price * 100)),
                LabeledPrice(label="Доставка", amount=5000),
            ],
            need_name=True,
            need_phone_number=True,
        )
    except Exception as e:
        raise Exception("make invoice\n" + str(e))
    return Invoice(invoice_link=invoice_link)
