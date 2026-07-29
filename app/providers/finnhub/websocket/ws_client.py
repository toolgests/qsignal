# # """
# # Finnhub WebSocket Client

# # Production-ready asynchronous WebSocket client for Finnhub.
# # """

# # from __future__ import annotations

# # import asyncio
# # import json

# # import websockets
# # from websockets.client import WebSocketClientProtocol
# # from websockets.exceptions import ConnectionClosed

# # from app.core.config import config
# # from app.logging import get_logger

# # logger = get_logger(__name__)


# # class FinnhubWebSocketClient:
# #     """
# #     Finnhub WebSocket client with auto reconnect.
# #     """

# #     def __init__(self) -> None:
# #         self._connection: WebSocketClientProtocol | None = None
# #         self._running = False

        

# #     # async def connect(self) -> None:
# #     #     """
# #     #     Connect to Finnhub WebSocket.
# #     #     """

# #     #     self._running = True

# #     #     url = f"{config.FINNHUB_WS_URL}?token={config.FINNHUB_API_KEY}"

# #     #     while self._running:
# #     #         try:
# #     #             logger.info("Connecting to Finnhub WebSocket")

# #     #             async with websockets.connect(
# #     #                 url,
# #     #                 ping_interval=20,
# #     #                 ping_timeout=20,
# #     #             ) as websocket:

# #     #                 self._connection = websocket

# #     #                 logger.info("Connected to Finnhub")

# #     #                 await self.listen()

# #     #         except ConnectionClosed:

# #     #             logger.warning("Finnhub WebSocket disconnected")

# #     #         except Exception as exc:

# #     #             logger.error(
# #     #                 "Finnhub WebSocket Error",
# #     #                 error=str(exc),
# #     #             )

# #     #         logger.info("Reconnecting in 5 seconds...")

# #     #         await asyncio.sleep(5)

# #     async def subscribe(self, symbol: str) -> None:
# #         """
# #         Subscribe to a symbol.
# #         """

# #         if self._connection is None:
# #             return

# #         await self._connection.send(
# #             json.dumps(
# #                 {
# #                     "type": "subscribe",
# #                     "symbol": symbol,
# #                 }
# #             )
# #         )

# #     async def unsubscribe(self, symbol: str) -> None:
# #         """
# #         Unsubscribe from a symbol.
# #         """

# #         if self._connection is None:
# #             return

# #         await self._connection.send(
# #             json.dumps(
# #                 {
# #                     "type": "unsubscribe",
# #                     "symbol": symbol,
# #                 }
# #             )
# #         )

# #     async def listen(self) -> None:
# #         """
# #         Listen for incoming messages.
# #         """

# #         assert self._connection is not None

# #         async for message in self._connection:

# #             payload = json.loads(message)

# #             logger.info(
# #                 "Finnhub Message",
# #                 payload=payload,
# #             )

# #     async def disconnect(self) -> None:
# #         """
# #         Close the WebSocket connection.
# #         """

# #         self._running = False

# #         if self._connection:

# #             await self._connection.close()

# #             logger.info("Finnhub WebSocket closed")

# #     async def stream(self, symbols: list[str]):
# #         """
# #         Async generator yielding normalized ticks for the given symbols.

# #         Reconnects automatically on failure.
# #         """

# #         from datetime import UTC, datetime

# #         url = f"{config.FINNHUB_WS_URL}?token={config.FINNHUB_API_KEY}"

# #         self._running = True

# #         while self._running:

# #             try:

# #                 logger.info("Connecting to Finnhub WebSocket")

# #                 async with websockets.connect(
# #                     url,
# #                     ping_interval=20,
# #                     ping_timeout=20,
# #                 ) as websocket:

# #                     self._connection = websocket

# #                     logger.info("Connected to Finnhub")

# #                     for symbol in symbols:
# #                         await websocket.send(
# #                             json.dumps(
# #                                 {
# #                                     "type": "subscribe",
# #                                     "symbol": symbol,
# #                                 }
# #                             )
# #                         )

# #                     async for message in websocket:

# #                         if not self._running:
# #                             break

# #                         payload = json.loads(message)

# #                         if payload.get("type") != "trade":
# #                             continue

# #                         for trade in payload.get("data", []):

# #                             yield {
# #                                 "symbol": trade["s"],
# #                                 "price": trade["p"],
# #                                 "volume": trade.get("v", 0),
# #                                 "timestamp": datetime.fromtimestamp(
# #                                     trade["t"] / 1000,
# #                                     tz=UTC,
# #                                 ),
# #                             }

# #             except ConnectionClosed:

# #                 logger.warning("Finnhub WebSocket disconnected")

# #             except Exception as exc:

# #                 logger.error("Finnhub WebSocket Error", error=str(exc))

# #             if not self._running:
# #                 break

# #             logger.info("Reconnecting in 5 seconds...")

# #             await asyncio.sleep(5)


# # finnhub_ws_client = FinnhubWebSocketClient()


# # """
# # Finnhub WebSocket Client

# # Production-ready asynchronous WebSocket client for Finnhub.
# # """

# # from __future__ import annotations

# # import asyncio
# # import json
# # from datetime import UTC, datetime
# # from datetime import UTC, datetime

# # import websockets
# # from websockets.exceptions import ConnectionClosed

# # from app.core.config import config
# # from app.logging import get_logger

# # logger = get_logger(__name__)


# # class FinnhubWebSocketClient:
# #     """
# #     Finnhub WebSocket client with auto reconnect.
# #     """

# #     def __init__(self) -> None:
# #         self._connection = None
# #         self._running = False

# #     async def stream(self, symbols: list[str]):
# #         """
# #         Stream live Finnhub market data.

# #         Uses one WebSocket connection for all symbols.
# #         """

# #         if not symbols:
# #             logger.warning(
# #                 "No Finnhub symbols provided"
# #             )
# #             return

# #         url = (
# #             f"{config.FINNHUB_WS_URL}"
# #             f"?token={config.FINNHUB_API_KEY}"
# #         )

# #         self._running = True

# #         logger.info(
# #             "Finnhub stream called",
# #             symbols=symbols,
# #         )

# #         logger.info(
# #             "Finnhub URL",
# #             url=url
# #         )
# #         while self._running:

# #             try:
# #                 logger.info(
# #                     "Connecting to Finnhub WebSocket"
# #                 )

# #                 async with websockets.connect(
# #                     url,
# #                     ping_interval=20,
# #                     ping_timeout=20,
# #                 ) as websocket:

# #                     self._connection = websocket

# #                     logger.info(
# #                         "Connected to Finnhub"
# #                     )

# #                     # Subscribe symbols
# #                     for symbol in symbols:
# #                         await websocket.send(
# #                             json.dumps(
# #                                 {
# #                                     "type": "subscribe",
# #                                     "symbol": symbol,
# #                                 }
# #                             )
# #                         )

# #                     logger.info(
# #                         "Subscribed to Finnhub symbols",
# #                         count=len(symbols),
# #                     )

# #                     async for message in websocket:

# #                         if not self._running:
# #                             break

# #                         payload = json.loads(message)

# #                         # Ignore non trade events
# #                         if payload.get("type") != "trade":
# #                             continue

# #                         for trade in payload.get(
# #                             "data",
# #                             []
# #                         ):

# #                             yield {
# #                                 "symbol": trade["s"],
# #                                 "price": trade["p"],
# #                                 "volume": trade.get(
# #                                     "v",
# #                                     0,
# #                                 ),
# #                                 "timestamp": datetime.fromtimestamp(
# #                                     trade["t"] / 1000,
# #                                     tz=UTC,
# #                                 ),
# #                             }

# #             except ConnectionClosed:
# #                 logger.warning(
# #                     "Finnhub WebSocket disconnected"
# #                 )

# #             except Exception as exc:
# #                 logger.error(
# #                     "Finnhub WebSocket Error",
# #                     error=str(exc),
# #                 )

# #             self._connection = None

# #             if self._running:
# #                 logger.info(
# #                     "Reconnecting to Finnhub in 5 seconds..."
# #                 )

# #                 await asyncio.sleep(5)

# #     async def subscribe(
# #         self,
# #         symbol: str,
# #     ) -> None:
# #         """
# #         Subscribe to additional symbol.
# #         """

# #         if self._connection is None:
# #             logger.warning(
# #                 "Finnhub connection not active"
# #             )
# #             return

# #         await self._connection.send(
# #             json.dumps(
# #                 {
# #                     "type": "subscribe",
# #                     "symbol": symbol,
# #                 }
# #             )
# #         )

# #     async def unsubscribe(
# #         self,
# #         symbol: str,
# #     ) -> None:
# #         """
# #         Unsubscribe symbol.
# #         """

# #         if self._connection is None:
# #             return

# #         await self._connection.send(
# #             json.dumps(
# #                 {
# #                     "type": "unsubscribe",
# #                     "symbol": symbol,
# #                 }
# #             )
# #         )

# #     async def disconnect(self) -> None:
# #         """
# #         Stop WebSocket connection.
# #         """

# #         self._running = False

# #         if self._connection:

# #             await self._connection.close()

# #             logger.info(
# #                 "Finnhub WebSocket closed"
# #             )

# #         self._connection = None


# # finnhub_ws_client = FinnhubWebSocketClient()


# """
# Finnhub WebSocket Client
# """

# from __future__ import annotations

# import asyncio
# import json
# from datetime import UTC, datetime

# import websockets
# from websockets.exceptions import ConnectionClosed

# from app.core.config import config
# from app.logging import get_logger


# logger = get_logger(__name__)


# class FinnhubWebSocketClient:


#     def __init__(self) -> None:
#         self._connection = None
#         self._running = False


#     async def stream(self, symbols: list[str]):

#         if not symbols:
#             return


#         url = (
#             f"{config.FINNHUB_WS_URL}"
#             f"?token={config.FINNHUB_API_KEY}"
#         )


#         self._running = True


#         while self._running:


#             try:

#                 logger.info(
#                     "Connecting to Finnhub WebSocket"
#                 )

#                 async with websockets.connect(
#                     url,
#                     open_timeout=30,
#                     close_timeout=10,
#                     ping_interval=20,
#                     ping_timeout=20,
#                     max_size=2 * 1024 * 1024,
#                 ) as websocket:


#                     self._connection = websocket


#                     logger.info(
#                         "Connected to Finnhub"
#                     )


#                     for symbol in symbols:

#                         await websocket.send(
#                             json.dumps(
#                                 {
#                                     "type":"subscribe",
#                                     "symbol":symbol
#                                 }
#                             )
#                         )


#                     logger.info(
#                         "Subscribed Finnhub symbols",
#                         symbols=symbols
#                     )


#                     async for message in websocket:
#     #                     logger.info(
#     #     "FINNHUB RAW MESSAGE",
#     #     message=message,
#     # )


#                         payload = json.loads(message)


#                         logger.debug(
#                             "Finnhub Payload",
#                             payload=payload
#                         )


#                         if payload.get("type") != "trade":
#                             continue



#                         for trade in payload.get(
#                             "data",
#                             []
#                         ):


#                             symbol = trade.get("s")


#                             price = trade.get("p")


#                             if not symbol or not price:
#                                 continue



#                             tick = {

#                                 "symbol": symbol.upper(),

#                                 "price": price,

#                                 "volume": trade.get(
#                                     "v",
#                                     0
#                                 ),

#                                 "timestamp":
#                                     datetime.fromtimestamp(
#                                         trade["t"]/1000,
#                                         tz=UTC
#                                     )

#                             }


#                             # print(
#                             #     "FINNHUB TICK:",
#                             #     tick
#                             # )


#                             yield tick



#             except ConnectionClosed:

#                 logger.warning(
#                     "Finnhub disconnected"
#                 )


#             except Exception as exc:

#                 logger.error(
#                     "Finnhub error",
#                     error=str(exc)
#                 )



#             self._connection = None


#             if self._running:

#                 await asyncio.sleep(5)



#     async def subscribe(
#         self,
#         symbol:str
#     ):

#         if not self._connection:
#             return


#         await self._connection.send(
#             json.dumps(
#                 {
#                     "type":"subscribe",
#                     "symbol":symbol
#                 }
#             )
#         )



#     async def disconnect(self):

#         self._running=False

#         if self._connection:

#             await self._connection.close()


#         self._connection=None



# finnhub_ws_client = FinnhubWebSocketClient()


# """
# Finnhub WebSocket Client

# Production-ready asynchronous WebSocket client for Finnhub.
# """

# from __future__ import annotations

# import asyncio
# import json

# import websockets
# from websockets.client import WebSocketClientProtocol
# from websockets.exceptions import ConnectionClosed

# from app.core.config import config
# from app.logging import get_logger

# logger = get_logger(__name__)


# class FinnhubWebSocketClient:
#     """
#     Finnhub WebSocket client with auto reconnect.
#     """

#     def __init__(self) -> None:
#         self._connection: WebSocketClientProtocol | None = None
#         self._running = False

        

#     # async def connect(self) -> None:
#     #     """
#     #     Connect to Finnhub WebSocket.
#     #     """

#     #     self._running = True

#     #     url = f"{config.FINNHUB_WS_URL}?token={config.FINNHUB_API_KEY}"

#     #     while self._running:
#     #         try:
#     #             logger.info("Connecting to Finnhub WebSocket")

#     #             async with websockets.connect(
#     #                 url,
#     #                 ping_interval=20,
#     #                 ping_timeout=20,
#     #             ) as websocket:

#     #                 self._connection = websocket

#     #                 logger.info("Connected to Finnhub")

#     #                 await self.listen()

#     #         except ConnectionClosed:

#     #             logger.warning("Finnhub WebSocket disconnected")

#     #         except Exception as exc:

#     #             logger.error(
#     #                 "Finnhub WebSocket Error",
#     #                 error=str(exc),
#     #             )

#     #         logger.info("Reconnecting in 5 seconds...")

#     #         await asyncio.sleep(5)

#     async def subscribe(self, symbol: str) -> None:
#         """
#         Subscribe to a symbol.
#         """

#         if self._connection is None:
#             return

#         await self._connection.send(
#             json.dumps(
#                 {
#                     "type": "subscribe",
#                     "symbol": symbol,
#                 }
#             )
#         )

#     async def unsubscribe(self, symbol: str) -> None:
#         """
#         Unsubscribe from a symbol.
#         """

#         if self._connection is None:
#             return

#         await self._connection.send(
#             json.dumps(
#                 {
#                     "type": "unsubscribe",
#                     "symbol": symbol,
#                 }
#             )
#         )

#     async def listen(self) -> None:
#         """
#         Listen for incoming messages.
#         """

#         assert self._connection is not None

#         async for message in self._connection:

#             payload = json.loads(message)

#             logger.info(
#                 "Finnhub Message",
#                 payload=payload,
#             )

#     async def disconnect(self) -> None:
#         """
#         Close the WebSocket connection.
#         """

#         self._running = False

#         if self._connection:

#             await self._connection.close()

#             logger.info("Finnhub WebSocket closed")

#     async def stream(self, symbols: list[str]):
#         """
#         Async generator yielding normalized ticks for the given symbols.

#         Reconnects automatically on failure.
#         """

#         from datetime import UTC, datetime

#         url = f"{config.FINNHUB_WS_URL}?token={config.FINNHUB_API_KEY}"

#         self._running = True

#         while self._running:

#             try:

#                 logger.info("Connecting to Finnhub WebSocket")

#                 async with websockets.connect(
#                     url,
#                     ping_interval=20,
#                     ping_timeout=20,
#                 ) as websocket:

#                     self._connection = websocket

#                     logger.info("Connected to Finnhub")

#                     for symbol in symbols:
#                         await websocket.send(
#                             json.dumps(
#                                 {
#                                     "type": "subscribe",
#                                     "symbol": symbol,
#                                 }
#                             )
#                         )

#                     async for message in websocket:

#                         if not self._running:
#                             break

#                         payload = json.loads(message)

#                         if payload.get("type") != "trade":
#                             continue

#                         for trade in payload.get("data", []):

#                             yield {
#                                 "symbol": trade["s"],
#                                 "price": trade["p"],
#                                 "volume": trade.get("v", 0),
#                                 "timestamp": datetime.fromtimestamp(
#                                     trade["t"] / 1000,
#                                     tz=UTC,
#                                 ),
#                             }

#             except ConnectionClosed:

#                 logger.warning("Finnhub WebSocket disconnected")

#             except Exception as exc:

#                 logger.error("Finnhub WebSocket Error", error=str(exc))

#             if not self._running:
#                 break

#             logger.info("Reconnecting in 5 seconds...")

#             await asyncio.sleep(5)


# finnhub_ws_client = FinnhubWebSocketClient()


# """
# Finnhub WebSocket Client

# Production-ready asynchronous WebSocket client for Finnhub.
# """

# from __future__ import annotations

# import asyncio
# import json
# from datetime import UTC, datetime
# from datetime import UTC, datetime

# import websockets
# from websockets.exceptions import ConnectionClosed

# from app.core.config import config
# from app.logging import get_logger

# logger = get_logger(__name__)


# class FinnhubWebSocketClient:
#     """
#     Finnhub WebSocket client with auto reconnect.
#     """

#     def __init__(self) -> None:
#         self._connection = None
#         self._running = False

#     async def stream(self, symbols: list[str]):
#         """
#         Stream live Finnhub market data.

#         Uses one WebSocket connection for all symbols.
#         """

#         if not symbols:
#             logger.warning(
#                 "No Finnhub symbols provided"
#             )
#             return

#         url = (
#             f"{config.FINNHUB_WS_URL}"
#             f"?token={config.FINNHUB_API_KEY}"
#         )

#         self._running = True

#         logger.info(
#             "Finnhub stream called",
#             symbols=symbols,
#         )

#         logger.info(
#             "Finnhub URL",
#             url=url
#         )
#         while self._running:

#             try:
#                 logger.info(
#                     "Connecting to Finnhub WebSocket"
#                 )

#                 async with websockets.connect(
#                     url,
#                     ping_interval=20,
#                     ping_timeout=20,
#                 ) as websocket:

#                     self._connection = websocket

#                     logger.info(
#                         "Connected to Finnhub"
#                     )

#                     # Subscribe symbols
#                     for symbol in symbols:
#                         await websocket.send(
#                             json.dumps(
#                                 {
#                                     "type": "subscribe",
#                                     "symbol": symbol,
#                                 }
#                             )
#                         )

#                     logger.info(
#                         "Subscribed to Finnhub symbols",
#                         count=len(symbols),
#                     )

#                     async for message in websocket:

#                         if not self._running:
#                             break

#                         payload = json.loads(message)

#                         # Ignore non trade events
#                         if payload.get("type") != "trade":
#                             continue

#                         for trade in payload.get(
#                             "data",
#                             []
#                         ):

#                             yield {
#                                 "symbol": trade["s"],
#                                 "price": trade["p"],
#                                 "volume": trade.get(
#                                     "v",
#                                     0,
#                                 ),
#                                 "timestamp": datetime.fromtimestamp(
#                                     trade["t"] / 1000,
#                                     tz=UTC,
#                                 ),
#                             }

#             except ConnectionClosed:
#                 logger.warning(
#                     "Finnhub WebSocket disconnected"
#                 )

#             except Exception as exc:
#                 logger.error(
#                     "Finnhub WebSocket Error",
#                     error=str(exc),
#                 )

#             self._connection = None

#             if self._running:
#                 logger.info(
#                     "Reconnecting to Finnhub in 5 seconds..."
#                 )

#                 await asyncio.sleep(5)

#     async def subscribe(
#         self,
#         symbol: str,
#     ) -> None:
#         """
#         Subscribe to additional symbol.
#         """

#         if self._connection is None:
#             logger.warning(
#                 "Finnhub connection not active"
#             )
#             return

#         await self._connection.send(
#             json.dumps(
#                 {
#                     "type": "subscribe",
#                     "symbol": symbol,
#                 }
#             )
#         )

#     async def unsubscribe(
#         self,
#         symbol: str,
#     ) -> None:
#         """
#         Unsubscribe symbol.
#         """

#         if self._connection is None:
#             return

#         await self._connection.send(
#             json.dumps(
#                 {
#                     "type": "unsubscribe",
#                     "symbol": symbol,
#                 }
#             )
#         )

#     async def disconnect(self) -> None:
#         """
#         Stop WebSocket connection.
#         """

#         self._running = False

#         if self._connection:

#             await self._connection.close()

#             logger.info(
#                 "Finnhub WebSocket closed"
#             )

#         self._connection = None


# finnhub_ws_client = FinnhubWebSocketClient()


"""
Finnhub WebSocket Client
"""

from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime

import websockets
from websockets.exceptions import ConnectionClosed

from app.core.config import config
from app.logging import get_logger


logger = get_logger(__name__)


class FinnhubWebSocketClient:


    def __init__(self) -> None:
        self._connection = None
        self._running = False


    async def stream(self, symbols: list[str]):

        if not symbols:
            return


        url = (
            f"{config.FINNHUB_WS_URL}"
            f"?token={config.FINNHUB_API_KEY}"
        )


        self._running = True


        while self._running:


            try:

                logger.info(
                    "Connecting to Finnhub WebSocket"
                )

                async with websockets.connect(
                    url,
                    open_timeout=30,
                    close_timeout=10,
                    ping_interval=20,
                    ping_timeout=20,
                    max_size=2 * 1024 * 1024,
                ) as websocket:


                    self._connection = websocket


                    logger.info(
                        "Connected to Finnhub"
                    )


                    for symbol in symbols:

                        await websocket.send(
                            json.dumps(
                                {
                                    "type":"subscribe",
                                    "symbol":symbol
                                }
                            )
                        )


                    logger.info(
                        "Subscribed Finnhub symbols",
                        symbols=symbols
                    )


                    async for message in websocket:
    #                     logger.info(
    #     "FINNHUB RAW MESSAGE",
    #     message=message,
    # )


                        payload = json.loads(message)


                        # logger.info(
                        #     "Finnhub RAW message",
                        #     type=payload.get("type"),
                        # )


                        if payload.get("type") != "trade":
                            continue



                        for trade in payload.get(
                            "data",
                            []
                        ):


                            symbol = trade.get("s")


                            price = trade.get("p")


                            if not symbol or not price:
                                continue



                            tick = {

                                "symbol": symbol.upper(),

                                "price": price,

                                "volume": trade.get(
                                    "v",
                                    0
                                ),

                                "timestamp":
                                    datetime.fromtimestamp(
                                        trade["t"]/1000,
                                        tz=UTC
                                    )

                            }


                            # print(
                            #     "FINNHUB TICK:",
                            #     tick
                            # )


                            yield tick



            except ConnectionClosed:

                logger.warning(
                    "Finnhub disconnected"
                )


            except Exception as exc:

                logger.error(
                    "Finnhub error",
                    error=str(exc)
                )



            self._connection = None


            if self._running:

                await asyncio.sleep(5)



    async def subscribe(
        self,
        symbol:str
    ):

        if not self._connection:
            return


        await self._connection.send(
            json.dumps(
                {
                    "type":"subscribe",
                    "symbol":symbol
                }
            )
        )



    async def disconnect(self):

        self._running=False

        if self._connection:

            await self._connection.close()


        self._connection=None



finnhub_ws_client = FinnhubWebSocketClient()