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
    POSTGRES_PORT: str = Field()

    class Config:
        env_file = str(Path("__file__").cwd() / ".env")
