import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "AI Smart Campus Event Registration Agent"
    DEBUG: bool = False
    ENV: str = "development"

    # MongoDB Configuration
    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "campus_agent_db"

    # Security Configuration
    JWT_SECRET: str = "supersecretkeychangeinproduction"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Google Gemini API
    GEMINI_API_KEY: Optional[str] = None

    # Logging Configuration
    LOG_LEVEL: str = "INFO"

    # CORS Settings
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
        "http://127.0.0.1:5176",
        "https://vercel.app"
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()