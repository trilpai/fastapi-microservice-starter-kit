# app/api/config/settings.py

"""
App-wide settings configuration using Pydantic.

This file centralizes all environment-dependent configurations
(e.g., database URL, environment type, secret keys, debug flags).

Values are loaded automatically from a `.env` file in the project root.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Environment-specific configuration class.

    Automatically reads values from `.env` using Pydantic v2’s
    `SettingsConfigDict` configuration.
    """

    # 🌎 Environment name: "local", "staging", or "prod"
    env: str = "local"

    # 🔗 Database connection URL
    # Examples:
    # - SQLite (dev): sqlite+aiosqlite:///./dev.db
    # - MySQL (prod): mysql+aiomysql://user:pass@host:port/dbname
    database_url: str = ""

    # 📦 SettingsConfig tells Pydantic to load from `.env` file
    model_config = SettingsConfigDict(
        env_file=".env",  # Load from .env in root directory
        extra="ignore",  # Ignore unexpected variables
    )


# 👇 This instance is imported wherever settings are needed
settings = Settings()
