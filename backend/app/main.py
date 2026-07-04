import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.core.database import connect_to_mongo, close_mongo_connection
from backend.app.api.v1.api import api_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage database connection lifecycle state."""
    logger.info("Initializing app foundation...")
    await connect_to_mongo()
    yield
    logger.info("Cleaning up app resources...")
    await close_mongo_connection()

# Initialize FastAPI App
app = FastAPI(
    title=settings.APP_NAME,
    description="Intelligent system automating campus event registrations using stateful LLM flows.",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register v1 router prefix
app.include_router(api_router, prefix="/api/v1")

@app.get("/health", tags=["Health Checker"])
async def health_check():
    """Health check endpoint to monitor application status."""
    return {"status": "healthy"}
