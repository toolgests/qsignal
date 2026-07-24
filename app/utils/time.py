"""
Time Utilities

Common datetime helpers used across the application.
"""

from __future__ import annotations

from datetime import UTC, datetime


def utcnow() -> datetime:
    """
    Return current UTC time.
    """
    return datetime.now(UTC)


def to_timestamp_ms(dt: datetime) -> int:
    """
    Convert a datetime to Unix milliseconds.
    """
    return int(dt.timestamp() * 1000)


def from_timestamp_ms(timestamp_ms: int) -> datetime:
    """
    Convert Unix milliseconds to a UTC datetime.
    """
    return datetime.fromtimestamp(timestamp_ms / 1000, tz=UTC)


def to_timestamp_s(dt: datetime) -> int:
    """
    Convert a datetime to Unix seconds.
    """
    return int(dt.timestamp())


def from_timestamp_s(timestamp_s: int) -> datetime:
    """
    Convert Unix seconds to a UTC datetime.
    """
    return datetime.fromtimestamp(timestamp_s, tz=UTC)
