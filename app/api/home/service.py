# """
# Home API Service
# """

# from __future__ import annotations

# import json

# from app.core.redis import redis_client


# CRYPTO_SYMBOLS = [
#     "BTC-USD",
#     "ETH-USD",
#     "SOL-USD",
#     "BNB-USD",
#     "XRP-USD",
#     "DOGE-USD",
#     "LINK-USD",
# ]

# STOCK_SYMBOLS = [
#     "AAPL",
#     "MSFT",
#     "NVDA",
#     "AMZN",
#     "META",
#     "GOOGL",
#     "TSLA",
# ]

# FOREX_SYMBOLS = [
#     "OANDA:EUR_USD",
#     "OANDA:GBP_USD",
#     "OANDA:USD_JPY",
#     "OANDA:AUD_USD",
#     "OANDA:USD_CHF",
#     "OANDA:USD_CAD",
#     "OANDA:NZD_USD",
# ]


# class HomeService:

#     async def _get_symbol(
#         self,
#         symbol: str,
#         market: str,
#     ):

#         tick = await redis_client.get(
#             f"tick:{symbol}"
#         )

#         if tick is None:
#             return None

#         tick = json.loads(tick)

#         candles = {}

#         for timeframe in (
#             "1m",
#             "5m",
#             "15m",
#             "60m",
#         ):

#             redis_key = (
#                 f"candles:{symbol}:{timeframe}"
#             )

#             data = await redis_client.lrange(
#                 redis_key,
#                 -100,
#                 -1,
#             )

#             candles[timeframe] = [
#                 json.loads(item)
#                 for item in data
#             ]

#         return {
#             "symbol": symbol,
#             "market": market,
#             "price": tick,
#             "candles": candles,
#         }

#     async def _load_market(
#         self,
#         symbols: list[str],
#         market: str,
#     ):

#         items = []

#         for symbol in symbols:

#             result = await self._get_symbol(
#                 symbol,
#                 market,
#             )

#             if result:
#                 items.append(result)

#         return items

#     async def get_home(self):

#         return {
#             "crypto": await self._load_market(
#                 CRYPTO_SYMBOLS,
#                 "crypto",
#             ),
#             "stocks": await self._load_market(
#                 STOCK_SYMBOLS,
#                 "stock",
#             ),
#             "forex": await self._load_market(
#                 FOREX_SYMBOLS,
#                 "forex",
#             ),
#         }

#     async def redis_test(self):

#         return {
#             "btc": await redis_client.get("tick:BTC-USD"),
#             "eth": await redis_client.get("tick:ETH-USD"),
#             "sol": await redis_client.get("tick:SOL-USD"),
#             "bnb": await redis_client.get("tick:BNB-USD"),
#             "aapl": await redis_client.get("tick:AAPL"),
#             "eurusd": await redis_client.get("tick:OANDA:EUR_USD"),
#         }


# home_service = HomeService()

"""
Home API Service
"""

from __future__ import annotations

import json

from app.core.redis import redis_client


CRYPTO_SYMBOLS = [
    "BTC-USD",
    "ETH-USD",
    "SOL-USD",
    "BNB-USD",
    "XRP-USD",
    "DOGE-USD",
    "LINK-USD",
]

STOCK_SYMBOLS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "META",
    "GOOGL",
    "TSLA",
]

FOREX_SYMBOLS = [
    "OANDA:EUR_USD",
    "OANDA:GBP_USD",
    "OANDA:USD_JPY",
    "OANDA:AUD_USD",
    "OANDA:USD_CHF",
    "OANDA:USD_CAD",
    "OANDA:NZD_USD",
]


class HomeService:

    async def _get_symbol(
        self,
        symbol: str,
        market: str,
    ):

        tick = await redis_client.get(
            f"tick:{symbol}"
        )

        if tick is None:
            return None

        tick = json.loads(tick)

        candles = {}

        for timeframe in (
            "1m",
            "5m",
            "15m",
            "60m",
        ):

            redis_key = (
                f"candles:{symbol}:{timeframe}"
            )

            data = await redis_client.lrange(
                redis_key,
                -100,
                -1,
            )

            candles[timeframe] = [
                json.loads(item)
                for item in data
            ]

        return {
            "symbol": symbol,
            "market": market,
            "price": tick,
            "candles": candles,
        }

    async def _load_market(
        self,
        symbols: list[str],
        market: str,
    ):

        items = []

        for symbol in symbols:

            result = await self._get_symbol(
                symbol,
                market,
            )

            if result:
                items.append(result)

        return items

    async def get_home(self):

        return {
            "crypto": await self._load_market(
                CRYPTO_SYMBOLS,
                "crypto",
            ),
            "stocks": await self._load_market(
                STOCK_SYMBOLS,
                "stock",
            ),
            "forex": await self._load_market(
                FOREX_SYMBOLS,
                "forex",
            ),
        }

    async def get_live_snapshot(self):
        """
        Same shape as get_home(); called by tick_processor after
        every processed tick to broadcast a fresh snapshot to
        connected WebSocket clients.
        """

        return await self.get_home()

    async def redis_test(self):

        return {
            "btc": await redis_client.get("tick:BTC-USD"),
            "eth": await redis_client.get("tick:ETH-USD"),
            "sol": await redis_client.get("tick:SOL-USD"),
            "bnb": await redis_client.get("tick:BNB-USD"),
            "aapl": await redis_client.get("tick:AAPL"),
            "eurusd": await redis_client.get("tick:OANDA:EUR_USD"),
        }


home_service = HomeService()