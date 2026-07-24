"""
Markets API Schemas

Pydantic response models for Market endpoints.
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class MarketResponse(BaseModel):
    """
    Live market response.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    symbol: str = Field(
        ...,
        examples=["BTCUSDT"]
    )

    market: str

    price: Decimal

    change: float

    change_percent: float

    volume: Decimal | None = None

    high: Decimal | None = None

    low: Decimal | None = None

    open: Decimal | None = None

    timestamp: datetime


class OHLCResponse(BaseModel):
    """
    OHLC response.
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


class SymbolResponse(BaseModel):
    """
    Trading symbol.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    symbol: str

    market: str

    description: str


class MarketListResponse(BaseModel):
    """
    List of available markets.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    markets: list[str]


class SymbolsResponse(BaseModel):
    """
    List of supported symbols.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    symbols: list[SymbolResponse]