# """
# Signal Generator

# Generates trading signals using technical indicators,
# voting engine and confidence calculator.
# """

# from __future__ import annotations

# import pandas as pd

# from app.services.indicator.service import indicator_service
# from app.signal_engine.confidence_calculator import confidence_calculator
# from app.signal_engine.models import (
#     IndicatorVote,
#     SignalResponse,
# )
# from app.signal_engine.voting_engine import voting_engine


# class SignalGenerator:
#     """
#     Generate trading signals from OHLCV data.
#     """

#     def generate(
#         self,
#         symbol: str,
#         market: str,
#         timeframe: str,
#         data: pd.DataFrame,
#     ) -> SignalResponse:
#         """
#         Generate trading signal.

#         Args:
#             symbol:
#                 Trading symbol.

#             market:
#                 crypto / forex / stocks

#             timeframe:
#                 1m, 5m, 1h ...

#             data:
#                 OHLCV dataframe.

#         Returns:
#             SignalResponse
#         """

#         dataframe = indicator_service.calculate_all(data)

#         latest = dataframe.iloc[-1].to_dict()

#         vote_result = voting_engine.vote(latest)

#         total_votes = (
#             vote_result["buy_votes"]
#             + vote_result["sell_votes"]
#         )

#         confidence = confidence_calculator.calculate(
#             buy_votes=vote_result["buy_votes"],
#             sell_votes=vote_result["sell_votes"],
#             total_votes=total_votes,
#         )

#         indicator_votes = []

#         for key, value in latest.items():

#             if key in {
#                 "close",
#                 "high",
#                 "low",
#                 "open",
#                 "volume",
#             }:
#                 continue

#             indicator_votes.append(
#                 IndicatorVote(
#                     indicator=key,
#                     signal="INFO",
#                     value=value,
#                 )
#             )

#         return SignalResponse(
#             symbol=symbol,
#             market=market,
#             timeframe=timeframe,
#             price=latest["close"],
#             signal=vote_result["signal"],
#             confidence=confidence["confidence"],
#             strength=confidence["strength"],
#             buy_votes=vote_result["buy_votes"],
#             sell_votes=vote_result["sell_votes"],
#             indicators=indicator_votes,
#         )


# signal_generator = SignalGenerator()


"""
Signal Generator

Generates trading signals using technical indicators,
voting engine and confidence calculator.
"""

from __future__ import annotations

import math
from decimal import Decimal

import pandas as pd

from app.services.indicator.service import indicator_service
from app.signal_engine.confidence_calculator import confidence_calculator
from app.signal_engine.models import (
    IndicatorVote,
    SignalResponse,
)
from app.signal_engine.voting_engine import voting_engine


class SignalGenerator:
    """
    Generate trading signals from OHLCV data.
    """

    def generate(
        self,
        symbol: str,
        market: str,
        timeframe: str,
        data: pd.DataFrame,
    ) -> SignalResponse:
        """
        Generate trading signal.
        """

        dataframe = indicator_service.calculate_all(data)

        latest = dataframe.iloc[-1].to_dict()

        vote_result = voting_engine.vote(latest)

        total_votes = (
            vote_result["buy_votes"]
            + vote_result["sell_votes"]
        )

        confidence = confidence_calculator.calculate(
            buy_votes=vote_result["buy_votes"],
            sell_votes=vote_result["sell_votes"],
            total_votes=total_votes,
        )

        indicator_votes: list[IndicatorVote] = []

        skip_fields = {
            "symbol",
            "market",
            "timeframe",
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
        }

        for key, value in latest.items():

            if key in skip_fields:
                continue

            if value is None:
                continue

            if isinstance(value, Decimal):
                value = float(value)

            if not isinstance(value, (int, float)):
                continue

            if isinstance(value, float):
                if math.isnan(value):
                    continue

                if math.isinf(value):
                    continue

            indicator_votes.append(
                IndicatorVote(
                    indicator=key,
                    signal="INFO",
                    value=float(value),
                )
            )

        return SignalResponse(
            symbol=symbol,
            market=market,
            timeframe=timeframe,
            price=float(latest["close"]),
            signal=vote_result["signal"],
            confidence=confidence["confidence"],
            strength=confidence["strength"],
            buy_votes=vote_result["buy_votes"],
            sell_votes=vote_result["sell_votes"],
            indicators=indicator_votes,
        )


signal_generator = SignalGenerator()