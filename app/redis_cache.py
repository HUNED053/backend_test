import redis
import json
from app import config


redis_client = redis.Redis.from_url(config.REDIS_URL, decode_responses=True)

def set_cache(key: str, value, expire_seconds: int = 30):
    """Save value in Redis with expiry"""
    redis_client.setex(key, expire_seconds, json.dumps(value, default=str))

def get_cache(key: str):
    """Get value from Redis by key"""
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def delete_cache(key: str):
    """Delete key from Redis"""
    redis_client.delete(key)
