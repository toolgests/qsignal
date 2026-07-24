"""
Validation Utilities

Shared validation helpers for symbols, timeframes and pagination.
"""

from __future__ import annotations

from app.core.constants import CRYPTO_SYMBOLS, FOREX_SYMBOLS, STOCK_SYMBOLS
from app.core.exceptions import InvalidSymbolError, InvalidTimeframeError
from app.market_engine.timeframe_manager import timeframe_manager


def validate_timeframe(timeframe: str) -> str:
    """
    Validate a timeframe string, raising if unsupported.
    """

    if not timeframe_manager.exists(timeframe):
        raise InvalidTimeframeError(
            message=f"Unsupported timeframe: {timeframe}",
            status_code=400,
        )

    return timeframe


def validate_crypto_symbol(symbol: str) -> str:
    """
    Validate a crypto symbol.
    """

    symbol = symbol.upper()

    if symbol not in CRYPTO_SYMBOLS:
        raise InvalidSymbolError(
            message=f"Unsupported crypto symbol: {symbol}",
            status_code=400,
        )

    return symbol


# def validate_forex_symbol(symbol: str) -> str:
#     """
#     Validate a forex symbol.
#     """

#     if symbol not in FOREX_SYMBOLS:
#         raise InvalidSymbolError(
#             message=f"Unsupported forex symbol: {symbol}",
#             status_code=400,
#         )

#     return symbol

def validate_forex_symbol(symbol: str) -> str:
    """
    Validate a forex symbol.
    """

    symbol = symbol.upper()

    if symbol not in FOREX_SYMBOLS:
        raise InvalidSymbolError(
            message=f"Unsupported forex symbol: {symbol}",
            status_code=400,
        )

    return symbol


def validate_stock_symbol(symbol: str) -> str:
    """
    Validate a stock symbol.
    """

    symbol = symbol.upper()

    if symbol not in STOCK_SYMBOLS:
        raise InvalidSymbolError(
            message=f"Unsupported stock symbol: {symbol}",
            status_code=400,
        )

    return symbol


def clamp_limit(limit: int, minimum: int = 1, maximum: int = 5000) -> int:
    """
    Clamp a history limit to a safe range.
    """

    return max(minimum, min(limit, maximum))
