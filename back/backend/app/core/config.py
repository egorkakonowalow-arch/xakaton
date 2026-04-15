"""
Module: config.py
Layer: Core
Description:
    Loads and validates application configuration from environment variables.
    Provides centralized settings object for all layers.
    Contains no business logic or database access.
Interacts with:
    - .env file
    - core/database.py
    - core/security.py
Called by:
    - main.py
    - service and repository layers via imports
"""

from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./hakaton.db")
    SECRET_KEY: str = Field(default="your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=480)
    UPLOAD_DIR: str = Field(default="uploads/")
    ALGORITHM: str = Field(default="HS256")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    """Returns cached settings object."""

    return Settings()


settings = get_settings()
