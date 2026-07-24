"""
Q Signals - Rate Limit Middleware

Simple in-memory sliding-window rate limiter, suitable for a
single-process deployment. Swap for a Redis-backed limiter when
scaling horizontally.
"""

from __future__ import annotations

import time
from collections import defaultdict, deque

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    In-memory request rate limiter.
    """

    def __init__(
        self,
        app,
        max_requests: int = 120,
        window_seconds: int = 60,
    ) -> None:
        super().__init__(app)

        self.max_requests = max_requests

        self.window_seconds = window_seconds

        self._hits: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):

        client_ip = request.client.host if request.client else "unknown"

        now = time.monotonic()

        hits = self._hits[client_ip]

        while hits and now - hits[0] > self.window_seconds:
            hits.popleft()

        if len(hits) >= self.max_requests:

            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "error": {
                        "type": "RateLimitExceeded",
                        "message": "Too many requests. Please try again later.",
                    },
                },
            )

        hits.append(now)

        return await call_next(request)


def setup_rate_limit(
    app: FastAPI,
    max_requests: int = 120,
    window_seconds: int = 60,
) -> None:
    """
    Register the rate limiting middleware.
    """

    app.add_middleware(
        RateLimitMiddleware,
        max_requests=max_requests,
        window_seconds=window_seconds,
    )
