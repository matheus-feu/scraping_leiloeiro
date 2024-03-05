from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """General Settings"""
    api_version: str
    app_v1_prefix: str
    debug: bool
    project_name: str
    project_description: str
    port: int

    """Model Settings"""
    model_config = SettingsConfigDict(
        env_file="core/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
