# """
# Stocks Service

# Business logic for stock market endpoints, backed by Finnhub.
# """

# from __future__ import annotations

# from app.providers.finnhub.parser.parser import finnhub_parser
# from app.providers.finnhub.rest.rest_client import finnhub_rest_client


# class StockService:
#     """
#     Service responsible for stock market data.
#     """

#     async def get_quote(self, symbol: str):
#         data = await finnhub_rest_client.get_stock_quote(symbol)
#         return finnhub_parser.parse_quote(symbol, data)

#     async def get_candles(
#         self,
#         symbol: str,
#         resolution: str,
#         from_timestamp: int,
#         to_timestamp: int,
#     ):
#         data = await finnhub_rest_client.get_stock_candles(
#             symbol=symbol,
#             resolution=resolution,
#             from_timestamp=from_timestamp,
#             to_timestamp=to_timestamp,
#         )

#         return finnhub_parser.parse_candles(
#             symbol=symbol,
#             resolution=resolution,
#             data=data,
#         )

#     async def get_company_profile(self, symbol: str):
#         data = await finnhub_rest_client.get_company_profile(symbol)
#         return finnhub_parser.parse_company_profile(data)


# stock_service = StockService()



"""
Stocks Service

Business logic for stock market endpoints.
Uses Redis live market data.
"""

from __future__ import annotations

import json
from datetime import datetime

from fastapi import HTTPException

# from app.providers.finnhub.parser.parser import finnhub_parser
from app.providers.finnhub.rest.rest_client import finnhub_rest_client
from app.core.redis import redis_client


class StockService:
    """
    Service responsible for stock market data.
    """


    async def get_quote(
        self,
        symbol: str,
    ):

        symbol = symbol.upper()

        key = f"tick:{symbol}"

        print("Searching Redis Key:", key)


        data = await redis_client.get(key)


        print("Redis Quote Data:", data)


        if not data:

            raise HTTPException(
                status_code=404,
                detail=f"No live quote found for {symbol}"
            )


        quote = json.loads(data)


        price = quote["price"]


        return {
            "symbol": symbol,
            "market": "stocks",
            "price": price,
            "current_price": price,
            "change": 0,
            "percent_change": 0,
            "high": price,
            "low": price,
            "open": price,
            "previous_close": price,
            "volume": quote.get(
                "volume",
                0
            ),
            "timestamp": int(
                datetime.fromisoformat(
                    quote["timestamp"]
                ).timestamp()
            ),
        }



    async def get_candles(
        self,
        symbol: str,
        resolution: str,
        from_timestamp: int,
        to_timestamp: int,
    ):

        symbol = symbol.upper()

        key = (
            f"candles:{symbol}:{resolution}m"
        )


        print(
            "Searching Candle Redis Key:",
            key
        )


        data = await redis_client.lrange(
            key,
            0,
            -1,
        )


        print(
            "Redis Candle Count:",
            len(data)
        )


        if not data:
            return []


        candles = []


        for item in data:

            candle = json.loads(item)


            ts = int(
                datetime.fromisoformat(
                    candle["timestamp"]
                ).timestamp()
            )


            if ts < from_timestamp:
                continue


            if ts > to_timestamp:
                continue


            candles.append(
                {
                    "symbol": candle["symbol"],
                    "resolution": candle["timeframe"],
                    "open": candle["open"],
                    "high": candle["high"],
                    "low": candle["low"],
                    "close": candle["close"],
                    "volume": candle["volume"],
                    "timestamp": ts,
                }
            )


        return candles



    async def get_company_profile(self, symbol: str):

        data = await finnhub_rest_client.get_company_profile(
            symbol
        )

        if not data:
            return {
                "ticker": symbol,
                "name": None,
                "country": None,
                "currency": None,
                "exchange": None,
                "industry": None,
                "ipo": None,
                "logo": None,
                "market_capitalization": None,
                "share_outstanding": None,
                "weburl": None,
            }


        return {
            "ticker": data.get("ticker", symbol),
            "name": data.get("name"),
            "country": data.get("country"),
            "currency": data.get("currency"),
            "exchange": data.get("exchange"),
            "industry": data.get("finnhubIndustry"),
            "ipo": data.get("ipo"),
            "logo": data.get("logo"),
            "market_capitalization": data.get(
                "marketCapitalization"
            ),
            "share_outstanding": data.get(
                "shareOutstanding"
            ),
            "weburl": data.get("weburl"),
        }



stock_service = StockService()