import logging

from src.bot.application.shared.telegram.admin.telegram_admin_service import TelegramAdminService, TelegramAdminServiceException
from src.bot.application.save_telegram_bot_token import SaveTelegramBotToken
from src.bot.application.shared.redis.redis_connector import RedisConnector, RedisConnectorNotRunningException
from src.bot.application.shared.static_storage_service import StaticStorageService


class SetUpBot:
    """
    Class that create all things required to bot start up
    """

    __LOGGER: logging.Logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        raise SetUpBotException("This class cannot be instantiate!!. Only has static methods")

    @classmethod
    def onStart(cls) -> None:
        """
        Configure application on startup

        :raise: SetUpBotException
        """
        
        logging.basicConfig(
            format='[%(asctime)s.%(msecs)03d] - %(levelname)s - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            encoding='utf-8',
            level=logging.DEBUG,
        )

        cls.__LOGGER.log(
            level=logging.INFO,
            msg=f"Starting telegram bot..."
        )

        StaticStorageService.initialize()
        try:
            RedisConnector.initialize()
        except RedisConnectorNotRunningException as e:
            raise SetUpBotException from e

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