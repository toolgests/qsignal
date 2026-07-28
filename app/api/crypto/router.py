"""
Crypto API Router
"""

from __future__ import annotations
from app.core.redis import redis_client

from fastapi import APIRouter, Query

from app.api.crypto.schemas import (
    CryptoCandleResponse,
    CryptoPriceResponse,
    CryptoTickerResponse,
)
from app.api.crypto.service import crypto_service
from app.utils.validators import validate_crypto_symbol, validate_timeframe

router = APIRouter(
    prefix="/crypto",
    tags=["Crypto"],
)


@router.get("/redis-test")
async def redis_test():
    return {
        "btc": await redis_client.get("tick:BTC-USD"),
        "eth": await redis_client.get("tick:ETH-USD"),
        "sol": await redis_client.get("tick:SOL-USD"),
        "bnb": await redis_client.get("tick:BNB-USD"),
    }



@router.get("/{symbol}/price", response_model=CryptoPriceResponse)
async def get_price(symbol: str):
    """
    Get latest crypto price.
    """
    symbol = validate_crypto_symbol(symbol)
    return await crypto_service.get_price(symbol)


@router.get("/{symbol}/ticker", response_model=CryptoTickerResponse)
async def get_ticker(symbol: str):
    """
    Get 24-hour crypto ticker statistics.
    """
    symbol = validate_crypto_symbol(symbol)
    return await crypto_service.get_ticker(symbol)


@router.get("/{symbol}/candles", response_model=list[CryptoCandleResponse])
async def get_candles(
    symbol: str,
    interval: str = Query(default="1m"),
    limit: int = Query(default=500, ge=1, le=1000),
):
    """
    Get OHLC candlestick data.
    """
    symbol = validate_crypto_symbol(symbol)
    interval = validate_timeframe(interval)
    return await crypto_service.get_candles(symbol, interval, limit)


