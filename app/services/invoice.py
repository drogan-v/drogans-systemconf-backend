import json
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Bot, LabeledPrice

from app.core.config import Settings
from app.db.models.item import Item
from app.schemas.item import Item as ItemSchema


async def generate_invoice_link(
    bot: Bot, items: list[ItemSchema], settings: Settings, session: AsyncSession
) -> str:
    query = await session.execute(
        select(Item).where(Item.item_id.in_([it.item_id for it in items]))
    )
    items_db = query.scalars().all()
    invoice_link = await bot.create_invoice_link(
        title="Ваша покупка",
        description="Лучший магазин техники в мире!",
        payload=json.dumps({"item_id": str(items[0].item_id)}),
        provider_token=settings.PAYMENT_PROVIDER_TOKEN,
        currency="RUB",
        prices=await _generate_prices(items_db),
        need_name=True,
        need_phone_number=True,
    )
    return invoice_link


async def _generate_prices(items: Sequence[Item]) -> list[LabeledPrice]:
    return [
        LabeledPrice(label=f"{it.item_name} x1", amount=int(it.item_price * 100))
        for it in items
    ]
