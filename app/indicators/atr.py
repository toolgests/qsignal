"""
Average True Range (ATR)

Production-ready ATR indicator implementation.
"""

from __future__ import annotations

import pandas as pd

from app.indicators.base import BaseIndicator


class ATRIndicator(BaseIndicator):
    """
    Average True Range (ATR).

    Default Period:
        14
    """

    def __init__(self, period: int = 14) -> None:
        self.period = period

    @property
    def name(self) -> str:
        return "ATR"

    def calculate(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calculate ATR.

        Required columns:
            high
            low
            close

        Returns:
            DataFrame with ATR column.
        """

        required = {"high", "low", "close"}

        if not required.issubset(data.columns):
            raise ValueError(
                "DataFrame must contain high, low and close columns."
            )

        result = data.copy()

        previous_close = result["close"].shift(1)

        tr1 = result["high"] - result["low"]

        tr2 = (result["high"] - previous_close).abs()

        tr3 = (result["low"] - previous_close).abs()

        true_range = pd.concat(
            [tr1, tr2, tr3],
            axis=1,
        ).max(axis=1)

        result[f"atr_{self.period}"] = (
            true_range
            .ewm(
                alpha=1 / self.period,
                adjust=False,
            )
            .mean()
        )

        return result