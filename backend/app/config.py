from pathlib import Path
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# backend/
BACKEND_DIR = Path(__file__).resolve().parent.parent

# backend/.env
ENV_FILE = BACKEND_DIR / ".env"


class Settings(BaseSettings):
    PROJECT_NAME: str = "RecallMeet AI"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "*"
    ]

    # Hindsight Configuration
    HINDSIGHT_API_KEY: str = Field(
        default="",
        description="API Key for Hindsight Cloud"
    )

    HINDSIGHT_BASE_URL: str = Field(
        default="https://api.hindsight.vectorize.io",
        description="Base URL of Hindsight Server or Cloud"
    )

    HINDSIGHT_BANK_ID: str = Field(
        default="recallmeet-demo",
        description="Default Hindsight memory bank ID"
    )

    HINDSIGHT_TIMEOUT: int = 15

    # Groq AI Configuration
    GROQ_API_KEY: str = Field(
        default="",
        description="API key for Groq Cloud"
    )

    GROQ_MODEL: str = Field(
        default="llama-3.3-70b-versatile",
        description="Groq model ID"
    )

    # Local Storage Fallback / Store path
    DATA_DIR: str = "data"

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()