# """
# Signal Service

# Coordinates OHLC history with the signal engine to produce
# trading signals for a given symbol / timeframe.
# """

# from __future__ import annotations

# import pandas as pd

# from app.core.exceptions import InsufficientDataError
# from app.market_engine.ohlc_aggregator import ohlc_aggregator
# from app.signal_engine.models import SignalResponse
# from app.signal_engine.signal_generator import signal_generator


# class SignalService:
#     """
#     Service responsible for producing trading signals.
#     """

#     MIN_CANDLES = 30

#     def generate_signal(
#         self,
#         symbol: str,
#         market: str,
#         timeframe: str,
#     ) -> SignalResponse:
#         """
#         Generate a trading signal from the latest stored candles.
#         """

#         candles = ohlc_aggregator.history(
#             symbol=symbol,
#             timeframe=timeframe,
#             limit=500,
#         )

#         if len(candles) < self.MIN_CANDLES:
#             raise InsufficientDataError(
#                 message=(
#                     f"Not enough candles for {symbol} ({timeframe}) to "
#                     f"generate a signal. Need at least {self.MIN_CANDLES}."
#                 ),
#                 status_code=422,
#             )

#         dataframe = pd.DataFrame(candles)

#         return signal_generator.generate(
#             symbol=symbol,
#             market=market,
#             timeframe=timeframe,
#             data=dataframe,
#         )


# signal_service = SignalService()


"""
Signal Service

Generates trading signals from candle data.
"""

from __future__ import annotations

import pandas as pd

from app.core.exceptions import InsufficientDataError
from app.signal_engine.models import SignalResponse
from app.signal_engine.signal_generator import signal_generator


class SignalService:

    MIN_CANDLES = 30

    def generate_signal(
        self,
        symbol: str,
        market: str,
        timeframe: str,
        candles: list[dict],
    ) -> SignalResponse:
        """
        Generate trading signal from candle history.
        """

        if len(candles) < self.MIN_CANDLES:
            raise InsufficientDataError(
                message=(
                    f"Not enough candles for {symbol} ({timeframe}) "
                    f"to generate a signal. Need at least "
                    f"{self.MIN_CANDLES}."
                ),
                status_code=422,
            )

        dataframe = pd.DataFrame(candles)

        return signal_generator.generate(
            symbol=symbol,
            market=market,
            timeframe=timeframe,
            data=dataframe,
        )


signal_service = SignalService()