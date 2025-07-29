from typing import Annotated

from fastapi import APIRouter, Depends, Header
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Bot

from app.core.config import Settings
from app.db.session import get_db_session
from app.dependencies import telegram_bot, get_redis_session
from app.schemas.invoice import Invoice
from app.schemas.item import Item
from app.services.init_data import init_data_is_valid
from app.services.invoice import generate_invoice_link

router = APIRouter(prefix="", tags=["Invoice"])


@router.post("/make_invoice")
async def make_invoice(
    x_telegram_webapp_initdata: Annotated[str, Header()],
    items: list[Item],
    bot: Bot = Depends(telegram_bot),
    session: AsyncSession = Depends(get_db_session),
    redis: Redis = Depends(get_redis_session)
) -> Invoice:
    settings = Settings()  # type: ignore
    try:
        if not init_data_is_valid(x_telegram_webapp_initdata, settings.TG_TOKEN):
            raise Exception("Init data is invalid")
        return Invoice(
            invoice_link=await generate_invoice_link(bot, items, settings, session, redis)
        )
    except Exception as e:
        raise Exception("make invoice: " + str(e))
