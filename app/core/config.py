from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "URL Shortener & Analytics Service"
    app_env: str = "development"
    base_url: str = "http://localhost:8000"

    database_url: str = "postgresql+psycopg://postgres:postgres@postgres:5432/url_shortener"
    redis_url: str = "redis://redis:6379/0"
    redis_ttl_seconds: int = 3600

    short_code_length: int = 7

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
