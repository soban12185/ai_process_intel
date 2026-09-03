import os
from pathlib import Path
from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "modus_ai.db"


class Settings(BaseSettings):
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash-lite"
    DATABASE_URL: str = f"sqlite:///{DB_PATH}"
    RESEARCH_ENABLED: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    model_config = {"extra": "ignore"}


settings = Settings()
