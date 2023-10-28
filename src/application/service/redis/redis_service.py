from typing import Any

from redis import Redis
from config.constants import DEFAULT_ENCODING

from src.application.service.redis.redis_connector import RedisConnector


class RedisService:

    # TODO: Raise exception
    def __init__(self):
        pass

    @classmethod
    def get_value(cls, key: str) -> bytes:
        redis_connection: Redis = RedisConnector.get_connection()
        value: bytes = redis_connection.get(key)
        RedisConnector.close_connection(redis_connection)
        return value
    
    @classmethod
    def get_value_as_str(cls, key: str) -> str:
        redis_connection: Redis = RedisConnector.get_connection()
        value: bytes = redis_connection.get(key)
        RedisConnector.close_connection(redis_connection)
        if not value:
            return None
        return str(value, encoding=DEFAULT_ENCODING)

    @classmethod
    def set_value(cls, key: str, value: Any) -> None:
        redis_connection: Redis = RedisConnector.get_connection()
        redis_connection.set(key, value)
        RedisConnector.close_connection(redis_connection)

