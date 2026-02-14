import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "expense_db"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    # SQLAlchemy database URL
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/expense_db"

    # App settings
    APP_ENV: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    # Optional: API settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Expense Tracker API"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.APP_ENV.lower() == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.APP_ENV.lower() == "production"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Using lru_cache ensures settings are loaded only once.
    """
    return Settings()


# Convenience instance for direct imports
settings = get_settings()
