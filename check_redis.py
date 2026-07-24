import asyncio

from app.core.redis import redis_client


async def clear():

    keys = await redis_client.keys("*")

    print("Deleting keys:")

    for key in keys:
        print(key)

    if keys:
        await redis_client.delete(*keys)

    print("Redis cleared")


asyncio.run(clear())