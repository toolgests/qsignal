"""
Signal Models

Pydantic models for trading signals.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class IndicatorVote(BaseModel):
    """
    Individual indicator vote.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    indicator: str

    signal: str

    value: Decimal | float | int


class TradingSignal(BaseModel):
    """
    Generated trading signal.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    symbol: str

    timeframe: str

    signal: str

    confidence: float

    strength: str

    buy_votes: int

    sell_votes: int

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )


class SignalResponse(BaseModel):
    """
    API response model.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    symbol: str

    market: str

    timeframe: str

    price: Decimal

    signal: str

    confidence: float

    strength: str

    buy_votes: int

    sell_votes: int

    indicators: list[IndicatorVote]

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )