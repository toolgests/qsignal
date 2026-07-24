
"""
Q Signals - Request ID Middleware

Assigns a unique Request ID to every incoming request.
"""

from uuid import uuid4

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware that assigns a unique Request ID
    to every HTTP request.
    """

    async def dispatch(self, request: Request, call_next):
        # Generate unique request ID
        request_id = str(uuid4())

        # Store it for downstream access
        request.state.request_id = request_id

        # Process request
        response = await call_next(request)

        # Include Request ID in response headers
        response.headers["X-Request-ID"] = request_id

        return response


def setup_request_id(app: FastAPI) -> None:
    """
    Register Request ID middleware.
    """

    app.add_middleware(RequestIDMiddleware)

