from redis.asyncio.client import Redis
from redis.asyncio import from_url
from typing import AsyncGenerator

from app.core.config import Settings

settings = Settings()  # type: ignore

redis_client = from_url(
    settings.REDIS_URL,
    decode_responses=True
)

async def get_redis_session() -> AsyncGenerator[Redis, None]:
    """
    Зависимость FastAPI для получения клиента Redis.
    """
    try:
        yield redis_client
    finally:
        await redis_client.close()
