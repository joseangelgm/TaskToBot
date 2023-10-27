from typing import Any

from redis import Redis

from src.application.service.redis.redis_connector import RedisConnector


class RedisService:

    # TODO: Raise exception
    def __init__(self):
        pass

    @classmethod
    def get_value(cls, key: str) -> Any:
        redis_connection: Redis = RedisConnector.get_connection()
        value: Any = redis_connection.get(key)
        RedisConnector.close_connection(redis_connection)
        return value

    @classmethod
    def set_value(cls, key: str, value: Any) -> None:
        redis_connection: Redis = RedisConnector.get_connection()
        redis_connection.set(key, value)
        RedisConnector.close_connection(redis_connection)

