"""
Markets Domain Models
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class MarketType(str, Enum):
    CRYPTO = "crypto"
    FOREX = "forex"
    STOCK = "stock"


class MarketData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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
