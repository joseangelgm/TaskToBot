import os
from src.bot.application.shared.redis.redis_service import RedisService

from src.bot.constants import BOT_TOKEN_CACHE_KEY


class SaveTelegramBotToken:
    """
    Save telegram bot token in cache. Telegram bot token has to be
    saved into TELEGRAM_BOT_TOKEN env variable
    """

    def __init__(self) -> None:
        pass

    @classmethod
    def save_telegram_bot_token_from_environment(cls) -> None:
        telegram_bot_token: str = os.getenv('TELEGRAM_BOT_TOKEN')

        if telegram_bot_token is None or not telegram_bot_token:
            raise SaveTelegramBotTokenException(
                f"TELEGRAM_BOT_TOKEN env variable is not defined. Please, set it with your bot token"
            )
        
        RedisService.set_value(key=BOT_TOKEN_CACHE_KEY, value=telegram_bot_token)


class SaveTelegramBotTokenException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)