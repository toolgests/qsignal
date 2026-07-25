# import redis.asyncio as redis

# redis_client = redis.Redis(
#     host="localhost",
#     port=6379,
#     decode_responses=True,
# )

import os
import redis.asyncio as redis

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
)