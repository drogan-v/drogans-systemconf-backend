from pydantic import Field
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    TG_TOKEN: str = Field()
    PAYMENT_PROVIDER_TOKEN: str = Field()
    WEBHOOK_SECRET: str = Field()
    PAYLOAD_SECRET: str = Field()

    POSTGRES_USER: str = Field()
    POSTGRES_DB: str = Field()
    POSTGRES_PASSWORD: str = Field()
    POSTGRES_HOST: str = Field()
    POSTGRES_PORT: str = Field()

    REDIS_DB: int = Field()
    REDIS_PASSWORD: str = Field()
    REDIS_HOST: str = Field()
    REDIS_PORT: str = Field()

    DATABASE_URL: str = Field(default="")
    REDIS_URL: str = Field(default="")

    class Config:
        env_file = str(Path("__file__").cwd() / ".env")
    
    def __init__(self, **data):
        super().__init__(**data)
        # Генерируем DATABASE_URL после загрузки остальных полей
        self.DATABASE_URL = self._generate_postgres_db_url()
        self.REDIS_URL = self._generate_redis_db_url()
    
    def _generate_postgres_db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    def _generate_redis_db_url(self) -> str:
        return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
