import redis
from app.config import REDIS_TOKEN_DB

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=REDIS_TOKEN_DB,
    decode_responses=True
)