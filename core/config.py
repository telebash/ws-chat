import os
import logging
# import sentry_sdk
from typing import Any, List, Union

# from sentry_sdk.integrations.logging import LoggingIntegration
from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn, AnyHttpUrl

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
        env_file = "../.env"

    API_V1_STR: str = "/default/api/v1"
    BACKEND_CORS_ORIGINS: List[Union[AnyHttpUrl, str]] = ['*']
    DOMAIN: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week

    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = os.environ['JWT_SECRET_KEY']
    JWT_REFRESH_SECRET_KEY: str = os.environ['JWT_REFRESH_SECRET_KEY']

    WS_ENDPOINT: str = os.environ['WEBSOCKET_API_ENDPOINT']
    BUCKET_NAME: str = os.environ['BUCKET_NAME']

    CP_PUBLIC_ID: str = os.environ['CP_PUBLIC_ID']
    CP_SECRET_KEY: str = os.environ['CP_SECRET_KEY']

    DATABASE_PASSWORD: str = get_env_value('DATABASE_PASSWORD')
    DATABASE_USERNAME: str = get_env_value('DATABASE_USERNAME')
    DATABASE_NAME: str = get_env_value('DATABASE_NAME')
    DATABASE_HOST: str = get_env_value('DATABASE_HOST')
    DATABASE_PORT: int = 5432

    PAYMENT_TOKEN: str = get_env_value('PAYMENT_TOKEN')

    OPENAI_URL: str = get_env_value('OPENAI_URL', 'https://api.openai.com')
    OPENAI_TOKEN: str = get_env_value('OPENAI_TOKEN')

    STABLE_API: str = get_env_value('STABLE_API', 'http://13.53.66.48:7861')

    STABILITY_AI_API: str = get_env_value('STABILITY_API', 'https://api.stability.ai')
    STABILITY_API_KEY: str = get_env_value('STABILITY_API_KEY')

    REPLICATE_API_TOKEN: str = get_env_value('REPLICATE_API_TOKEN')
    REPLICATE_API: str = os.getenv('REPLICATE_API', 'https://api.replicate.com/')

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_SSL: bool

    DATABASE_URL: PostgresDsn | None = None
    SYNC_DATABASE_URL: PostgresDsn | None = None
    WORKERS: int = 3
    PORT: int = 8000
    CURRENCY: str = 'kzt'
    SUBSCRIPTION_AMOUNT: int = 2000000

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: str
    MAIL_SERVER: str
    MAIL_FROM_NAME: str

    def _build_database_url(self):
        return f"{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    def get_sync_database_url(self):
        return self.SYNC_DATABASE_URL or f"postgresql://{self._build_database_url()}"

    def get_async_database_url(self):
        return self.DATABASE_URL or f"postgresql+asyncpg://{self._build_database_url()}"


settings = Settings()
