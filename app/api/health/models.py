
"""
Market Domain Models

Shared models for market data across all providers.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class MarketType(str, Enum):
    """
    Supported market types.
    """

    CRYPTO = "crypto"
    FOREX = "forex"
    STOCK = "stock"


class MarketData(BaseModel):
    """
    Live market data model.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    symbol: str = Field(..., examples=["BTCUSDT"])

    market: MarketType

    price: Decimal

    change: float

    change_percent: float

    volume: Decimal | None = None

    high: Decimal | None = None

    low: Decimal | None = None

    open: Decimal | None = None

    timestamp: datetime


class OHLC(BaseModel):
    """
    OHLC candle model.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    symbol: str

    timeframe: str

    open: Decimal

    high: Decimal

    low: Decimal

    close: Decimal

    volume: Decimal

    timestamp: datetime

