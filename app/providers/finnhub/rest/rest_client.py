"""
Finnhub REST Client

Production-ready wrapper for Finnhub REST API.
"""

from __future__ import annotations

from app.providers.finnhub.client.client import finnhub_client


class FinnhubRestClient:
    """
    Finnhub REST API wrapper.
    """

    async def get_stock_quote(self, symbol: str) -> dict:
        """
        Get real-time stock quote.
        """

        return await finnhub_client.get(
            "/quote",
            params={
                "symbol": symbol.upper(),
            },
        )

    async def get_forex_quote(self, symbol: str) -> dict:
        """
        Get real-time forex quote.

        Example:
            OANDA:EUR_USD
        """

        return await finnhub_client.get(
            "/quote",
            params={
                "symbol": symbol,
            },
        )

    async def get_stock_candles(
        self,
        symbol: str,
        resolution: str,
        from_timestamp: int,
        to_timestamp: int,
    ) -> dict:
        """
        Get stock OHLC candles.
        """

        return await finnhub_client.get(
            "/stock/candle",
            params={
                "symbol": symbol.upper(),
                "resolution": resolution,
                "from": from_timestamp,
                "to": to_timestamp,
            },
        )

    async def get_forex_candles(
        self,
        symbol: str,
        resolution: str,
        from_timestamp: int,
        to_timestamp: int,
    ) -> dict:
        """
        Get forex OHLC candles.
        """

        return await finnhub_client.get(
            "/forex/candle",
            params={
                "symbol": symbol,
                "resolution": resolution,
                "from": from_timestamp,
                "to": to_timestamp,
            },
        )

    async def get_stock_symbols(
        self,
        exchange: str = "US",
    ) -> list:
        """
        Get all stock symbols.
        """

        return await finnhub_client.get(
            "/stock/symbol",
            params={
                "exchange": exchange,
            },
        )

    async def get_forex_symbols(
        self,
        exchange: str = "oanda",
    ) -> dict:
        """
        Get supported forex symbols.
        """

        return await finnhub_client.get(
            "/forex/symbol",
            params={
                "exchange": exchange,
            },
        )

    async def get_company_profile(
        self,
        symbol: str,
    ) -> dict:
        """
        Get company profile.
        """

        return await finnhub_client.get(
            "/stock/profile2",
            params={
                "symbol": symbol.upper(),
            },
        )


finnhub_rest_client = FinnhubRestClient()