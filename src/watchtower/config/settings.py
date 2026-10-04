from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"
    database_url: str = "sqlite:///./watchtower.db"
    log_level: str = "INFO"
    request_timeout_seconds: int = 30
    max_concurrent_watch_runs: int = 3


settings = Settings()
