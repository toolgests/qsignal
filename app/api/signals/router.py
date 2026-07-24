"""
Signals API Router
"""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.api.signals.schemas import SignalResponse
from app.api.signals.service import signals_api_service
from app.core.constants import MarketType
from app.utils.validators import validate_timeframe

router = APIRouter(
    prefix="/signals",
    tags=["Signals"],
)


@router.get(
    "/{symbol}",
    response_model=SignalResponse,
)
async def get_signal(
    symbol: str,
    market: MarketType = Query(
        default=MarketType.CRYPTO
    ),
    timeframe: str = Query(
        default="1m"
    ),
):
    symbol = symbol.upper()

    timeframe = validate_timeframe(
        timeframe
    )

    signal = await signals_api_service.get_signal(
        symbol=symbol,
        market=market.value,
        timeframe=timeframe,
    )

    return signal