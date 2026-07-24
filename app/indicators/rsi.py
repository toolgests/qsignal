"""
Relative Strength Index (RSI)

Production-ready RSI indicator implementation.
"""

from __future__ import annotations

import pandas as pd

from app.indicators.base import BaseIndicator


class RSIIndicator(BaseIndicator):
    """
    Relative Strength Index (RSI).

    Default Period:
        14
    """

    def __init__(self, period: int = 14) -> None:
        self.period = period

    @property
    def name(self) -> str:
        return "RSI"

    def calculate(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calculate RSI.

        Required columns:
            close

        Returns:
            DataFrame with RSI column.
        """

        if "close" not in data.columns:
            raise ValueError("'close' column not found.")

        result = data.copy()

        delta = result["close"].diff()

        gain = delta.clip(lower=0)

        loss = -delta.clip(upper=0)

        avg_gain = gain.ewm(
            alpha=1 / self.period,
            adjust=False,
        ).mean()

        avg_loss = loss.ewm(
            alpha=1 / self.period,
            adjust=False,
        ).mean()

        rs = avg_gain / avg_loss

        result[f"rsi_{self.period}"] = 100 - (
            100 / (1 + rs)
        )

        return result