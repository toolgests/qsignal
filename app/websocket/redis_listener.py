import json

from app.core.redis import redis_client
from app.websocket.manager import connection_manager


async def start_market_listener():

    pubsub = redis_client.pubsub()

    await pubsub.subscribe(
        "market_prices"
    )

    async for message in pubsub.listen():

        if message["type"] != "message":
            continue

        data = json.loads(
            message["data"]
        )

        await connection_manager.broadcast(
            data
        )