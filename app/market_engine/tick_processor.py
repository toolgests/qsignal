



# """
# Tick Processor

# Processes incoming market ticks from Binance and Finnhub.
# """

# from __future__ import annotations

# import json

# from datetime import UTC, datetime
# from decimal import Decimal
# from typing import Any

# from structlog import get_logger

# from app.core.redis import redis_client
# from app.websocket.manager import connection_manager
# from app.market_engine.candle_builder import candle_builder


# logger = get_logger(__name__)


# class TickProcessor:

#     def __init__(self) -> None:
#         self._latest_ticks: dict[str, dict[str, Any]] = {}


#     async def process(
#         self,
#         symbol: str,
#         market: str,
#         price: Decimal,
#         volume: Decimal | None = None,
#         timestamp: datetime | None = None,
#     ):

#         timestamp = timestamp or datetime.now(UTC)

#         price = Decimal(price)
#         volume = Decimal(volume or 0)


#         tick = {
#             "symbol": symbol.upper(),
#             "market": market.lower(),
#             "price": price,
#             "volume": volume,
#             "timestamp": timestamp,
#         }


#         # memory cache
#         self._latest_ticks[symbol.upper()] = tick


#         # ============================
#         # SAVE TICK IN REDIS
#         # ============================

#         await redis_client.set(
#             f"tick:{symbol.upper()}",
#             json.dumps(
#                 {
#                     "symbol": symbol.upper(),
#                     "market": market.lower(),
#                     "price": float(price),
#                     "volume": float(volume),
#                     "timestamp": timestamp.isoformat(),
#                 }
#             ),
#         )


#         # ============================
#         # BUILD CANDLE
#         # ============================

#         candle = await candle_builder.update(
#             symbol=symbol,
#             timeframe=1,
#             price=price,
#             volume=volume,
#             timestamp=timestamp,
#         )
#         # print("CANDLE CREATED:", candle)

#         # save candle redis

#         await redis_client.set(
#             f"candle:{symbol.upper()}:1m",
#             json.dumps(
#                 {
#                     "symbol": candle["symbol"],
#                     "timeframe": candle["timeframe"],
#                     "open": float(candle["open"]),
#                     "high": float(candle["high"]),
#                     "low": float(candle["low"]),
#                     "close": float(candle["close"]),
#                     "volume": float(candle["volume"]),
#                     "timestamp": candle["timestamp"].isoformat(),
#                 }
#             ),
#         )


#         # websocket price push

#         await connection_manager.broadcast(
#             {
#                 "event":"price",
#                 "symbol":symbol.upper(),
#                 "market":market.lower(),
#                 "price":float(price),
#                 "volume":float(volume),
#                 "timestamp":timestamp.isoformat(),
#             }
#         )


#         return tick



#     def latest(self,symbol:str):
#         return self._latest_ticks.get(symbol.upper())


#     def clear(self):
#         self._latest_ticks.clear()


#     @property
#     def total_symbols(self):
#         return len(self._latest_ticks)



# tick_processor = TickProcessor()



"""
Tick Processor

Processes incoming market ticks from Binance and Finnhub.
"""

from __future__ import annotations

import json

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from structlog import get_logger

from app.core.redis import redis_client
from app.websocket.manager import connection_manager
from app.market_engine.candle_builder import candle_builder


logger = get_logger(__name__)


class TickProcessor:

    def __init__(self) -> None:
        self._latest_ticks: dict[str, dict[str, Any]] = {}


    async def process(
        self,
        symbol: str,
        market: str,
        price: Decimal | float,
        volume: Decimal | float | None = None,
        timestamp: datetime | None = None,
    ):

        timestamp = timestamp or datetime.now(UTC)

        symbol = symbol.upper()

        price = Decimal(str(price))
        volume = Decimal(str(volume or 0))


        tick = {
            "symbol": symbol,
            "market": market.lower(),
            "price": price,
            "volume": volume,
            "timestamp": timestamp,
        }


        # =========================
        # MEMORY CACHE
        # =========================

        self._latest_ticks[symbol] = tick



        # =========================
        # SAVE TICK REDIS
        # =========================

        tick_key = f"tick:{symbol}"

        await redis_client.set(
            tick_key,
            json.dumps(
                {
                    "symbol": symbol,
                    "market": market.lower(),
                    "price": float(price),
                    "volume": float(volume),
                    "timestamp": timestamp.isoformat(),
                }
            ),
            ex=86400,
        )


        # logger.info(
        #     "TICK SAVED REDIS",
        #     key=tick_key,
        #     price=float(price),
        # )



        # =========================
        # BUILD CANDLES
        # =========================

        timeframes = [
            1,
            4,
            5,
            15,
            60,
        ]


        for timeframe in timeframes:

            candle = await candle_builder.update(
                symbol=symbol,
                timeframe=timeframe,
                price=price,
                volume=volume,
                timestamp=timestamp,
            )


            # print(
            #     "CANDLE CREATED:",
            #     candle
            # )


            candle_key = (
                f"candles:{symbol}:{timeframe}m"
            )


            # Store candle history as LIST

            await redis_client.rpush(
                candle_key,
                json.dumps(
                    {
                        "symbol": candle["symbol"],
                        "timeframe": candle["timeframe"],
                        "open": float(candle["open"]),
                        "high": float(candle["high"]),
                        "low": float(candle["low"]),
                        "close": float(candle["close"]),
                        "volume": float(candle["volume"]),
                        "timestamp": candle["timestamp"].isoformat(),
                    }
                ),
            )


            # print(
            #     "CANDLE SAVED:",
            #     candle_key
            # )



        # =========================
        # WEBSOCKET PUSH
        # =========================

        logger.info(
    "SENDING WS DATA",
    symbol=symbol,
    market=market,
    price=float(price),
)

        await connection_manager.broadcast(
            {
                "event": "price",
                "symbol": symbol,
                "market": market.lower(),
                "price": float(price),
                "volume": float(volume),
                "timestamp": timestamp.isoformat(),
            }
        )


        return tick



    def latest(
        self,
        symbol: str
    ):

        return self._latest_ticks.get(
            symbol.upper()
        )



    def clear(self):

        self._latest_ticks.clear()



    @property
    def total_symbols(self):

        return len(self._latest_ticks)



tick_processor = TickProcessor()