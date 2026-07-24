
"""
Q Signals - Application Settings

Centralized application configuration using Pydantic Settings.
All sensitive values are loaded from environment variables.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------
    APP_NAME: str = Field(default="Q Signals")
    APP_VERSION: str = Field(default="1.0.0")
    APP_DESCRIPTION: str = Field(
        default="Professional Trading Signal Backend"
    )
    DEBUG: bool = Field(default=True)

    # ------------------------------------------------------------------
    # Server
    # ------------------------------------------------------------------
    HOST: str = Field(default="127.0.0.1")
    PORT: int = Field(default=8000)

    # ------------------------------------------------------------------
    # CORS
    # ------------------------------------------------------------------
    CORS_ORIGINS: list[str] = Field(default=["*"])

    # ------------------------------------------------------------------
    # Binance
    # ------------------------------------------------------------------
    BINANCE_REST_URL: str = Field(
        default="https://api.binance.com"
    )

    BINANCE_WS_URL: str = Field(
        default="wss://stream.binance.com:9443/ws"
    )

    BINANCE_API_KEY: str = Field(default="")
    BINANCE_SECRET_KEY: str = Field(default="")

    # ------------------------------------------------------------------
    # Finnhub
    # ------------------------------------------------------------------
    FINNHUB_REST_URL: str = Field(
        default="https://finnhub.io/api/v1"
    )

    FINNHUB_WS_URL: str = Field(
        default="wss://ws.finnhub.io"
    )

    FINNHUB_API_KEY: str = Field(default="")

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    LOG_LEVEL: str = Field(default="INFO")

    # ------------------------------------------------------------------
    # WebSocket
    # ------------------------------------------------------------------
    WS_HEARTBEAT_INTERVAL: int = Field(default=30)
    WS_RECONNECT_DELAY: int = Field(default=5)

    # ------------------------------------------------------------------
    # Redis (Future)
    # ------------------------------------------------------------------
    REDIS_ENABLED: bool = Field(default=False)
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)

    # ------------------------------------------------------------------
    # Market Defaults
    # ------------------------------------------------------------------
    DEFAULT_TIMEFRAME: str = Field(default="1m")

    SUPPORTED_TIMEFRAMES: list[str] = Field(
        default=[
            "1m",
            "5m",
            "15m",
            "30m",
            "1h",
            "4h",
            "1d",
        ]
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.
    """
    return Settings()


settings = get_settings()

