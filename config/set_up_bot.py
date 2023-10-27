import logging

from src.application.service.redis.redis_connector import RedisConnector
from src.application.service.static_storage_service import StaticStorageService


class SetUpBot:

    __LOGGER: logging.Logger = logging.getLogger(__name__)

    # TODO: Raise exception
    def __init__(self) -> None:
        pass

    @classmethod
    def onStart(cls) -> None:
        cls.__LOGGER.log(
            level=logging.INFO,
            msg=f"Configuring environment..."
        )

        StaticStorageService.initialize()
        RedisConnector.initialize()

    @classmethod
    def onShutdown(cls) -> None:
        RedisConnector.destroy()
        StaticStorageService.destroy()