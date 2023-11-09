import logging

from src.bot.application.shared.ngrok_service import NgrokService, NgrokServiceException
from src.bot.application.shared.redis.redis_service import RedisService
from src.bot.application.shared.telegram.admin.telegram_admin_service import TelegramAdminService
from src.bot.application.shared.telegram.admin.webhook_update_request import WebhookUpdateRequest
from src.bot.constants import BOT_SECRET_TOKEN_HEADER_CACHE_KEY, TELEGRAM_BOT_NGROK_TUNNEL_NAME

class UpdateBotWebhook:

    __LOGGER: logging.Logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        pass

    @classmethod
    def update_bot_webhook(cls) -> None:
        """
        Update telegram bot endpoint. Refresh secret-token header

        :raise: UpdateBotWebhookException
        """
        cls.__LOGGER.log(
            level=logging.INFO,
            msg=f"Updating telegram bot webhook"
        )

        telegram_bot_public_url: str = None
        try:
            telegram_bot_public_url: str = NgrokService.get_tunnel_endpoint(TELEGRAM_BOT_NGROK_TUNNEL_NAME)
        except NgrokServiceException as e:
            raise UpdateBotWebhookException(e) from e
        
        secret_token: str = RedisService.get_value(BOT_SECRET_TOKEN_HEADER_CACHE_KEY)
        
        webhook_update_request: WebhookUpdateRequest = WebhookUpdateRequest(
            url=telegram_bot_public_url,
            secret_token=secret_token
        )
        del secret_token
        del telegram_bot_public_url

        TelegramAdminService.update_webhook(webhook_update_request)
        del webhook_update_request


class UpdateBotWebhookException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)