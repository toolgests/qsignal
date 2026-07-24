# """
# Forex Service

# Business logic for forex market endpoints, backed by Finnhub.
# """

# from __future__ import annotations
# from datetime import datetime
# import json
# from fastapi import HTTPException
# from app.core.redis import redis_client


# from app.providers.finnhub.parser.parser import finnhub_parser
# from app.providers.finnhub.rest.rest_client import finnhub_rest_client
# from app.services.redis_service import redis_service

# class ForexService:
#     """
#     Service responsible for forex market data.
#     """

#     # async def get_quote(self, symbol: str):

#     #     print("Symbol received:", symbol)
#     #     data = await redis_service.get_quote(symbol)
#     #     # data = await finnhub_rest_client.get_forex_quote(symbol)
#     #     print("Response:", data)
#     #     return finnhub_parser.parse_quote(symbol, data)



#     # async def get_quote(self, symbol: str):

#     #     print("Symbol received:", symbol)

#     #     data = await redis_service.get_quote(symbol)

#     #     print("Response:", data)

#     #     if data is None:
#     #         raise HTTPException(
#     #             status_code=404,
#     #             detail=f"No live data found for {symbol}"
#     #         )

#     #     return finnhub_parser.parse_quote(symbol, data)


#     async def get_quote(self, symbol: str):

#         data = await redis_service.get_quote(symbol)

#         if data is None:
#             raise HTTPException(
#                 status_code=404,
#                 detail=f"{symbol} not found"
#             )

#         return data


#     # async def get_candles(
#     #     self,
#     #     symbol: str,
#     #     resolution: str,
#     #     from_timestamp: int,
#     #     to_timestamp: int,
#     # ):

#     #     key = f"candle:{symbol.upper()}:{resolution}m"

#     #     print("Searching Candle Redis Key:", key)


#     #     data = await redis_client.get(key)


#     #     print("Redis Candle Data:", data)


#     #     if not data:
#     #         return []


#     #     candle = json.loads(data)


#     #     return [
#     #         {
#     #             "symbol": candle["symbol"],
#     #             "resolution": candle["timeframe"],
#     #             "open": candle["open"],
#     #             "high": candle["high"],
#     #             "low": candle["low"],
#     #             "close": candle["close"],
#     #             "volume": candle["volume"],
#     #             "timestamp": int(
#     #                 datetime.fromisoformat(
#     #                     candle["timestamp"].replace("Z", "+00:00")
#     #                 ).timestamp()
#     #             ),
#     #         }
#     #     ]



#     async def get_candles(
#         self,
#         symbol: str,
#         resolution: str,
#         from_timestamp: int,
#         to_timestamp: int,
#     ):

#         key = f"candles:{symbol.upper()}:{resolution}m"

#         print("Searching Candle Redis Key:", key)

#         data = await redis_client.lrange(
#             key,
#             0,
#             -1,
#         )

#         print("Redis Candle Count:", len(data))


#         if not data:
#             return []


#         candles = []

#         for item in data:

#             candle = json.loads(item)

#             timestamp = int(
#                 datetime.fromisoformat(
#                     candle["timestamp"]
#                 ).timestamp()
#             )


#             # timestamp filter
#             if timestamp < from_timestamp:
#                 continue

#             if timestamp > to_timestamp:
#                 continue


#             candles.append(
#                 {
#                     "symbol": candle["symbol"],
#                     "resolution": candle["timeframe"],
#                     "open": candle["open"],
#                     "high": candle["high"],
#                     "low": candle["low"],
#                     "close": candle["close"],
#                     "volume": candle["volume"],
#                     "timestamp": timestamp,
#                 }
#             )

# forex_service = ForexService()




from __future__ import annotations

from datetime import datetime
import json

from fastapi import HTTPException

from app.core.redis import redis_client
from app.services.redis_service import redis_service


class ForexService:

    async def get_quote(self, symbol: str):

        data = await redis_service.get_quote(symbol)

        if data is None:
            raise HTTPException(
                status_code=404,
                detail=f"No live quote found for {symbol}"
            )


        price = data["price"]


        return {
            "symbol": data["symbol"],
            "market": "forex",

            "price": price,
            "current_price": price,

            "change": 0,
            "percent_change": 0,

            "high": price,
            "low": price,
            "open": price,
            "previous_close": price,

            "volume": data.get(
                "volume",
                0
            ),

            "timestamp": data["timestamp"]
        }

    async def get_candles(
        self,
        symbol: str,
        resolution: str,
        from_timestamp: int | None = None,
        to_timestamp: int | None = None,
    ):

        symbol = symbol.upper()

        key = f"candles:{symbol}:{resolution}m"

        print("Searching Candle Redis Key:", key)


        data = await redis_client.lrange(
            key,
            0,
            -1
        )


        print("Redis Candle Count:", len(data))


        if not data:
            return []


        # default range
        if from_timestamp is None:
            from_timestamp = 0


        if to_timestamp is None:
            to_timestamp = int(
                datetime.now().timestamp()
            )


        candles = []


        for item in data:

            candle = json.loads(item)


            candle_time = candle["timestamp"]


            # handle ISO timestamp
            if candle_time.endswith("Z"):
                candle_time = candle_time.replace(
                    "Z",
                    "+00:00"
                )


            ts = int(
                datetime.fromisoformat(
                    candle_time
                ).timestamp()
            )


            print(
        "CANDLE TS:",
        ts,
        "FROM:",
        from_timestamp,
        "TO:",
        to_timestamp
    )


            # filter
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


        # oldest -> newest order
        candles.sort(
            key=lambda x: x["timestamp"]
        )


        return candles


forex_service = ForexService()