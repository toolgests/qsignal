



# # """
# # Tick Processor

# # Processes incoming market ticks from Binance and Finnhub.
# # """

# # from __future__ import annotations

# # import json

# # from datetime import UTC, datetime
# # from decimal import Decimal
# # from typing import Any

# # from structlog import get_logger

# # from app.core.redis import redis_client
# # from app.websocket.manager import connection_manager
# # from app.market_engine.candle_builder import candle_builder


# # logger = get_logger(__name__)


# # class TickProcessor:

# #     def __init__(self) -> None:
# #         self._latest_ticks: dict[str, dict[str, Any]] = {}


# #     async def process(
# #         self,
# #         symbol: str,
# #         market: str,
# #         price: Decimal | float,
# #         volume: Decimal | float | None = None,
# #         timestamp: datetime | None = None,
# #     ):

# #         timestamp = timestamp or datetime.now(UTC)

# #         symbol = symbol.upper()

# #         price = Decimal(str(price))
# #         volume = Decimal(str(volume or 0))


# #         tick = {
# #             "symbol": symbol,
# #             "market": market.lower(),
# #             "price": price,
# #             "volume": volume,
# #             "timestamp": timestamp,
# #         }


# #         # =========================
# #         # MEMORY CACHE
# #         # =========================

# #         self._latest_ticks[symbol] = tick



# #         # =========================
# #         # SAVE TICK REDIS
# #         # =========================

# #         tick_key = f"tick:{symbol}"

# #         await redis_client.set(
# #             tick_key,
# #             json.dumps(
# #                 {
# #                     "symbol": symbol,
# #                     "market": market.lower(),
# #                     "price": float(price),
# #                     "volume": float(volume),
# #                     "timestamp": timestamp.isoformat(),
# #                 }
# #             ),
# #             ex=60,
# #         )


# #         # logger.info(
# #         #     "TICK SAVED REDIS",
# #         #     key=tick_key,
# #         #     price=float(price),
# #         # )



# #         # =========================
# #         # BUILD CANDLES
# #         # =========================

# #         timeframes = [
# #             1,
# #             4,
# #             5,
# #             15,
# #             60,
# #         ]


# #         for timeframe in timeframes:

# #             candle = await candle_builder.update(
# #                 symbol=symbol,
# #                 timeframe=timeframe,
# #                 price=price,
# #                 volume=volume,
# #                 timestamp=timestamp,
# #             )


# #             # print(
# #             #     "CANDLE CREATED:",
# #             #     candle
# #             # )


# #             candle_key = (
# #                 f"candles:{symbol}:{timeframe}m"
# #             )


# #             # Store candle history as LIST

# #             await redis_client.rpush(
# #                 candle_key,
# #                 json.dumps(
# #                     {
# #                         "symbol": candle["symbol"],
# #                         "timeframe": candle["timeframe"],
# #                         "open": float(candle["open"]),
# #                         "high": float(candle["high"]),
# #                         "low": float(candle["low"]),
# #                         "close": float(candle["close"]),
# #                         "volume": float(candle["volume"]),
# #                         "timestamp": candle["timestamp"].isoformat(),
# #                     }
# #                 ),
# #             )


# #             # print(
# #             #     "CANDLE SAVED:",
# #             #     candle_key
# #             # )



# #         # =========================
# #         # WEBSOCKET PUSH
# #         # =========================

# # #         logger.info(
# # #     "SENDING WS DATA",
# # #     symbol=symbol,
# # #     market=market,
# # #     price=float(price),
# # # )

# #         # await connection_manager.broadcast(
# #         #     {
# #         #         "event": "price",
# #         #         "symbol": symbol,
# #         #         "market": market.lower(),
# #         #         "price": float(price),
# #         #         "volume": float(volume),
# #         #         "timestamp": timestamp.isoformat(),
# #         #     }
# #         # )

# #         await redis_client.publish(
# #     "market_prices",
# #     json.dumps(
# #         {
# #             "event": "price",
# #             "symbol": symbol,
# #             "market": market.lower(),
# #             "price": float(price),
# #             "volume": float(volume),
# #             "timestamp": timestamp.isoformat(),
# #         }
# #     )
# # )


# #         return tick



# #     def latest(
# #         self,
# #         symbol: str
# #     ):

# #         return self._latest_ticks.get(
# #             symbol.upper()
# #         )



# #     def clear(self):

# #         self._latest_ticks.clear()



# #     @property
# #     def total_symbols(self):

# #         return len(self._latest_ticks)



# # tick_processor = TickProcessor()



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
# from app.market_engine.candle_builder import candle_builder
# from app.websocket.manager import connection_manager
# from app.api.home.service import home_service

# logger = get_logger(__name__)


# class TickProcessor:

#     def __init__(self) -> None:
#         self._latest_ticks: dict[str, dict[str, Any]] = {}

#     async def process(
#         self,
#         symbol: str,
#         market: str,
#         price: Decimal | float,
#         volume: Decimal | float | None = None,
#         timestamp: datetime | None = None,
#     ):

#         timestamp = timestamp or datetime.now(UTC)

#         symbol = symbol.upper()

#         price = Decimal(str(price))
#         volume = Decimal(str(volume or 0))

#         tick = {
#             "symbol": symbol,
#             "market": market.lower(),
#             "price": price,
#             "volume": volume,
#             "timestamp": timestamp,
#         }

#         # =========================
#         # MEMORY CACHE
#         # =========================

#         self._latest_ticks[symbol] = tick

#         # =========================
#         # SAVE LATEST TICK
#         # =========================

#         await redis_client.set(
#             f"tick:{symbol}",
#             json.dumps(
#                 {
#                     "symbol": symbol,
#                     "market": market.lower(),
#                     "price": float(price),
#                     "volume": float(volume),
#                     "timestamp": timestamp.isoformat(),
#                 }
#             ),
#             ex=60,
#         )

#         # =========================
#         # BUILD CANDLES
#         # =========================

#         for timeframe in (
#             1,
#             4,
#             5,
#             15,
#             60,
#         ):
#             await candle_builder.update(
#                 symbol=symbol,
#                 timeframe=timeframe,
#                 price=price,
#                 volume=volume,
#                 timestamp=timestamp,
#             )

#         # =========================
#         # SEND MARKET SNAPSHOT
#         # =========================

#         snapshot = await home_service.get_live_snapshot()
#         logger.info(
#     "HOME SNAPSHOT CREATED",
#     crypto=len(snapshot["crypto"]),
#     stocks=len(snapshot["stocks"]),
#     forex=len(snapshot["forex"]),
# )

#         await connection_manager.broadcast(snapshot)

#         return tick

#     def latest(
#         self,
#         symbol: str,
#     ):
#         return self._latest_ticks.get(symbol.upper())

#     def clear(self):
#         self._latest_ticks.clear()

#     @property
#     def total_symbols(self):
#         return len(self._latest_ticks)


# tick_processor = TickProcessor()


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
#         price: Decimal | float,
#         volume: Decimal | float | None = None,
#         timestamp: datetime | None = None,
#     ):

#         timestamp = timestamp or datetime.now(UTC)

#         symbol = symbol.upper()

#         price = Decimal(str(price))
#         volume = Decimal(str(volume or 0))


#         tick = {
#             "symbol": symbol,
#             "market": market.lower(),
#             "price": price,
#             "volume": volume,
#             "timestamp": timestamp,
#         }


#         # =========================
#         # MEMORY CACHE
#         # =========================

#         self._latest_ticks[symbol] = tick



#         # =========================
#         # SAVE TICK REDIS
#         # =========================

#         tick_key = f"tick:{symbol}"

#         await redis_client.set(
#             tick_key,
#             json.dumps(
#                 {
#                     "symbol": symbol,
#                     "market": market.lower(),
#                     "price": float(price),
#                     "volume": float(volume),
#                     "timestamp": timestamp.isoformat(),
#                 }
#             ),
#             ex=60,
#         )


#         # logger.info(
#         #     "TICK SAVED REDIS",
#         #     key=tick_key,
#         #     price=float(price),
#         # )



#         # =========================
#         # BUILD CANDLES
#         # =========================

#         timeframes = [
#             1,
#             4,
#             5,
#             15,
#             60,
#         ]


#         for timeframe in timeframes:

#             candle = await candle_builder.update(
#                 symbol=symbol,
#                 timeframe=timeframe,
#                 price=price,
#                 volume=volume,
#                 timestamp=timestamp,
#             )


#             # print(
#             #     "CANDLE CREATED:",
#             #     candle
#             # )


#             candle_key = (
#                 f"candles:{symbol}:{timeframe}m"
#             )


#             # Store candle history as LIST

#             await redis_client.rpush(
#                 candle_key,
#                 json.dumps(
#                     {
#                         "symbol": candle["symbol"],
#                         "timeframe": candle["timeframe"],
#                         "open": float(candle["open"]),
#                         "high": float(candle["high"]),
#                         "low": float(candle["low"]),
#                         "close": float(candle["close"]),
#                         "volume": float(candle["volume"]),
#                         "timestamp": candle["timestamp"].isoformat(),
#                     }
#                 ),
#             )


#             # print(
#             #     "CANDLE SAVED:",
#             #     candle_key
#             # )



#         # =========================
#         # WEBSOCKET PUSH
#         # =========================

# #         logger.info(
# #     "SENDING WS DATA",
# #     symbol=symbol,
# #     market=market,
# #     price=float(price),
# # )

#         # await connection_manager.broadcast(
#         #     {
#         #         "event": "price",
#         #         "symbol": symbol,
#         #         "market": market.lower(),
#         #         "price": float(price),
#         #         "volume": float(volume),
#         #         "timestamp": timestamp.isoformat(),
#         #     }
#         # )

#         await redis_client.publish(
#     "market_prices",
#     json.dumps(
#         {
#             "event": "price",
#             "symbol": symbol,
#             "market": market.lower(),
#             "price": float(price),
#             "volume": float(volume),
#             "timestamp": timestamp.isoformat(),
#         }
#     )
# )


#         return tick



#     def latest(
#         self,
#         symbol: str
#     ):

#         return self._latest_ticks.get(
#             symbol.upper()
#         )



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

import asyncio
import json
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from structlog import get_logger

from app.core.redis import redis_client
from app.market_engine.candle_builder import candle_builder
from app.websocket.manager import connection_manager
from app.api.home.service import home_service

logger = get_logger(__name__)


class TickProcessor:

    def __init__(self) -> None:
        self._latest_ticks: dict[str, dict[str, Any]] = {}
        self._last_snapshot_sent: float = 0.0
        self._snapshot_interval_seconds: float = 2.0

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
        # DAY OPEN (persisted in Redis so it survives restarts)
        # =========================

        day_key = f"day_open:{symbol}:{timestamp.strftime('%Y-%m-%d')}"

        await redis_client.set(
            day_key,
            str(price),
            nx=True,
            ex=90000,  # ~25h, comfortably covers the whole UTC day
        )

        day_open_raw = await redis_client.get(day_key)
        day_open = Decimal(day_open_raw) if day_open_raw else price

        change = price - day_open
        change_percent = (
            (change / day_open) * 100
            if day_open != 0
            else Decimal("0")
        )

        tick["change"] = float(change)
        tick["change_percent"] = float(change_percent)

        # =========================
        # MEMORY CACHE
        # =========================

        self._latest_ticks[symbol] = tick

        # =========================
        # SAVE LATEST TICK
        # =========================

        await redis_client.set(
            f"tick:{symbol}",
            json.dumps(
                {
                    "symbol": symbol,
                    "market": market.lower(),
                    "price": float(price),
                    "volume": float(volume),
                    "timestamp": timestamp.isoformat(),
                }
            ),
            ex=60,
        )

        # =========================
        # BUILD CANDLES
        # =========================

        for timeframe in (
            1,
            4,
            5,
            15,
            60,
        ):
            await candle_builder.update(
                symbol=symbol,
                timeframe=timeframe,
                price=price,
                volume=volume,
                timestamp=timestamp,
            )

        # =========================
        # SEND MARKET SNAPSHOT (throttled)
        # =========================
        #
        # This is a heavy, deeply-nested payload (all symbols x all
        # timeframes x up to 100 candles). Broadcasting it on every
        # single tick floods the socket and races against the
        # lightweight per-symbol "price" events sent by
        # websocket_worker every 100ms. Throttle it instead so the
        # home page still gets periodic full refreshes without
        # drowning out the price stream.

        now = asyncio.get_event_loop().time()

        if now - self._last_snapshot_sent >= self._snapshot_interval_seconds:

            self._last_snapshot_sent = now

            snapshot = await home_service.get_live_snapshot()

            # logger.info(
            #     "HOME SNAPSHOT CREATED",
            #     crypto=len(snapshot["crypto"]),
            #     stocks=len(snapshot["stocks"]),
            #     forex=len(snapshot["forex"]),
            # )

            await connection_manager.broadcast(snapshot)

        return tick

    def latest(
        self,
        symbol: str,
    ):
        return self._latest_ticks.get(symbol.upper())

    def clear(self):
        self._latest_ticks.clear()

    @property
    def total_symbols(self):
        return len(self._latest_ticks)


tick_processor = TickProcessor()