"""
Cache Service

Lightweight in-memory TTL cache used as a fast lookup layer in
front of provider REST calls. Backed by Redis in the future when
``config.REDIS_ENABLED`` is turned on.
"""

from __future__ import annotations

import time
from typing import Any


class CacheService:
    """
    Simple in-memory cache with per-key TTL.
    """

    def __init__(self) -> None:
        self._store: dict[str, tuple[Any, float | None]] = {}

    def set(self, key: str, value: Any, ttl: float | None = None) -> None:
        """
        Store a value with an optional TTL in seconds.
        """

        expires_at = (time.monotonic() + ttl) if ttl else None

        self._store[key] = (value, expires_at)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a value if present and not expired.
        """

        entry = self._store.get(key)

        if entry is None:
            return default

        value, expires_at = entry

        if expires_at is not None and time.monotonic() > expires_at:
            self._store.pop(key, None)
            return default

        return value

    def exists(self, key: str) -> bool:
        """
        Check if a non-expired key exists.
        """

        return self.get(key, default=_MISSING) is not _MISSING

    def delete(self, key: str) -> None:
        """
        Remove a key from the cache.
        """

        self._store.pop(key, None)

    def clear(self) -> None:
        """
        Clear the entire cache.
        """

        self._store.clear()

    @property
    def size(self) -> int:
        """
        Number of stored keys (including possibly expired ones).
        """

        return len(self._store)


_MISSING = object()

cache_service = CacheService()
