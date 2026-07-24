"""
Crypto API Schemas
"""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CryptoPriceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symbol: str
    price: Decimal


class CryptoTickerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symbol: str
    last_price: Decimal
    price_change: Decimal
    price_change_percent: Decimal
    high_price: Decimal
    low_price: Decimal
    open_price: Decimal
    volume: Decimal


class CryptoCandleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symbol: str
    interval: str
    open_time: int
    close_time: int
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    closed: bool
