"""
WebSocket Events

Pydantic models for outbound WebSocket event payloads.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BaseEvent(BaseModel):
    """
    Base WebSocket event.
    """

    model_config = ConfigDict(from_attributes=True)

    event: str

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class PriceEvent(BaseEvent):
    """
    Live price update event.
    """

    event: str = "price"

    symbol: str

    market: str

    price: Decimal

    change: float = 0.0

    change_percent: float = 0.0


class OHLCEvent(BaseEvent):
    """
    OHLC candle update event.
    """

    event: str = "ohlc"

    symbol: str

    timeframe: str

    open: Decimal

    high: Decimal

    low: Decimal

    close: Decimal

    volume: Decimal


class IndicatorEvent(BaseEvent):
    """
    Indicator update event.
    """

    event: str = "indicator"

    symbol: str

    timeframe: str

    indicators: dict[str, Any]


class SignalEvent(BaseEvent):
    """
    Trading signal event.
    """

    event: str = "signal"

    symbol: str

    market: str

    timeframe: str

    signal: str

    confidence: float

    strength: str


class SystemEvent(BaseEvent):
    """
    System / connection status event.
    """

    event: str = "system"

    message: str

    status: str = "ok"
