import os
import redis
from dotenv import load_dotenv

load_dotenv()

print("HOST:", repr(os.getenv("REDIS_HOST")))
print("PORT:", repr(os.getenv("REDIS_PORT")))
print("USERNAME:", repr(os.getenv("REDIS_USERNAME")))
print("PASSWORD EXISTS:", bool(os.getenv("REDIS_PASSWORD")))
print("PASSWORD LENGTH:", len(os.getenv("REDIS_PASSWORD") or ""))

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    username=os.getenv("REDIS_USERNAME"),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
)

print("PING:", redis_client.ping())