"""
Symbol Service

Provides unified access to supported trading symbols.
"""

from __future__ import annotations

from app.providers.binance.rest.rest_client import binance_rest_client
from app.providers.finnhub.parser.parser import finnhub_parser
from app.providers.finnhub.rest.rest_client import finnhub_rest_client


class SymbolService:
    """
    Service responsible for symbol management.
    """

    async def get_crypto_symbols(self) -> list[str]:
        """
        Return all Binance trading symbols.
        """

        return await binance_rest_client.get_symbols()

    async def get_stock_symbols(
        self,
        exchange: str = "US",
    ):
        """
        Return supported US stock symbols.
        """

        symbols = await finnhub_rest_client.get_stock_symbols(exchange)

        return finnhub_parser.parse_symbols(symbols)

    async def get_forex_symbols(
        self,
        exchange: str = "oanda",
    ):
        """
        Return supported Forex symbols.
        """

        symbols = await finnhub_rest_client.get_forex_symbols(exchange)

        return finnhub_parser.parse_symbols(symbols)

    async def get_all_symbols(self) -> dict:
        """
        Return all supported symbols grouped by market.
        """

        crypto = await self.get_crypto_symbols()
        stocks = await self.get_stock_symbols()
        forex = await self.get_forex_symbols()

        return {
            "crypto": crypto,
            "stocks": stocks,
            "forex": forex,
        }


symbol_service = SymbolService()