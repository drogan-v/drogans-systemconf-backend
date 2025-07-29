from fastapi import Request
from telegram import Bot
from redis.asyncio.client import Redis

from app.redis.session import redis_client

async def telegram_bot(request: Request) -> Bot:
    return request.app.state.bot

async def get_redis_session() -> Redis:
    return redis_client
