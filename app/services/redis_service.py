# import json

import json

from app.core.redis import redis_client


class RedisService:

    async def save_quote(self, tick: dict):
        await redis_client.set(
            f"tick:{tick['symbol'].upper()}",
            json.dumps(tick, default=str),
        )

    async def get_quote(self, symbol: str):

        key = f"tick:{symbol.upper()}"

        print("Searching Redis Key:", key)

        data = await redis_client.get(key)

        print("Redis Data:", data)

        if not data:
            return None

        return json.loads(data)

    async def get_candles(
        self,
        symbol: str,
        resolution: str,
        from_timestamp: int,
        to_timestamp: int,
    ):
        key = f"candles:{symbol.upper()}:{resolution}"

        data = await redis_client.get(key)

        if not data:
            return []

        candles = json.loads(data)

        return [
            candle
            for candle in candles
            if from_timestamp <= candle["timestamp"] <= to_timestamp
        ]


redis_service = RedisService()