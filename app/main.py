from contextlib import asynccontextmanager
from typing import AsyncGenerator

from .api.v1 import invoice, webhook, item, order_item
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from telegram import Bot

from .core.config import Settings
from .db.session import engine, Base



async def set_webhook(bot: Bot, webhook_secret: str):
    webhook_url = "https://g40sl192-8000.euw.devtunnels.ms/webhook"
    await bot.set_webhook(url=webhook_url, secret_token=webhook_secret)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings = Settings()  # type: ignore
    app.state.bot = Bot(token=settings.TG_TOKEN)
    await set_webhook(app.state.bot, settings.WEBHOOK_SECRET)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
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
app.include_router(invoice.router)
app.include_router(webhook.router)
app.include_router(item.router)

@app.get("/")
async def root():
    return {"status": "ok"}
