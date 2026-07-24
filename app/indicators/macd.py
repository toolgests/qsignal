"""
Moving Average Convergence Divergence (MACD)

Production-ready MACD indicator implementation.
"""

from __future__ import annotations

import pandas as pd

from app.indicators.base import BaseIndicator


class MACDIndicator(BaseIndicator):
    """
    Moving Average Convergence Divergence (MACD).

    Default Parameters:
        Fast EMA: 12
        Slow EMA: 26
        Signal EMA: 9
    """

    def __init__(
        self,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9,
    ) -> None:
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period

    @property
    def name(self) -> str:
        return "MACD"

    def calculate(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calculate MACD.

        Required columns:
            close

        Returns:
            DataFrame containing:
                ema_fast
                ema_slow
                macd
                macd_signal
                macd_histogram
        """

        if "close" not in data.columns:
            raise ValueError("'close' column not found.")

        result = data.copy()

        ema_fast = result["close"].ewm(
            span=self.fast_period,
            adjust=False,
        ).mean()

        ema_slow = result["close"].ewm(
            span=self.slow_period,
            adjust=False,
        ).mean()

        macd = ema_fast - ema_slow

        signal = macd.ewm(
            span=self.signal_period,
            adjust=False,
        ).mean()

        histogram = macd - signal

        result[f"ema_{self.fast_period}"] = ema_fast
        result[f"ema_{self.slow_period}"] = ema_slow
        result["macd"] = macd
        result["macd_signal"] = signal
        result["macd_histogram"] = histogram

        return result