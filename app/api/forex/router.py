"""
Forex API Router
"""

from __future__ import annotations

import time

from fastapi import APIRouter, Query

from app.api.forex.schemas import ForexCandleResponse, ForexQuoteResponse
from app.api.forex.service import forex_service
from app.utils.validators import validate_forex_symbol

router = APIRouter(
    prefix="/forex",
    tags=["Forex"],
)


@router.get("/{symbol}/quote", response_model=ForexQuoteResponse)
async def get_quote(symbol: str):
    """
    Get real-time forex quote.

    Example symbol: OANDA:EUR_USD
    """
    symbol = validate_forex_symbol(symbol)
    return await forex_service.get_quote(symbol)


# @router.get("/{symbol}/candles", response_model=list[ForexCandleResponse])
# async def get_candles(
#     symbol: str,
#     resolution: str = Query(default="1"),
#     from_timestamp: int = Query(
#         default_factory=lambda: int(time.time()) - 86400
#     ),
#     to_timestamp: int = Query(default_factory=lambda: int(time.time())),
# ):
#     """
#     Get OHLC forex candles.
#     """
#     symbol = validate_forex_symbol(symbol)
#     return await forex_service.get_candles(
#         symbol,
#         resolution,
#         from_timestamp,
#         to_timestamp,
#     )



@router.get(
    "/{symbol}/candles",
    response_model=list[ForexCandleResponse],
)



async def get_candles(
    symbol: str,
    resolution: str = Query(
        default="1",
        description="Candle resolution (1,5,15,30,60,D)"
    ),
    from_timestamp: int = Query(
        default_factory=lambda: int(time.time()) - 86400,
        description="Unix start timestamp"
    ),
    to_timestamp: int = Query(
        default_factory=lambda: int(time.time()),
        description="Unix end timestamp"
    ),
):
    """
    Get historical forex candles from Redis.
    """

    symbol = validate_forex_symbol(symbol)

    return await forex_service.get_candles(
        symbol=symbol,
        resolution=resolution,
        from_timestamp=from_timestamp,
        to_timestamp=to_timestamp,
    )
