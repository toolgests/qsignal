"""
Crypto Service

Business logic for crypto market endpoints, backed by Binance.
"""

from __future__ import annotations

from app.providers.binance.parser.parser import binance_parser
from app.providers.binance.rest.rest_client import binance_rest_client
from app.services.redis_service import redis_service

class CryptoService:
    """
    Service responsible for crypto market data.
    """

    async def get_price(self, symbol: str):
        data = await redis_service.get_quote(symbol)

        if data is None:
            return {
                "success": False,
                "message": f"No live data found for {symbol}"
            }

        return data

    async def get_ticker(self, symbol: str):
        data = await binance_rest_client.get_24hr_ticker(symbol)
        return binance_parser.parse_24hr_ticker(data)

    async def get_candles(
        self,
        symbol: str,
        interval: str = "1m",
        limit: int = 500,
    ):
        data = await binance_rest_client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit,
        )

        return [
            binance_parser.parse_kline(
                symbol=symbol,
                interval=interval,
                data=item,
            )
            for item in data
        ]


crypto_service = CryptoService()
