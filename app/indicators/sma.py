"""
Simple Moving Average (SMA)

Calculates the Simple Moving Average for OHLCV data.
"""

from __future__ import annotations

import pandas as pd

from app.indicators.base import BaseIndicator


class SMAIndicator(BaseIndicator):
    """
    Simple Moving Average (SMA) indicator.
    """

    def __init__(self, period: int = 20) -> None:
        self.period = period

    @property
    def name(self) -> str:
        return "SMA"

    def calculate(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calculate SMA.

        Expected DataFrame columns:
            close

        Returns:
            Original DataFrame with SMA column.
        """

        if "close" not in data.columns:
            raise ValueError("'close' column not found.")

        result = data.copy()

        result[f"sma_{self.period}"] = (
            result["close"]
            .rolling(window=self.period, min_periods=self.period)
            .mean()
        )

        return result