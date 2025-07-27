from contextlib import asynccontextmanager

from .api.v1 import invoice, webhook
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from telegram import Bot

from .core.config import Settings


async def set_webhook(bot: Bot, webhook_secret: str):
    webhook_url = "https://g40sl192-8000.euw.devtunnels.ms/webhook"
    await bot.set_webhook(url=webhook_url, secret_token=webhook_secret)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()  # type: ignore
    app.state.bot = Bot(token=settings.TG_TOKEN)
    await set_webhook(app.state.bot, settings.WEBHOOK_SECRET)
    yield


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


@app.get("/")
async def root():
    return {"message": "Hello World"}
