"""
Finnhub Data Models

Pydantic models for Finnhub REST and WebSocket responses.
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class FinnhubQuote(BaseModel):
    """
    Finnhub real-time quote.
    """

    model_config = ConfigDict(from_attributes=True)

    symbol: str

    current_price: Decimal

    change: Decimal

    percent_change: Decimal

    high: Decimal

    low: Decimal

    open: Decimal

    previous_close: Decimal

    timestamp: int


class FinnhubCandle(BaseModel):
    """
    Finnhub OHLC candle.
    """

    model_config = ConfigDict(from_attributes=True)

    symbol: str

    resolution: str

    open: Decimal

    high: Decimal

    low: Decimal

    close: Decimal

    volume: Decimal

    timestamp: int


class FinnhubSymbol(BaseModel):
    """
    Trading symbol.
    """

    model_config = ConfigDict(from_attributes=True)

    symbol: str

    display_symbol: str

    description: str

    currency: str

    exchange: str

    type: str


class FinnhubCompanyProfile(BaseModel):
    """
    Company profile.
    """

    model_config = ConfigDict(from_attributes=True)

    ticker: str

    name: str

    country: str

    currency: str

    exchange: str

    industry: str

    ipo: str

    logo: str

    market_capitalization: Decimal

    share_outstanding: Decimal

    weburl: str