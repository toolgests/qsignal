"""
Indicator Service

Calculates all technical indicators for OHLCV market data.
"""

from __future__ import annotations

import pandas as pd

from app.indicators.adx import ADXIndicator
from app.indicators.atr import ATRIndicator
from app.indicators.bollinger_bands import BollingerBandsIndicator
from app.indicators.ema import EMAIndicator
from app.indicators.macd import MACDIndicator
from app.indicators.rsi import RSIIndicator
from app.indicators.sma import SMAIndicator
from app.indicators.vwap import VWAPIndicator


class IndicatorService:
    """
    Service responsible for technical indicator calculations.
    """

    def __init__(self) -> None:
        self.sma = SMAIndicator()
        self.ema = EMAIndicator()
        self.rsi = RSIIndicator()
        self.macd = MACDIndicator()
        self.atr = ATRIndicator()
        self.adx = ADXIndicator()
        self.vwap = VWAPIndicator()
        self.bollinger = BollingerBandsIndicator()

    def calculate_all(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calculate all configured indicators.
        """

        result = data.copy()

        result = self.sma.calculate(result)
        result = self.ema.calculate(result)
        result = self.rsi.calculate(result)
        result = self.macd.calculate(result)
        result = self.atr.calculate(result)
        result = self.adx.calculate(result)
        result = self.vwap.calculate(result)
        result = self.bollinger.calculate(result)

        return result

    def latest(self, data: pd.DataFrame) -> dict:
        """
        Return latest indicator values.
        """

        result = self.calculate_all(data)

        return result.iloc[-1].to_dict()


indicator_service = IndicatorService()