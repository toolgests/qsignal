"""
Stocks API Schemas
"""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class StockQuoteResponse(BaseModel):
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


class StockCandleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symbol: str
    resolution: str
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    timestamp: int


class CompanyProfileResponse(BaseModel):
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
