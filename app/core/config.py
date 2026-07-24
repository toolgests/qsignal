
"""
Q Signals - Configuration

Central configuration access for the application.
"""

from app.core.settings import settings


class Config:
    """
    Central configuration object.

    Import this class anywhere in the project instead of
    importing settings directly.
    """

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------
    APP_NAME = settings.APP_NAME
    APP_VERSION = settings.APP_VERSION
    APP_DESCRIPTION = settings.APP_DESCRIPTION
    DEBUG = settings.DEBUG

    # ------------------------------------------------------------------
    # Server
    # ------------------------------------------------------------------
    HOST = settings.HOST
    PORT = settings.PORT

    # ------------------------------------------------------------------
    # CORS
    # ------------------------------------------------------------------
    CORS_ORIGINS = settings.CORS_ORIGINS

    # ------------------------------------------------------------------
    # Binance
    # ------------------------------------------------------------------
    BINANCE_REST_URL = settings.BINANCE_REST_URL
    BINANCE_WS_URL = settings.BINANCE_WS_URL
    BINANCE_API_KEY = settings.BINANCE_API_KEY
    BINANCE_SECRET_KEY = settings.BINANCE_SECRET_KEY

    # ------------------------------------------------------------------
    # Finnhub
    # ------------------------------------------------------------------
    FINNHUB_REST_URL = settings.FINNHUB_REST_URL
    FINNHUB_WS_URL = settings.FINNHUB_WS_URL
    FINNHUB_API_KEY = settings.FINNHUB_API_KEY

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    LOG_LEVEL = settings.LOG_LEVEL

    # ------------------------------------------------------------------
    # WebSocket
    # ------------------------------------------------------------------
    WS_HEARTBEAT_INTERVAL = settings.WS_HEARTBEAT_INTERVAL
    WS_RECONNECT_DELAY = settings.WS_RECONNECT_DELAY

    # ------------------------------------------------------------------
    # Redis
    # ------------------------------------------------------------------
    REDIS_ENABLED = settings.REDIS_ENABLED
    REDIS_HOST = settings.REDIS_HOST
    REDIS_PORT = settings.REDIS_PORT

    # ------------------------------------------------------------------
    # Market
    # ------------------------------------------------------------------
    DEFAULT_TIMEFRAME = settings.DEFAULT_TIMEFRAME
    SUPPORTED_TIMEFRAMES = settings.SUPPORTED_TIMEFRAMES


config = Config()

