import logging

import redis
from redis import Redis

from config.constants import REDIS_HOST, REDIS_PORT, REDIS_MAX_CONNECTIONS, REDIS_CONNECTION_POOL_NAME
from service.static_storage_service import StaticStorageService


class RedisConnector:

    __LOGGER: logging.Logger = logging.getLogger(__name__)

    #TODO: raise exception so this class can not be instantiate
    def __init__(self) -> None:
        pass

    @classmethod
    def initialize(cls) -> None:
        connection_pool:  redis.ConnectionPool = redis.ConnectionPool(
            host=REDIS_HOST,
            port=REDIS_PORT,
            max_connections=REDIS_MAX_CONNECTIONS,
            db=0
        )

        StaticStorageService.set_value(
            REDIS_CONNECTION_POOL_NAME,
            connection_pool
        )

        cls.__LOGGER.log(
            level=logging.INFO,
            msg=f"Redis connection pool created"
        )

    @classmethod
    def get_connection(cls) -> Redis:
        connection_pool: redis.ConnectionPool = StaticStorageService.get_value(
            REDIS_CONNECTION_POOL_NAME,
        )

        return redis.Redis(
            connection_pool=connection_pool
        )

    @classmethod
    def close_connection(cls, redis_connection: Redis) -> None:
        redis_connection.close()

    @classmethod
    def destroy(cls) -> None:
        connection_pool: redis.ConnectionPool = StaticStorageService.get_value(
            REDIS_CONNECTION_POOL_NAME,
        )

        # Close the pool, disconnecting all connections
        connection_pool.close()

