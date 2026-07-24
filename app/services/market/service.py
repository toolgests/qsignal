"""
Market Service

Unified market service for Crypto, Forex and Stocks.
"""

from __future__ import annotations

from app.providers.binance.rest.rest_client import binance_rest_client
from app.providers.finnhub.rest.rest_client import finnhub_rest_client


class MarketService:
    """
    Unified market service.
    """

    async def get_crypto_price(self, symbol: str) -> dict:
        """
        Get latest crypto price.
        """

        return await binance_rest_client.get_price(symbol)

    async def get_crypto_ticker(self, symbol: str) -> dict:
        """
        Get crypto 24hr ticker.
        """

        return await binance_rest_client.get_24hr_ticker(symbol)

    async def get_crypto_ohlc(
        self,
        symbol: str,
        interval: str = "1m",
        limit: int = 500,
    ) -> list:
        """
        Get crypto OHLC candles.
        """

        return await binance_rest_client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit,
        )

    async def get_stock_quote(self, symbol: str) -> dict:
        """
        Get stock quote.
        """

        return await finnhub_rest_client.get_stock_quote(symbol)

    async def get_forex_quote(self, symbol: str) -> dict:
        """
        Get forex quote.
        """

        return await finnhub_rest_client.get_forex_quote(symbol)

    async def get_stock_candles(
        self,
        symbol: str,
        resolution: str,
        from_timestamp: int,
        to_timestamp: int,
    ) -> dict:
        """
        Get stock OHLC.
        """

        return await finnhub_rest_client.get_stock_candles(
            symbol=symbol,
            resolution=resolution,
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
        )

    async def get_forex_candles(
        self,
        symbol: str,
        resolution: str,
        from_timestamp: int,
        to_timestamp: int,
    ) -> dict:
        """
        Get forex OHLC.
        """

        return await finnhub_rest_client.get_forex_candles(
            symbol=symbol,
            resolution=resolution,
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
        )


market_service = MarketService()