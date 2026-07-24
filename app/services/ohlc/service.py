"""
OHLC Service

Normalize OHLC data from different providers.
"""

from __future__ import annotations

from decimal import Decimal

from app.providers.binance.parser.parser import binance_parser
from app.providers.finnhub.parser.parser import finnhub_parser
from app.providers.binance.rest.rest_client import binance_rest_client
from app.providers.finnhub.rest.rest_client import finnhub_rest_client


class OHLCService:
    """
    OHLC normalization service.
    """

    async def get_crypto_ohlc(
        self,
        symbol: str,
        interval: str = "1m",
        limit: int = 500,
    ):
        """
        Get normalized Binance candles.
        """

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

    async def get_stock_ohlc(
        self,
        symbol: str,
        resolution: str,
        from_timestamp: int,
        to_timestamp: int,
    ):
        """
        Get normalized stock candles.
        """

        data = await finnhub_rest_client.get_stock_candles(
            symbol=symbol,
            resolution=resolution,
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
        )

        return finnhub_parser.parse_candles(
            symbol=symbol,
            resolution=resolution,
            data=data,
        )

    async def get_forex_ohlc(
        self,
        symbol: str,
        resolution: str,
        from_timestamp: int,
        to_timestamp: int,
    ):
        """
        Get normalized forex candles.
        """

        data = await finnhub_rest_client.get_forex_candles(
            symbol=symbol,
            resolution=resolution,
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
        )

        return finnhub_parser.parse_candles(
            symbol=symbol,
            resolution=resolution,
            data=data,
        )

    @staticmethod
    def latest_close(candles) -> Decimal:
        """
        Return latest closing price.
        """

        if not candles:
            raise ValueError("No candle data available.")

        return candles[-1].close


ohlc_service = OHLCService()