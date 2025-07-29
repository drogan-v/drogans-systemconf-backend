from redis.asyncio import from_url

from app.core.config import Settings

settings = Settings()  # type: ignore

redis_client = from_url(settings.REDIS_URL, decode_responses=True)
