
"""
Q Signals - CORS Middleware

Centralized Cross-Origin Resource Sharing (CORS) configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import config


def setup_cors(app: FastAPI) -> None:
    """
    Configure Cross-Origin Resource Sharing (CORS).

    Args:
        app: FastAPI application instance.
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

