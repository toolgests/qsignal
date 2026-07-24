"""
Exponential Moving Average (EMA)

Calculates the Exponential Moving Average for OHLCV data.
"""

from __future__ import annotations

import pandas as pd

from app.indicators.base import BaseIndicator


class EMAIndicator(BaseIndicator):
    """
    Exponential Moving Average (EMA) indicator.
    """

    def __init__(self, period: int = 20) -> None:
        self.period = period

    @property
    def name(self) -> str:
        return "EMA"

    def calculate(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calculate EMA.

        Expected DataFrame columns:
            close

        Returns:
            Original DataFrame with EMA column.
        """

        if "close" not in data.columns:
            raise ValueError("'close' column not found.")

        result = data.copy()

        result[f"ema_{self.period}"] = (
            result["close"]
            .ewm(
                span=self.period,
                adjust=False,
            )
            .mean()
        )

        return result