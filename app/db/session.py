from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import Settings

settings = Settings()  # type: ignore


class Base(DeclarativeBase):
    pass


engine = create_async_engine(str(settings.DATABASE_URL), echo=False)

async_session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость для получения асинхронной сессии базы данных.
    """
    async with async_session_maker() as session:
        yield session
