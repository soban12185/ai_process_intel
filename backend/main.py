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
