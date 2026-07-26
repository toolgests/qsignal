# """
# Binance WebSocket Client

# Production-ready asynchronous Binance WebSocket client.
# """

# from __future__ import annotations

# import asyncio
# import json
# from datetime import UTC, datetime

# import websockets
# from websockets.client import WebSocketClientProtocol
# from websockets.exceptions import ConnectionClosed

# from app.core.config import config
# from app.logging import get_logger
# from app.providers.binance.parser.parser import binance_parser

# logger = get_logger(__name__)


# class BinanceWebSocketClient:
#     """
#     Binance WebSocket client with automatic reconnect.
#     """

#     def __init__(self) -> None:
#         self._connection: WebSocketClientProtocol | None = None
#         self._running = False

#     async def connect(self, streams: list[str]) -> None:
#         """
#         Connect to Binance WebSocket.
#         """

#         stream_url = "/".join(stream.lower() for stream in streams)

#         # url = f"{config.BINANCE_WS_URL}/stream?streams={stream_url}"
#         url = "wss://stream.binance.com:9443/stream?streams=btcusdt@trade/ethusdt@trade"

#         self._running = True

#         while self._running:

#             try:

#                 logger.info(
#                     "Connecting to Binance WebSocket",
#                     url=url,
#                 )

#                 async with websockets.connect(
#                     url,
#                     ping_interval=20,
#                     ping_timeout=20,
#                     close_timeout=5,
#                 ) as websocket:

#                     self._connection = websocket

#                     logger.info("Connected to Binance")

#                     await self.listen()

#             except ConnectionClosed:

#                 logger.warning("Binance WebSocket disconnected")

#             except Exception as exc:

#                 logger.error(
#                     "Binance WebSocket Error",
#                     error=str(exc),
#                 )

#             logger.info("Reconnecting in 5 seconds...")

#             await asyncio.sleep(5)

#     async def listen(self) -> None:
#         """
#         Listen for incoming WebSocket messages.
#         """

#         assert self._connection is not None

#         async for message in self._connection:

#             payload = json.loads(message)

#             await self.process_message(payload)

#     async def process_message(self, payload: dict) -> None:
#         """
#         Process Binance WebSocket payload.
#         """

#         data = payload.get("data")

#         if not data:
#             return

#         event_type = data.get("e")

#         if event_type == "trade":

#             trade = binance_parser.parse_trade(data)

#             logger.info(
#                 "Trade Received",
#                 symbol=trade.symbol,
#                 price=str(trade.price),
#             )

#         elif event_type == "24hrTicker":

#             ticker = binance_parser.parse_24hr_ticker(data)

#             logger.info(
#                 "Ticker Updated",
#                 symbol=ticker.symbol,
#                 price=str(ticker.last_price),
#             )

#     async def disconnect(self) -> None:
#         """
#         Disconnect WebSocket.
#         """

#         self._running = False

#         if self._connection:

#             await self._connection.close()

#             logger.info("Binance WebSocket closed")

#     async def stream(self, symbols: list[str]):
#         """
#         Async generator yielding normalized ticks for the given symbols.

#         Reconnects automatically on failure.
#         """

#         streams = [f"{symbol.lower()}@trade" for symbol in symbols]

#         stream_url = "/".join(streams)
#         url = "wss://stream.binance.com:9443/stream?streams=btcusdt@trade/ethusdt@trade"

#         # url = f"{config.BINANCE_WS_URL}/stream?streams={stream_url}"

#         self._running = True

#         while self._running:

#             try:

#                 logger.info("Connecting to Binance WebSocket", url=url)

#                 async with websockets.connect(
#                     url,
#                     ping_interval=20,
#                     ping_timeout=20,
#                     close_timeout=5,
#                 ) as websocket:

#                     self._connection = websocket

#                     logger.info("Connected to Binance")

#                     async for message in websocket:

#                         if not self._running:
#                             break

#                         payload = json.loads(message)

#                         data = payload.get("data")

#                         if not data or data.get("e") != "trade":
#                             continue

#                         trade = binance_parser.parse_trade(data)

#                         yield {
#                             "symbol": trade.symbol,
#                             "price": trade.price,
#                             "volume": trade.quantity,
#                             "timestamp": datetime.fromtimestamp(
#                                 trade.trade_time / 1000,
#                                 tz=UTC,
#                             ),
#                         }

#             except ConnectionClosed:

#                 logger.warning("Binance WebSocket disconnected")

#             except Exception as exc:

#                 logger.error("Binance WebSocket Error", error=str(exc))

#             if not self._running:
#                 break

#             logger.info("Reconnecting in 5 seconds...")

#             await asyncio.sleep(5)


# binance_ws_client = BinanceWebSocketClient()



"""
Coinbase WebSocket Client

Production-ready asynchronous Coinbase Advanced Trade WebSocket client.
"""

from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime

import websockets
from websockets.client import WebSocketClientProtocol
from websockets.exceptions import ConnectionClosed

from app.logging import get_logger
from app.providers.binance.parser.parser import binance_parser

logger = get_logger(__name__)


class CoinbaseWebSocketClient:
    """
    Coinbase WebSocket client with automatic reconnect.
    """

    WS_URL = "wss://advanced-trade-ws.coinbase.com"

    def __init__(self) -> None:

        self._connection: WebSocketClientProtocol | None = None
        self._running = False


    def subscribe_message(
        self,
        symbols: list[str],
    ) -> dict:

        """
        Coinbase subscription payload.
        """

        products = [
            symbol.upper()
            for symbol in symbols
        ]

        return {
            "type": "subscribe",
            "channel": "market_trades",
            "product_ids": products,
        }


    async def connect(
        self,
        symbols: list[str],
    ) -> None:

        """
        Connect Coinbase WebSocket.
        """

        self._running = True


        while self._running:

            try:

                logger.info(
                    "Connecting to Coinbase WebSocket",
                    url=self.WS_URL,
                )


                async with websockets.connect(
                    self.WS_URL,
                    ping_interval=20,
                    ping_timeout=20,
                    close_timeout=5,
                ) as websocket:


                    self._connection = websocket


                    await websocket.send(
                        json.dumps(
                            self.subscribe_message(
                                symbols
                            )
                        )
                    )


                    logger.info(
                        "Connected to Coinbase"
                    )


                    await self.listen()


            except ConnectionClosed:

                logger.warning(
                    "Coinbase WebSocket disconnected"
                )


            except Exception as exc:

                logger.error(
                    "Coinbase WebSocket Error",
                    error=str(exc),
                )


            logger.info(
                "Reconnecting in 5 seconds..."
            )


            await asyncio.sleep(5)



    async def listen(self) -> None:

        """
        Listen incoming messages.
        """

        assert self._connection is not None


        async for message in self._connection:

            payload = json.loads(message)


            await self.process_message(
                payload
            )



    async def process_message(
        self,
        payload: dict,
    ) -> None:

        """
        Process Coinbase messages.
        """


        if payload.get("channel") != "market_trades":

            return


        try:

            trades = (
                payload
                .get("events", [])
            )


            for event in trades:

                for trade_data in event.get(
                    "trades",
                    []
                ):

                    trade = (
                        binance_parser
                        # coinbase_parser
                        .parse_trade(
                            trade_data
                        )
                    )


                    logger.info(
                        "Trade Received",
                        symbol=trade.symbol,
                        price=str(trade.price),
                    )


        except Exception as exc:

            logger.error(
                "Trade Processing Error",
                error=str(exc),
            )



    async def stream(
        self,
        symbols: list[str],
    ):

        """
        Async generator yielding normalized ticks.
        """


        self._running = True


        while self._running:


            try:


                logger.info(
                    "Connecting to Coinbase WebSocket",
                    url=self.WS_URL,
                )


                async with websockets.connect(
                    self.WS_URL,
                    ping_interval=20,
                    ping_timeout=20,
                    close_timeout=5,
                ) as websocket:


                    self._connection = websocket


                    await websocket.send(
                        json.dumps(
                            self.subscribe_message(
                                symbols
                            )
                        )
                    )


                    logger.info(
                        "Coinbase Connected"
                    )



                    async for message in websocket:


                        if not self._running:

                            break


                        payload = json.loads(
                            message
                        )


                        if (
                            payload.get("channel")
                            != "market_trades"
                        ):

                            continue



                        for event in payload.get(
                            "events",
                            []
                        ):


                            for trade_data in event.get(
                                "trades",
                                []
                            ):


                                trade = (
                                    binance_parser
                                    # coinbase_parser
                                    .parse_trade(
                                        trade_data
                                    )
                                )


                                yield {

                                    "symbol":
                                        trade.symbol,


                                    "price":
                                        trade.price,


                                    "volume":
                                        trade.quantity,
                                    "timestamp":
                                        datetime.fromtimestamp(
                                            trade.trade_time / 1000,
                                            tz=UTC,
                                        ),

                                    # "timestamp":
                                    #     datetime.fromtimestamp(
                                    #         trade.time / 1000,
                                    #         tz=UTC,
                                    #     ),

                                }



            except ConnectionClosed:

                logger.warning(
                    "Coinbase disconnected"
                )


            except Exception as exc:

                logger.error(
                    "Coinbase Stream Error",
                    error=str(exc),
                )



            if not self._running:

                break



            await asyncio.sleep(5)



    async def disconnect(self):

        """
        Close WebSocket.
        """


        self._running = False


        if self._connection:

            await self._connection.close()


            logger.info(
                "Coinbase WebSocket closed"
            )



binance_ws_client = CoinbaseWebSocketClient()