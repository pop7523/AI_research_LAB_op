from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    app_name: str = "ai-newsroom"
    database_url: str = "sqlite+pysqlite:///./ai_newsroom.db"
    test_database_url: str = "sqlite+pysqlite:///:memory:"
    llm_provider: str = "fake"
    enable_llm_calls: bool = False
    enable_auto_publish: bool = False
    default_language: str = "ko"
    timezone: str = "Asia/Seoul"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()

