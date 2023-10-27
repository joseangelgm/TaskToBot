import logging

from src.application.service.telegram.admin.telegram_admin_service import TelegramAdminService
from src.application.save_telegram_bot_token import SaveTelegramBotToken
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

        SaveTelegramBotToken.save_telegram_bot_token_from_environment()

        telegram_admin_service: TelegramAdminService = TelegramAdminService()
        telegram_admin_service.update_webhook()

    @classmethod
    def onShutdown(cls) -> None:
        RedisConnector.destroy()
        StaticStorageService.destroy()