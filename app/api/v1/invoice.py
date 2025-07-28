import json
from typing import Annotated

from fastapi import APIRouter, Depends, Header
from telegram import Bot, LabeledPrice

from app.dependencies import telegram_bot
from app.schemas.item import Item
from app.schemas.invoice import Invoice
from app.core.config import Settings
from app.services.init_data import init_data_is_valid

router = APIRouter(prefix="", tags=["Invoice"])


@router.post("/make_invoice")
async def make_invoice(
    x_telegram_webapp_initdata: Annotated[str, Header()], 
    item: Item,
    bot: Bot = Depends(telegram_bot)
) -> Invoice:
    settings = Settings() # type: ignore
    try:
        if not init_data_is_valid(x_telegram_webapp_initdata, settings.TG_TOKEN):
            raise Exception("Init data is invalid")
        invoice_link = await bot.create_invoice_link(
            title=item.item_name,
            # TODO: ITEM HAS NOT DESCRIPTION. FIX IT!
            description=item.item_description if item.item_description else "fake description",
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
        raise Exception("make invoice: " + str(e))
    return Invoice(invoice_link=invoice_link)
