# """
# Market Stream

# Continuously receives live market data from providers
# and forwards it to the Market Engine.
# """

# from __future__ import annotations

# import asyncio

# from structlog import get_logger

# from app.core.constants import CRYPTO_SYMBOLS, FOREX_SYMBOLS, STOCK_SYMBOLS
# from app.market_engine.tick_processor import tick_processor
# from app.providers.binance.websocket.ws_client import binance_ws_client
# from app.providers.finnhub.websocket.ws_client import finnhub_ws_client

# logger = get_logger(__name__)


# class MarketStream:
#     """
#     Background market stream service.
#     """

#     def __init__(self) -> None:
#         self._running = False
#         self._tasks: list[asyncio.Task] = []

#     async def start(self) -> None:
#         """
#         Start all market streams.
#         """

#         if self._running:
#             return

#         logger.info("Starting Market Stream...")

#         self._running = True

#         # self._tasks = [
#         #     asyncio.create_task(
#         #         self._crypto_stream()
#         #     ),
#         #     asyncio.create_task(
#         #         self._forex_stream()
#         #     ),
#         #     asyncio.create_task(
#         #         self._stock_stream()
#         #     ),
#         # ]

#         self._tasks = [
#     asyncio.create_task(
#         self._crypto_stream()
#     ),
#     asyncio.create_task(
#         self._finnhub_stream()
#         ),
#     ]

#         logger.info(
#             "Market Stream started.",
#             workers=len(self._tasks),
#         )

#     async def stop(self) -> None:
#         """
#         Stop all streams.
#         """

#         logger.info("Stopping Market Stream...")

#         self._running = False

#         for task in self._tasks:
#             task.cancel()

#         if self._tasks:

#             await asyncio.gather(
#                 *self._tasks,
#                 return_exceptions=True,
#             )

#         self._tasks.clear()

#         logger.info("Market Stream stopped.")

#     async def _crypto_stream(self) -> None:
#         """
#         Listen Binance WebSocket.
#         """

#         async for tick in binance_ws_client.stream(CRYPTO_SYMBOLS):

#             if not self._running:
#                 break

#             await tick_processor.process(
#                 symbol=tick["symbol"],
#                 market="crypto",
#                 price=tick["price"],
#                 volume=tick.get("volume", 0),
#                 timestamp=tick["timestamp"],
#             )


# async def _finnhub_stream(self) -> None:
#     """
#     Listen Finnhub Forex + Stock streams.
#     """

#     symbols = FOREX_SYMBOLS + STOCK_SYMBOLS

#     async for tick in finnhub_ws_client.stream(symbols):

#         if not self._running:
#             break

#         market = (
#             "forex"
#             if tick["symbol"] in FOREX_SYMBOLS
#             else "stocks"
#         )

#         await tick_processor.process(
#             symbol=tick["symbol"],
#             market=market,
#             price=tick["price"],
#             volume=tick.get("volume", 0),
#             timestamp=tick["timestamp"],
#         )
#     # async def _forex_stream(self) -> None:
#     #     """
#     #     Listen Finnhub Forex stream.
#     #     """

#     #     async for tick in finnhub_ws_client.stream(FOREX_SYMBOLS):

#     #         if not self._running:
#     #             break

#     #         await tick_processor.process(
#     #             symbol=tick["symbol"],
#     #             market="forex",
#     #             price=tick["price"],
#     #             volume=tick.get("volume", 0),
#     #             timestamp=tick["timestamp"],
#     #         )

#     # async def _stock_stream(self) -> None:
#     #     """
#     #     Listen Finnhub Stock stream.
#     #     """

#     #     async for tick in finnhub_ws_client.stream(STOCK_SYMBOLS):

#     #         if not self._running:
#     #             break

#     #         await tick_processor.process(
#     #             symbol=tick["symbol"],
#     #             market="stocks",
#     #             price=tick["price"],
#     #             volume=tick.get("volume", 0),
#     #             timestamp=tick["timestamp"],
#     #         )


# market_stream = MarketStream()


"""
Market Stream

Continuously receives live market data from providers
and forwards it to the Market Engine.
"""

from __future__ import annotations

import asyncio

from structlog import get_logger

from app.core.constants import (
    CRYPTO_SYMBOLS,
    FOREX_SYMBOLS,
    STOCK_SYMBOLS,
)
from app.market_engine.tick_processor import tick_processor
from app.providers.binance.websocket.ws_client import binance_ws_client
from app.providers.finnhub.websocket.ws_client import finnhub_ws_client

logger = get_logger(__name__)


class MarketStream:
    """
    Background market stream service.
    """

    def __init__(self) -> None:
        self._running = False
        self._tasks: list[asyncio.Task] = []

    async def start(self) -> None:
        """
        Start all market streams.
        """

        if self._running:
            return

        logger.info("Starting Market Stream...")

        self._running = True

        self._tasks = [
            asyncio.create_task(
                self._crypto_stream()
            ),
            asyncio.create_task(
                self._finnhub_stream()
            ),
        ]

        for task in self._tasks:
            logger.info(
                "BACKGROUND TASK STARTED",
                task=task.get_name()
            )

    async def stop(self) -> None:
        """
        Stop all streams.
        """

        logger.info("Stopping Market Stream...")

        self._running = False

        for task in self._tasks:
            task.cancel()

        if self._tasks:
            await asyncio.gather(
                *self._tasks,
                return_exceptions=True,
            )

        self._tasks.clear()

        logger.info("Market Stream stopped.")

    async def _crypto_stream(self) -> None:
        """
        Listen Binance WebSocket.
        """

        async for tick in binance_ws_client.stream(CRYPTO_SYMBOLS):

        #     logger.info(
        #     "CRYPTO TICK RECEIVED",
        #     symbol=tick["symbol"],
        #     price=tick["price"],
        # )
        #     logger.info(
        #     "BINANCE TICK RECEIVED",
        #     tick=tick
        # )



            if not self._running:
                break

            await tick_processor.process(
                symbol=tick["symbol"],
                market="crypto",
                price=tick["price"],
                volume=tick.get("volume", 0),
                timestamp=tick["timestamp"],
            )

    async def _finnhub_stream(self) -> None:
        
        """
        Listen Finnhub Forex + Stock streams.
        Uses one WebSocket connection for all symbols.

        """

        print("🔥 FINNHUB FUNCTION ENTERED")

        logger.info(
            "Starting Finnhub Stream3534"
        )

        # logger.info("Starting Finnhub Stream34")

        symbols = FOREX_SYMBOLS + STOCK_SYMBOLS

        logger.info(
            "Starting Finnhub stream",
            symbols=symbols,
        )

        async for tick in finnhub_ws_client.stream(symbols):

            # print("FINNHUB TICK:", tick)

            # logger.info(
            #     "FINNHUB TICK RECEIVED",
            #     tick=tick,
            # )

            if not self._running:
                break

            symbol = tick["symbol"]

            market = (
                "forex"
                if symbol in FOREX_SYMBOLS
                else "stocks"
            )

            await tick_processor.process(
                symbol=symbol,
                market=market,
                price=tick["price"],
                volume=tick.get("volume", 0),
                timestamp=tick["timestamp"],
            )


market_stream = MarketStream()