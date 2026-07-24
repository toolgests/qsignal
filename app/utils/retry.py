"""
Retry Utilities

Simple asynchronous retry decorator with exponential backoff.
"""

from __future__ import annotations

import asyncio
import functools
from typing import Any, Callable, TypeVar

from app.logging import get_logger

logger = get_logger(__name__)

T = TypeVar("T")


def async_retry(
    attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Retry an async function with exponential backoff.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:

            current_delay = delay

            last_exc: Exception | None = None

            for attempt in range(1, attempts + 1):

                try:
                    return await func(*args, **kwargs)

                except exceptions as exc:

                    last_exc = exc

                    logger.warning(
                        "Retrying after failure",
                        function=func.__name__,
                        attempt=attempt,
                        max_attempts=attempts,
                        error=str(exc),
                    )

                    if attempt == attempts:
                        break

                    await asyncio.sleep(current_delay)

                    current_delay *= backoff

            raise last_exc  # type: ignore[misc]

        return wrapper

    return decorator
