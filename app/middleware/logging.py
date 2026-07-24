"""
Q Signals - Request Logging Middleware

Logs every incoming HTTP request and its response status/latency.
"""

from __future__ import annotations

import time

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.logging import get_logger

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that logs request/response information.
    """

    async def dispatch(self, request: Request, call_next):

        start_time = time.perf_counter()

        response = await call_next(request)

        duration_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        logger.info(
            "HTTP Request",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
            request_id=getattr(request.state, "request_id", None),
        )

        return response


def setup_logging_middleware(app: FastAPI) -> None:
    """
    Register the request logging middleware.
    """

    app.add_middleware(RequestLoggingMiddleware)
