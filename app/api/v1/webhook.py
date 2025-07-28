import hmac

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from telegram import Bot, Update
from telegram.constants import ParseMode

from app.core.config import Settings
from app.dependencies import telegram_bot
from app.services.pre_checkout_query import save_pre_checkout_query_info

router = APIRouter(prefix="", tags=["Webhook"])


def verify_webhook(request: Request):
    settings = Settings()  # type: ignore
    secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if not secret_token or not hmac.compare_digest(
        secret_token, settings.WEBHOOK_SECRET
    ):
        raise HTTPException(403, "Invalid secret token")


@router.post("/webhook")
async def webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    bot: Bot = Depends(telegram_bot),
):
    try:
        verify_webhook(request)
        data = await request.json()
        update = Update.de_json(data, bot)
        if update.pre_checkout_query:
            await save_pre_checkout_query_info(update.pre_checkout_query)
            await bot.answer_pre_checkout_query(
                pre_checkout_query_id=update.pre_checkout_query.id,
                ok=True,
                error_message="Bad :(",
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
