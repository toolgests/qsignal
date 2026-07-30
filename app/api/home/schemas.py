"""
Home API Schemas
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class PriceResponse(BaseModel):
    symbol: str
    market: str
    price: float
    volume: float
    timestamp: datetime


class CandleResponse(BaseModel):
    symbol: str
    timeframe: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class SymbolResponse(BaseModel):
    symbol: str
    market: str
    price: PriceResponse
    candles: dict[str, list[CandleResponse]]


class HomeResponse(BaseModel):
    crypto: list[SymbolResponse]
    stocks: list[SymbolResponse]
    forex: list[SymbolResponse]