import os
from pathlib import Path
from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "modus_ai.db"


class Settings(BaseSettings):
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    DATABASE_URL: str = f"sqlite:///{DB_PATH}"
    RESEARCH_ENABLED: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    model_config = {"extra": "ignore"}


settings = Settings()
