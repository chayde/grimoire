"""Application configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application
    app_name: str = "Grimoire - Factorio Blueprint Manager"
    app_version: str = "0.1.0"
    debug: bool = True

    # Database
    database_url: str = "postgresql://grimoire:grimoire@localhost/grimoire"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000


# Global settings instance
settings = Settings()
