"""
Q Signals Backend

Main FastAPI application entry point.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.background.scheduler import scheduler
from app.core.config import config
from app.logging.logger import configure_logging, get_logger
from app.middleware.cors import setup_cors
from app.middleware.error_handler import setup_exception_handlers
from app.middleware.request_id import setup_request_id
from app.websocket.router import router as websocket_router

configure_logging()

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle.
    """

    # Startup
    logger.info(
        "Q Signals Backend Starting",
        version=config.APP_VERSION,
    )

    await scheduler.start_all()

    yield

    # Shutdown
    await scheduler.stop_all()

    logger.info("Q Signals Backend Stopped")


app = FastAPI(
    title=config.APP_NAME,
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(api_router)
app.include_router(websocket_router)

setup_exception_handlers(app)
setup_request_id(app)

# ---------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------

setup_cors(app)

# ---------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint.
    """
    return {
        "application": config.APP_NAME,
        "status": "running",
        "version": config.APP_VERSION,
    }
