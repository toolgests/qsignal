"""
Signal Rules

Centralized trading rules for indicator evaluation.
"""

from __future__ import annotations


class SignalRules:
    """
    Trading rules used by the voting engine.
    """

    # ==========================
    # RSI
    # ==========================

    RSI_OVERSOLD = 30.0
    RSI_OVERBOUGHT = 70.0

    # ==========================
    # ADX
    # ==========================

    ADX_WEAK_TREND = 20.0
    ADX_STRONG_TREND = 25.0
    ADX_VERY_STRONG_TREND = 40.0

    # ==========================
    # EMA / SMA
    # ==========================

    EMA_PERIOD = 20
    SMA_PERIOD = 20

    # ==========================
    # MACD
    # ==========================

    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9

    # ==========================
    # ATR
    # ==========================

    ATR_PERIOD = 14

    # ==========================
    # VWAP
    # ==========================

    VWAP_ENABLED = True

    # ==========================
    # Bollinger Bands
    # ==========================

    BB_PERIOD = 20
    BB_STD_DEV = 2

    # ==========================
    # Voting
    # ==========================

    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

    STRONG_BUY = "STRONG BUY"
    STRONG_SELL = "STRONG SELL"

    MIN_BUY_VOTES = 4
    MIN_SELL_VOTES = 4

    STRONG_BUY_VOTES = 6
    STRONG_SELL_VOTES = 6

    # ==========================
    # Confidence
    # ==========================

    VERY_HIGH_CONFIDENCE = 90.0
    HIGH_CONFIDENCE = 75.0
    MEDIUM_CONFIDENCE = 60.0
    LOW_CONFIDENCE = 50.0


rules = SignalRules()