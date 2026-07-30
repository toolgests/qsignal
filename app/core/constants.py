
"""
Q Signals - Application Constants

This module contains all application-wide constant values.
Do not hardcode these values anywhere else in the project.
"""

from enum import Enum


# =====================================================================
# API
# =====================================================================

API_PREFIX = "/api/v1"


# =====================================================================
# Markets
# =====================================================================

class MarketType(str, Enum):
    CRYPTO = "crypto"
    FOREX = "forex"
    STOCK = "stock"


# =====================================================================
# Supported Symbols
# =====================================================================

CRYPTO_SYMBOLS = [
    "BTC-USD",
    "ETH-USD",
    "SOL-USD",
    "BNB-USD",
    "XRP-USD",
    "DOGE-USD",
    "LINK-USD",
]

FOREX_SYMBOLS = [
    "OANDA:EUR_USD",
    "OANDA:GBP_USD",
    "OANDA:USD_JPY",
    "OANDA:AUD_USD",
    "OANDA:USD_CHF",
    "OANDA:USD_CAD",
    "OANDA:NZD_USD",
]

STOCK_SYMBOLS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "META",
    "GOOGL",
    "TSLA",
]

# STOCK_SYMBOLS = [
#     "AAPL",   # Apple
#     "MSFT",   # Microsoft
#     "NVDA",   # NVIDIA
#     "AMZN",   # Amazon
#     "META",   # Meta Platforms
#     "GOOGL",  # Alphabet (Google)
#     "TSLA",   # Tesla
#     "AVGO",   # Broadcom
#     "NFLX",   # Netflix
#     "AMD",    # Advanced Micro Devices
# ]


# =====================================================================
# Timeframes
# =====================================================================

class TimeFrame(str, Enum):
    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"
    H4 = "4h"
    D1 = "1d"


# =====================================================================
# Indicators
# =====================================================================

class Indicator(str, Enum):
    RSI = "RSI"
    EMA = "EMA"
    SMA = "SMA"
    MACD = "MACD"
    ADX = "ADX"
    ATR = "ATR"
    VWAP = "VWAP"
    BOLLINGER_BANDS = "BOLLINGER_BANDS"


# =====================================================================
# Signals
# =====================================================================

class SignalType(str, Enum):
    STRONG_BUY = "STRONG_BUY"
    BUY = "BUY"
    NEUTRAL = "NEUTRAL"
    SELL = "SELL"
    STRONG_SELL = "STRONG_SELL"


# =====================================================================
# Provider Names
# =====================================================================

class Provider(str, Enum):
    BINANCE = "binance"
    FINNHUB = "finnhub"


# =====================================================================
# WebSocket Channels
# =====================================================================

class WSChannel(str, Enum):
    ALL = "all"
    PRICES = "prices"
    CHART = "chart"
    SIGNALS = "signals"
    CRYPTO = "crypto"
    FOREX = "forex"
    STOCKS = "stocks"


# =====================================================================
# Connection Status
# =====================================================================

class ConnectionStatus(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    RECONNECTING = "reconnecting"
    ERROR = "error"


# =====================================================================
# HTTP Status Messages
# =====================================================================

SUCCESS = "success"
FAILED = "failed"


# =====================================================================
# Default Limits
# =====================================================================

DEFAULT_HISTORY_LIMIT = 500
MAX_HISTORY_LIMIT = 5000


# =====================================================================
# WebSocket
# =====================================================================

DEFAULT_HEARTBEAT_SECONDS = 30
DEFAULT_RECONNECT_DELAY = 5
MAX_RECONNECT_ATTEMPTS = 10

