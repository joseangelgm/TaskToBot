import logging

from src.bot.application.shared.telegram.admin.telegram_admin_service import TelegramAdminService
from src.bot.constants import BOT_SECRET_TOKEN_HEADER_CACHE_KEY, OLD_BOT_SECRET_TOKEN_HEADER_CACHE_KEY
from src.bot.application.shared.redis.redis_service import RedisService


class ReloadSecretToken:
    """
    Manage secret token updates given by telegram in each request
    """

    __LOGGER: logging.Logger = logging.getLogger(__name__)


    # TODO: raise exception
    def __init__(self) -> None:
        pass

    @classmethod
    def reload_secret_token(cls) -> None:
        """
        Creates a new token and save the old one as a old token
        """

        secret_token_in_cache: str = RedisService.get_value_as_str(BOT_SECRET_TOKEN_HEADER_CACHE_KEY)
        if secret_token_in_cache is None:
            secret_token_in_cache = TelegramAdminService.generate_secret_token()
            RedisService.set_value(BOT_SECRET_TOKEN_HEADER_CACHE_KEY, secret_token_in_cache)
            cls.__LOGGER.log(level=logging.INFO, msg=f"Secret token created {secret_token_in_cache}")
        else:
            cls.__LOGGER.log(level=logging.INFO, msg=f"Secret token saved as old secret token {secret_token_in_cache}")
            RedisService.set_value(OLD_BOT_SECRET_TOKEN_HEADER_CACHE_KEY, secret_token_in_cache)

            new_secret_token_in_cache: str = TelegramAdminService.generate_secret_token()
            cls.__LOGGER.log(level=logging.INFO, msg=f"New secret token created {new_secret_token_in_cache}")
            RedisService.set_value(BOT_SECRET_TOKEN_HEADER_CACHE_KEY, new_secret_token_in_cache)