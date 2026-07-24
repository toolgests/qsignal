"""
Bollinger Bands

Production-ready Bollinger Bands indicator implementation.
"""

from __future__ import annotations

import pandas as pd

from app.indicators.base import BaseIndicator


class BollingerBandsIndicator(BaseIndicator):
    """
    Bollinger Bands Indicator.

    Default Parameters:
        Period: 20
        Standard Deviations: 2
    """

    def __init__(
        self,
        period: int = 20,
        std_dev: float = 2.0,
    ) -> None:
        self.period = period
        self.std_dev = std_dev

    @property
    def name(self) -> str:
        return "Bollinger Bands"

    def calculate(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calculate Bollinger Bands.

        Required columns:
            close

        Returns:
            DataFrame containing:
                bb_middle
                bb_upper
                bb_lower
                bb_width
                bb_percent
        """

        if "close" not in data.columns:
            raise ValueError(
                "'close' column not found."
            )

        result = data.copy()

        middle = (
            result["close"]
            .rolling(
                window=self.period,
                min_periods=self.period,
            )
            .mean()
        )

        std = (
            result["close"]
            .rolling(
                window=self.period,
                min_periods=self.period,
            )
            .std()
        )

        upper = middle + (std * self.std_dev)

        lower = middle - (std * self.std_dev)

        width = upper - lower

        percent = (
            (result["close"] - lower)
            / width
        )

        result["bb_middle"] = middle
        result["bb_upper"] = upper
        result["bb_lower"] = lower
        result["bb_width"] = width
        result["bb_percent"] = percent

        return result