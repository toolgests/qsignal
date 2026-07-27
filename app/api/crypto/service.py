# """
# Crypto Service

# Business logic for crypto market endpoints, backed by Binance.
# """

# from __future__ import annotations

# from app.providers.binance.parser.parser import binance_parser
# from app.providers.binance.rest.rest_client import binance_rest_client
# from app.services.redis_service import redis_service

# class CryptoService:
#     """
#     Service responsible for crypto market data.
#     """

#     async def get_price(self, symbol: str):
#         data = await redis_service.get_quote(symbol)

#         if data is None:
#             return {
#                 "success": False,
#                 "message": f"No live data found for {symbol}"
#             }

#         return data

#     async def get_ticker(self, symbol: str):
#         data = await binance_rest_client.get_24hr_ticker(symbol)
#         return binance_parser.parse_24hr_ticker(data)

#     async def get_candles(
#         self,
#         symbol: str,
#         interval: str = "1m",
#         limit: int = 500,
#     ):
#         data = await binance_rest_client.get_klines(
#             symbol=symbol,
#             interval=interval,
#             limit=limit,
#         )

#         return [
#             binance_parser.parse_kline(
#                 symbol=symbol,
#                 interval=interval,
#                 data=item,
#             )
#             for item in data
#         ]


# crypto_service = CryptoService()


"""
Crypto Service

Business logic for crypto market endpoints.
"""

from __future__ import annotations
from datetime import datetime

from app.services.redis_service import redis_service


class CryptoService:
    """
    Service responsible for crypto market data.
    """

    async def get_price(self, symbol: str):

        data = await redis_service.get_quote(symbol)

        if data is None:
            return {
                "success": False,
                "message": f"No live data found for {symbol}"
            }

        return data

    async def get_ticker(self, symbol: str):

        tick = await redis_service.get_quote(symbol)

        if tick is None:
            return None

        return {
            "symbol": tick["symbol"],
            "last_price": tick["price"],
            "price_change": 0,
            "price_change_percent": 0,
            "high_price": tick["price"],
            "low_price": tick["price"],
            "open_price": tick["price"],
            "volume": tick["volume"], 
        }


# from datetime import datetime

# from datetime import datetime

    async def get_candles(
        self,
        symbol: str,
        interval: str = "1m",
        limit: int = 500,
    ):

        candles = await redis_service.get_candles(
            symbol=symbol,
            timeframe=interval,
            limit=limit,
        )

        result = []

        for candle in candles:

            dt = datetime.fromisoformat(candle["timestamp"])
            ms = int(dt.timestamp() * 1000)

            result.append({
                "symbol": candle["symbol"],
                "interval": candle["timeframe"],
                "open_time": ms,
                "open": candle["open"],
                "high": candle["high"],
                "low": candle["low"],
                "close": candle["close"],
                "volume": candle["volume"],
                "close_time": ms,
                "closed": True,
            })

        return result


crypto_service = CryptoService()
