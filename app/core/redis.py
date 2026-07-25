# import os
# import redis.asyncio as redis
# from dotenv import load_dotenv

# load_dotenv()

# redis_client = redis.Redis(
#     host=os.getenv("REDIS_HOST", "localhost"),
#     port=int(os.getenv("REDIS_PORT", "6379")),
#     password=os.getenv("REDIS_PASSWORD"),
#     ssl=os.getenv("REDIS_TLS", "False").lower() == "true",
#     decode_responses=True,
# )

# print("HOST =", os.getenv("REDIS_HOST"))
# print("PORT =", os.getenv("REDIS_PORT"))
# print("TLS =", os.getenv("REDIS_TLS"))
# print("PASSWORD =", bool(os.getenv("REDIS_PASSWORD")))

import os
import redis.asyncio as redis

redis_client = redis.from_url(
    os.getenv("REDIS_MASTER_URL"),
    decode_responses=True,
)