"""
Signals API Service
"""

from __future__ import annotations

import json

from app.core.exceptions import InsufficientDataError
from app.core.redis import redis_client
from app.services.signal.service import signal_service


class SignalsAPIService:
    """
    API-facing signal service.
    """

    MIN_CANDLES = 30

    async def get_signal(
        self,
        symbol: str,
        market: str,
        timeframe: str,
    ):
        symbol = symbol.upper()

        key = f"candles:{symbol}:{timeframe}"

        candles = await redis_client.lrange(
            key,
            0,
            -1,
        )

        print(f"Redis Key: {key}")
        print(f"Candles in Redis: {len(candles)}")

        if len(candles) < self.MIN_CANDLES:
            raise InsufficientDataError(
                message=(
                    f"Not enough candles for {symbol} "
                    f"({timeframe}) to generate a signal. "
                    f"Need at least {self.MIN_CANDLES}."
                ),
                status_code=422,
            )

        candles = [
            json.loads(candle)
            for candle in candles
        ]
        return signal_service.generate_signal(
            symbol=symbol,
            market=market,
            timeframe=timeframe,
            candles=candles,
        )


signals_api_service = SignalsAPIService()