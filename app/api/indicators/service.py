# from __future__ import annotations

# import json
# import pandas as pd

# from app.core.exceptions import InsufficientDataError
# from app.market_engine.ohlc_aggregator import ohlc_aggregator
# from app.services.indicator.service import indicator_service
# from app.core.redis import redis_client


# class IndicatorsAPIService:

#     MIN_CANDLES = 30


#     async def get_latest_indicators(
#         self,
#         symbol: str,
#         timeframe: str,
#     ) -> dict:


#         symbol = symbol.upper()


#         # First try memory aggregator
#         candles = ohlc_aggregator.history(
#             symbol=symbol,
#             timeframe=timeframe,
#             limit=500,
#         )


#         # Fallback Redis
#         if len(candles) < self.MIN_CANDLES:

#             key = f"candles:{symbol}:{timeframe}"

#             data = await redis_client.lrange(
#                 key,
#                 0,
#                 -1
#             )


#             candles = [
#                 json.loads(item)
#                 for item in data
#             ]


#         if len(candles) < self.MIN_CANDLES:

#             raise InsufficientDataError(
#                 message=(
#                     f"Not enough candles for {symbol} "
#                     f"({timeframe}). "
#                     f"Available: {len(candles)}, "
#                     f"Need: {self.MIN_CANDLES}"
#                 ),
#                 status_code=422,
#             )


#         dataframe = pd.DataFrame(candles)


#         return indicator_service.latest(
#             dataframe
#         )


# indicators_api_service = IndicatorsAPIService()



from __future__ import annotations

import json
import math

import pandas as pd

from app.core.exceptions import InsufficientDataError
from app.market_engine.ohlc_aggregator import ohlc_aggregator
from app.services.indicator.service import indicator_service
from app.core.redis import redis_client


class IndicatorsAPIService:

    MIN_CANDLES = 30

    def _sanitize(self, value):
        """
        Recursively convert NaN/Infinity into None
        so FastAPI can serialize the response.
        """

        if isinstance(value, dict):
            return {
                k: self._sanitize(v)
                for k, v in value.items()
            }

        if isinstance(value, list):
            return [
                self._sanitize(v)
                for v in value
            ]

        if isinstance(value, tuple):
            return [
                self._sanitize(v)
                for v in value
            ]

        if isinstance(value, float):

            if math.isnan(value):
                return None

            if math.isinf(value):
                return None

            return value

        return value

    async def get_latest_indicators(
        self,
        symbol: str,
        timeframe: str,
    ) -> dict:

        symbol = symbol.upper()

        candles = ohlc_aggregator.history(
            symbol=symbol,
            timeframe=timeframe,
            limit=500,
        )

        if len(candles) < self.MIN_CANDLES:

            key = f"candles:{symbol}:{timeframe}"

            data = await redis_client.lrange(
                key,
                0,
                -1,
            )

            candles = [
                json.loads(item)
                for item in data
            ]

        if len(candles) < self.MIN_CANDLES:

            raise InsufficientDataError(
                message=(
                    f"Not enough candles for {symbol} "
                    f"({timeframe}). "
                    f"Available: {len(candles)}, "
                    f"Need: {self.MIN_CANDLES}"
                ),
                status_code=422,
            )

        dataframe = pd.DataFrame(candles)

        indicators = indicator_service.latest(
            dataframe
        )

        return self._sanitize(indicators)


indicators_api_service = IndicatorsAPIService()