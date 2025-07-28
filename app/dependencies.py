from fastapi import Request
from telegram import Bot


async def telegram_bot(request: Request) -> Bot:
    return request.app.state.bot
