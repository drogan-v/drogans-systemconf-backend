from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin
from telegram import Bot

from app.admin import ItemAdmin, OrderAdmin, OrderItemAdmin, UserAdmin

from .api.v1 import invoice, item, order, order_item, user, webhook
from .core.config import Settings
from .redis.session import redis_client
from .db.models.item import Item  # type: ignore
from .db.models.order import Order  # type: ignore
from .db.models.order_item import OrderItem  # type: ignore
from .db.models.user import User  # type: ignore
from .db.session import Base, engine


async def set_webhook(bot: Bot, webhook_url: str, webhook_secret: str):
    await bot.set_webhook(url=webhook_url, secret_token=webhook_secret)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings = Settings()  # type: ignore
    app.state.bot = Bot(token=settings.TG_TOKEN)
    await set_webhook(app.state.bot, webhook_url=settings.WEBHOOK_URL, webhook_secret=settings.WEBHOOK_SECRET)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await redis_client.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
app.include_router(order_item.router)
app.include_router(order.router)
app.include_router(user.router)
app.include_router(item.router)
app.include_router(invoice.router)
app.include_router(webhook.router)

admin = Admin(app, engine, title="Admin Panel")
admin.add_view(ItemAdmin)
admin.add_view(OrderItemAdmin)
admin.add_view(OrderAdmin)
admin.add_view(UserAdmin)


@app.get("/")
async def root():
    return {"status": "ok"}
