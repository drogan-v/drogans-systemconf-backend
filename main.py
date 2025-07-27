import hmac
import os
from contextlib import asynccontextmanager
from typing import Annotated

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from telegram import Bot, LabeledPrice, Update
from telegram.constants import ParseMode

load_dotenv(verbose=True)
try:
    TG_TOKEN = os.environ["TG_TOKEN"]
    PAYMENT_PROVIDER_TOKEN = os.environ["PAYMENT_PROVIDER_TOKEN"]
    WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]
    PAYLOAD_SECRET = os.environ["PAYLOAD_SECRET"]
except KeyError:
    raise Exception("Please, define all env vars")


bot = Bot(token=TG_TOKEN)


async def set_webhook():
    webhook_url = "https://g40sl192-8000.euw.devtunnels.ms/webhook"
    await bot.set_webhook(url=webhook_url, secret_token=WEBHOOK_SECRET)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await set_webhook()
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


class Invoice(BaseModel):
    invoice_link: str


class Product(BaseModel):
    product_id: int
    product_name: str
    price: int
    description: str | None


def verify_webhook(request: Request):
    secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if not secret_token or not hmac.compare_digest(secret_token, WEBHOOK_SECRET):
        raise HTTPException(403, "Invalid secret token")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/make_invoice")
async def make_invoice(
    x_telegram_webapp_initdata: Annotated[str, Header()], product: Product
) -> Invoice:
    invoice_link = await bot.create_invoice_link(
        title=product.product_name,
        description=product.description if product.description else "",
        payload=PAYLOAD_SECRET,
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency="RUB",
        prices=[
            LabeledPrice(label=product.product_name, amount=product.price * 100),
            LabeledPrice(label="Доставка", amount=5000),
        ],
        need_name=True,
        need_phone_number=True,
    )
    return Invoice(invoice_link=invoice_link)


@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    try:
        verify_webhook(request)
        data = await request.json()
        update = Update.de_json(data, bot)

        if update.pre_checkout_query:
            await bot.answer_pre_checkout_query(
                pre_checkout_query_id=update.pre_checkout_query.id,
                ok=True,
                error_message="Херово",
            )

        if update.message and update.message.successful_payment:
            payment = update.message.successful_payment
            background_tasks.add_task(
                bot.send_message,
                chat_id=update.message.chat_id,
                text=f"✅ Заказ {payment.invoice_payload} оплачен!",
                parse_mode=ParseMode.HTML,
            )

        return {"ok": True}
    except Exception as e:
        raise Exception("webhook" + str(e))
