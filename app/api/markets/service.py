"""
Markets Service

Business logic for market operations.
"""

from app.core.constants import (
    CRYPTO_SYMBOLS,
    FOREX_SYMBOLS,
    STOCK_SYMBOLS,
)


class MarketService:
    """
    Service responsible for market information.
    """

    async def get_markets(self) -> list[str]:
        """
        Return supported market types.
        """

        return [
            "crypto",
            "forex",
            "stocks",
        ]

    async def get_all_symbols(self) -> dict:
        """
        Return all supported symbols.
        """

        return {
            "crypto": CRYPTO_SYMBOLS,
            "forex": FOREX_SYMBOLS,
            "stocks": STOCK_SYMBOLS,
        }

    async def get_crypto_symbols(self) -> list[str]:
        """
        Return supported crypto symbols.
        """

        return CRYPTO_SYMBOLS

    async def get_forex_symbols(self) -> list[str]:
        """
        Return supported forex symbols.
        """

        return FOREX_SYMBOLS

    async def get_stock_symbols(self) -> list[str]:
        """
        Return supported stock symbols.
        """

        return STOCK_SYMBOLS


market_service = MarketService()