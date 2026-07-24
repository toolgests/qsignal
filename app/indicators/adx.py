"""
Average Directional Index (ADX)

Production-ready ADX indicator implementation.
"""

from __future__ import annotations

import pandas as pd

from app.indicators.base import BaseIndicator


class ADXIndicator(BaseIndicator):
    """
    Average Directional Index (ADX).

    Default Period:
        14
    """

    def __init__(self, period: int = 14) -> None:
        self.period = period

    @property
    def name(self) -> str:
        return "ADX"

    def calculate(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calculate ADX.

        Required columns:
            high
            low
            close

        Returns:
            DataFrame with:
                +DI
                -DI
                ADX
        """

        required = {"high", "low", "close"}

        if not required.issubset(data.columns):
            raise ValueError(
                "DataFrame must contain high, low and close columns."
            )

        result = data.copy()

        high = result["high"]
        low = result["low"]
        close = result["close"]

        up_move = high.diff()

        down_move = -low.diff()

        plus_dm = up_move.where(
            (up_move > down_move) & (up_move > 0),
            0.0,
        )

        minus_dm = down_move.where(
            (down_move > up_move) & (down_move > 0),
            0.0,
        )

        tr1 = high - low

        tr2 = (high - close.shift()).abs()

        tr3 = (low - close.shift()).abs()

        true_range = pd.concat(
            [tr1, tr2, tr3],
            axis=1,
        ).max(axis=1)

        atr = true_range.ewm(
            alpha=1 / self.period,
            adjust=False,
        ).mean()

        plus_di = (
            100
            * plus_dm.ewm(
                alpha=1 / self.period,
                adjust=False,
            ).mean()
            / atr
        )

        minus_di = (
            100
            * minus_dm.ewm(
                alpha=1 / self.period,
                adjust=False,
            ).mean()
            / atr
        )

        dx = (
            (plus_di - minus_di).abs()
            / (plus_di + minus_di)
        ) * 100

        adx = dx.ewm(
            alpha=1 / self.period,
            adjust=False,
        ).mean()

        result["plus_di"] = plus_di
        result["minus_di"] = minus_di
        result[f"adx_{self.period}"] = adx

        return result