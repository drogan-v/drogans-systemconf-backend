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

    DATABASE_URL: str = Field(default="")

    class Config:
        env_file = str(Path("__file__").cwd() / ".env")
    
    def __init__(self, **data):
        super().__init__(**data)
        # Генерируем DATABASE_URL после загрузки остальных полей
        self.DATABASE_URL = self._generate_db_url()
    
    def _generate_db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
