"""
Base Indicator

Abstract base class for all technical indicators.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class BaseIndicator(ABC):
    """
    Base class for all technical indicators.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Indicator name.
        """
        raise NotImplementedError

    @abstractmethod
    def calculate(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calculate indicator values.

        Args:
            data:
                OHLCV dataframe.

        Returns:
            DataFrame containing indicator values.
        """
        raise NotImplementedError