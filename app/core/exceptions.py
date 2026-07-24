
"""
Q Signals - Custom Exceptions

Centralized exception definitions for the application.
"""

from typing import Any


class QSignalsException(Exception):
    """
    Base exception for the application.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Any | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.details = details

        super().__init__(message)


# ======================================================================
# Provider Exceptions
# ======================================================================

class ProviderException(QSignalsException):
    """Base provider exception."""


class BinanceConnectionError(ProviderException):
    """Raised when Binance connection fails."""


class BinanceAPIError(ProviderException):
    """Raised when Binance API returns an error."""


class FinnhubConnectionError(ProviderException):
    """Raised when Finnhub connection fails."""


class FinnhubAPIError(ProviderException):
    """Raised when Finnhub API returns an error."""


class ProviderTimeoutError(ProviderException):
    """Raised when provider request times out."""


class ProviderReconnectError(ProviderException):
    """Raised when reconnection attempts fail."""


# ======================================================================
# Market Exceptions
# ======================================================================

class MarketException(QSignalsException):
    """Base market exception."""


class InvalidSymbolError(MarketException):
    """Raised when an invalid symbol is requested."""


class InvalidTimeframeError(MarketException):
    """Raised when timeframe is invalid."""


class MarketDataUnavailableError(MarketException):
    """Raised when market data is unavailable."""


class OHLCGenerationError(MarketException):
    """Raised when candle generation fails."""


# ======================================================================
# Indicator Exceptions
# ======================================================================

class IndicatorException(QSignalsException):
    """Base indicator exception."""


class IndicatorCalculationError(IndicatorException):
    """Raised when indicator calculation fails."""


class InsufficientDataError(IndicatorException):
    """Raised when indicator does not have enough data."""


# ======================================================================
# Signal Exceptions
# ======================================================================

class SignalException(QSignalsException):
    """Base signal exception."""


class SignalGenerationError(SignalException):
    """Raised when signal generation fails."""


# ======================================================================
# WebSocket Exceptions
# ======================================================================

class WebSocketException(QSignalsException):
    """Base websocket exception."""


class WebSocketDisconnectedError(WebSocketException):
    """Raised when websocket disconnects."""


class WebSocketAuthenticationError(WebSocketException):
    """Reserved for future authenticated websocket support."""


# ======================================================================
# Cache Exceptions
# ======================================================================

class CacheException(QSignalsException):
    """Base cache exception."""


class CacheConnectionError(CacheException):
    """Raised when cache is unavailable."""


# ======================================================================
# Configuration Exceptions
# ======================================================================

class ConfigurationError(QSignalsException):
    """Raised when configuration is invalid."""


# ======================================================================
# Validation Exceptions
# ======================================================================

class ValidationException(QSignalsException):
    """Raised for validation failures."""

