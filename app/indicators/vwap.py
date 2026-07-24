"""
Volume Weighted Average Price (VWAP)

Production-ready VWAP indicator implementation.
"""

from __future__ import annotations

import pandas as pd

from app.indicators.base import BaseIndicator


class VWAPIndicator(BaseIndicator):
    """
    Volume Weighted Average Price (VWAP).

    Formula:
        VWAP = Σ(Typical Price × Volume) / Σ(Volume)
    """

    @property
    def name(self) -> str:
        return "VWAP"

    def calculate(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calculate VWAP.

        Required columns:
            high
            low
            close
            volume

        Returns:
            DataFrame with VWAP column.
        """

        required = {
            "high",
            "low",
            "close",
            "volume",
        }

        if not required.issubset(data.columns):
            raise ValueError(
                "DataFrame must contain high, low, close and volume columns."
            )

        result = data.copy()

        typical_price = (
            result["high"]
            + result["low"]
            + result["close"]
        ) / 3

        cumulative_price_volume = (
            typical_price * result["volume"]
        ).cumsum()

        cumulative_volume = (
            result["volume"]
        ).cumsum()

        result["vwap"] = (
            cumulative_price_volume
            / cumulative_volume
        )

        return result