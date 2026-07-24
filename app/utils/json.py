"""
JSON Utilities

Fast JSON encoding/decoding helpers built on orjson, with
support for Decimal, datetime, NaN and Infinity values.
"""

from __future__ import annotations

import math
from datetime import date, datetime
from decimal import Decimal
from typing import Any

import orjson


def _sanitize(value: Any) -> Any:
    """
    Recursively sanitize values so they are JSON serializable.
    """

    if isinstance(value, dict):
        return {
            key: _sanitize(val)
            for key, val in value.items()
        }

    if isinstance(value, list):
        return [_sanitize(item) for item in value]

    if isinstance(value, tuple):
        return [_sanitize(item) for item in value]

    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, float):
        if math.isnan(value):
            return None

        if math.isinf(value):
            return None

        return value

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    return value


def dumps(data: Any) -> str:
    """
    Serialize Python object to JSON.
    """

    return orjson.dumps(
        _sanitize(data)
    ).decode("utf-8")


def loads(data: str | bytes) -> Any:
    """
    Deserialize JSON.
    """

    return orjson.loads(data)