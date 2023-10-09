import os
import logging
# import sentry_sdk
from typing import Any

# from sentry_sdk.integrations.logging import LoggingIntegration
from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn


load_dotenv()


def get_env_value(key: str, default: Any = None) -> str:
    value = os.getenv(key)
    if value is None:
        if default is None:
            raise ValueError(f'Env value not set for {key}')
        return default
    return value


# SENTRY_DSN = get_env_value('SENTRY_DSN', '')
# if SENTRY_DSN:
#     sentry_logging = LoggingIntegration(
#         level=logging.INFO,
#         event_level=logging.WARNING,
#     )
#     sentry_sdk.init(
#         dsn=SENTRY_DSN,
#         integrations=[sentry_logging],
#         traces_sample_rate=1.0
#     )


class Settings(BaseSettings):
    """Настройки приложения"""
    class Config:
        env_file = ".env"

    DATABASE_PASSWORD: str = get_env_value('DATABASE_PASSWORD')
    DATABASE_USERNAME: str = get_env_value('DATABASE_USERNAME')
    DATABASE_NAME: str = get_env_value('DATABASE_NAME')
    DATABASE_HOST: str = get_env_value('DATABASE_HOST')
    DATABASE_PORT: int = 5432

    BOT_TOKEN = get_env_value('BOT_TOKEN')
    TELEGRAM_BOT_URL = get_env_value('TELEGRAM_BOT_URL')
    PAYMENT_TOKEN = get_env_value('PAYMENT_TOKEN')

    OPENAI_URL = get_env_value('OPENAI_URL', 'https://api.openai.com')
    OPENAI_TOKEN = get_env_value('OPENAI_TOKEN')

    STABLE_API = get_env_value('STABLE_API', 'http://13.53.66.48:7861')

    STABILITY_AI_API = get_env_value('STABILITY_API', 'https://api.stability.ai')
    STABILITY_API_KEY = get_env_value('STABILITY_API_KEY')

    REPLICATE_API_TOKEN = get_env_value('REPLICATE_API_TOKEN')
    REPLICATE_API = os.getenv('REPLICATE_API', 'https://api.replicate.com/')

    REDIS_HOST: str = get_env_value('REDIS_HOST')
    REDIS_PORT: int = int(get_env_value('REDIS_PORT'))
    REDIS_PASSWORD: str | None = redis_password if (redis_password := get_env_value('REDIS_PASSWORD', '')) else None
    REDIS_SSL: bool = get_env_value('REDIS_SSL', False) == 'True'

    DATABASE_URL: PostgresDsn | None = None
    SYNC_DATABASE_URL: PostgresDsn | None = None
    WORKERS = 3
    PORT = 8000
    CURRENCY = 'kzt'
    SUBSCRIPTION_AMOUNT = 2000000

    def _build_database_url(self):
        return f"{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    def get_sync_database_url(self):
        return self.SYNC_DATABASE_URL or f"postgresql://{self._build_database_url()}"

    def get_async_database_url(self):
        return self.DATABASE_URL or f"postgresql+asyncpg://{self._build_database_url()}"


settings = Settings()
