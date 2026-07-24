# """
# Candle Builder

# Builds real-time OHLC candles from incoming market ticks.
# """

# from __future__ import annotations

# from collections import defaultdict
# from datetime import UTC, datetime
# from decimal import Decimal
# from typing import Any


# class CandleBuilder:
#     """
#     Builds OHLC candles from live ticks.
#     """

#     def __init__(self) -> None:
#         self._candles: dict[tuple[str, str], dict[str, Any]] = {}

#     @staticmethod
#     def _floor_time(
#         timestamp: datetime,
#         timeframe: int,
#     ) -> datetime:
#         """
#         Floor timestamp to timeframe.

#         timeframe is in minutes.
#         """

#         timestamp = timestamp.astimezone(UTC)

#         minute = (
#             timestamp.minute // timeframe
#         ) * timeframe

#         return timestamp.replace(
#             minute=minute,
#             second=0,
#             microsecond=0,
#         )

#     def update(
#         self,
#         symbol: str,
#         timeframe: int,
#         price: Decimal,
#         volume: Decimal,
#         timestamp: datetime,
#     ) -> dict[str, Any]:
#         """
#         Update candle with new tick.
#         """

#         candle_time = self._floor_time(
#             timestamp,
#             timeframe,
#         )

#         key = (
#             symbol.upper(),
#             f"{timeframe}m",
#         )

#         candle = self._candles.get(key)

#         if candle is None or candle["timestamp"] != candle_time:

#             candle = {
#                 "symbol": symbol.upper(),
#                 "timeframe": f"{timeframe}m",
#                 "timestamp": candle_time,
#                 "open": price,
#                 "high": price,
#                 "low": price,
#                 "close": price,
#                 "volume": volume,
#             }

#             self._candles[key] = candle

#             return candle

#         candle["high"] = max(
#             candle["high"],
#             price,
#         )

#         candle["low"] = min(
#             candle["low"],
#             price,
#         )

#         candle["close"] = price

#         candle["volume"] += volume

#         return candle

#     def latest(
#         self,
#         symbol: str,
#         timeframe: int,
#     ) -> dict[str, Any] | None:
#         """
#         Return latest candle.
#         """

#         return self._candles.get(
#             (
#                 symbol.upper(),
#                 f"{timeframe}m",
#             )
#         )

#     def all(self) -> list[dict[str, Any]]:
#         """
#         Return all active candles.
#         """

#         return list(self._candles.values())

#     def clear(self) -> None:
#         """
#         Clear candle cache.
#         """

#         self._candles.clear()

#     @property
#     def total_candles(self) -> int:
#         """
#         Total active candles.
#         """

#         return len(self._candles)


# candle_builder = CandleBuilder()



from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from app.core.redis import redis_client


class CandleBuilder:
    """
    Builds OHLC candles from live ticks.
    """

    def __init__(self) -> None:
        self._candles: dict[tuple[str, str], dict[str, Any]] = {}


    @staticmethod
    def _floor_time(
        timestamp: datetime,
        timeframe: int,
    ) -> datetime:

        timestamp = timestamp.astimezone(UTC)

        minute = (
            timestamp.minute // timeframe
        ) * timeframe

        return timestamp.replace(
            minute=minute,
            second=0,
            microsecond=0,
        )


    async def update(
        self,
        symbol: str,
        timeframe: int,
        price: Decimal,
        volume: Decimal,
        timestamp: datetime,
    ) -> dict[str, Any]:

        candle_time = self._floor_time(
            timestamp,
            timeframe,
        )


        key = (
            symbol.upper(),
            f"{timeframe}m",
        )


        candle = self._candles.get(key)


        # New candle
        if candle is None or candle["timestamp"] != candle_time:

            candle = {
                "symbol": symbol.upper(),
                "timeframe": f"{timeframe}m",
                "timestamp": candle_time,
                "open": price,
                "high": price,
                "low": price,
                "close": price,
                "volume": volume,
            }

            self._candles[key] = candle


        # Update existing candle
        else:

            candle["high"] = max(
                candle["high"],
                price,
            )

            candle["low"] = min(
                candle["low"],
                price,
            )

            candle["close"] = price

            candle["volume"] += volume



        # Save latest candle in Redis
        redis_key = (
            f"candle:{symbol.upper()}:{timeframe}m"
        )


        # await redis_client.set(
        #     redis_key,
        #     json.dumps(
        #         {
        #             "symbol": candle["symbol"],
        #             "timeframe": candle["timeframe"],
        #             "timestamp": candle["timestamp"].isoformat(),
        #             "open": float(candle["open"]),
        #             "high": float(candle["high"]),
        #             "low": float(candle["low"]),
        #             "close": float(candle["close"]),
        #             "volume": float(candle["volume"]),
        #         }
        #     ),
        # )


        await redis_client.rpush(
            redis_key,
            json.dumps(
                {
                    "symbol": candle["symbol"],
                    "timeframe": candle["timeframe"],
                    "timestamp": candle["timestamp"].isoformat(),
                    "open": float(candle["open"]),
                    "high": float(candle["high"]),
                    "low": float(candle["low"]),
                    "close": float(candle["close"]),
                    "volume": float(candle["volume"]),
                }
            ),
        )


        # keep only last 500 candles
        await redis_client.ltrim(
            redis_key,
            -500,
            -1,
        )

        return candle



    def latest(
        self,
        symbol: str,
        timeframe: int,
    ) -> dict[str, Any] | None:

        return self._candles.get(
            (
                symbol.upper(),
                f"{timeframe}m",
            )
        )


    def all(self) -> list[dict[str, Any]]:
        """
        Return all active candles.
        """

        return list(self._candles.values())


    def clear(self) -> None:

        self._candles.clear()



candle_builder = CandleBuilder()