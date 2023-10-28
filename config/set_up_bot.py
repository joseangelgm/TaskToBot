import logging

from src.application.service.telegram.admin.telegram_admin_service import TelegramAdminService, TelegramAdminServiceException
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
        """
        Configure application on startup

        :raise: SetUpBotException
        """
        
        cls.__LOGGER.log(
            level=logging.INFO,
            msg=f"Starting telegram bot..."
        )

        StaticStorageService.initialize()
        RedisConnector.initialize()

        SaveTelegramBotToken.save_telegram_bot_token_from_environment()

        try:
            telegram_admin_service: TelegramAdminService = TelegramAdminService()
            telegram_admin_service.update_webhook()
        except TelegramAdminServiceException as e:
            raise SetUpBotException from e

    @classmethod
    def onShutdown(cls) -> None:
        try:
            RedisConnector.destroy()
            StaticStorageService.destroy()
        except SetUpBotException as e:
            cls.__LOGGER.log(
                level=logging.ERROR,
                msg=e,
                exc_info=True
            )


class SetUpBotException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)