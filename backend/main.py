import os
from pathlib import Path

# Load .env BEFORE importing config (so Settings picks up the values)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
env_file = PROJECT_ROOT / ".env"
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file, override=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import init_db
from backend.api import processes, analysis, query
from backend.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="NovaBank AI Process Intelligence Engine",
    description="Enterprise AI Research & Intelligence Engine for Banking Process Analysis",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(processes.router, prefix="/api/processes", tags=["Processes"])
app.include_router(analysis.router, prefix="/api/processes", tags=["Analysis"])
app.include_router(query.router, prefix="/api", tags=["Query"])


@app.on_event("startup")
def startup():
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized.")


@app.get("/health")
def health_check():
    return {"status": "healthy", "app": "NovaBank AI Process Intelligence Engine"}


@app.get("/debug/config")
def debug_config():
    key = settings.GROQ_API_KEY
    return {
        "key_length": len(key) if key else 0,
        "key_prefix": key[:10] + "..." if key and len(key) > 10 else "NOT SET",
        "model": settings.GROQ_MODEL,
    }


@app.get("/debug/test-groq")
def debug_test_groq():
    import httpx
    api_key = settings.GROQ_API_KEY
    if not api_key:
        return {"error": "No API key set"}
    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": settings.GROQ_MODEL, "messages": [{"role": "user", "content": "Say hello"}], "max_tokens": 10},
            )
            return {"status": resp.status_code, "body": resp.text[:500]}
    except Exception as e:
        return {"error": str(e)}
