import json
import logging
from logging import INFO, Logger
import uuid

from src.bot.constants import BOT_SECRET_TOKEN_HEADER_CACHE_KEY, BOT_TOKEN_CACHE_KEY, OLD_BOT_SECRET_TOKEN_HEADER_CACHE_KEY, TELEGRAM_BOT_NGROK_TUNNEL_NAME
from src.bot.application.shared.http.http_method import HTTPMethod
from src.bot.application.shared.http.http_request import HTTPRequest
from src.bot.application.shared.http.http_response import HTTPResponse
from src.bot.application.shared.http.http_service import HTTPService, HTTPServiceConnectionRefusedException
from src.bot.application.shared.ngrok_service import NgrokService, NgrokServiceException
from src.bot.application.shared.telegram.admin.webhook_info_response import WebhookInfoResponse
from src.bot.application.shared.telegram.admin.webhook_update_request import WebhookUpdateRequest
from src.bot.application.shared.telegram.telegram_service_commons import TelegramServiceCommons
from src.bot.application.shared.redis.redis_service import RedisService

class TelegramAdminService(TelegramServiceCommons):
    """
    Class that manage admin operations with telegram api
    """

    __LOGGER: Logger = logging.getLogger(__name__)

    # TODO: Raise exception
    def __init__(self) -> None:
        pass
        
    @classmethod
    def update_webhook(cls, webhook_update_request: WebhookUpdateRequest) -> None:
        """
        Update telegram bot endpoint. Refresh secret-token header

        :raise: TelegramAdminServiceException
        """

        telegram_bot_token: str = cls.__recover_telegram_bot_token()

        http_request: HTTPRequest = HTTPRequest(
            url=cls._build_telegram_api_url_for_method(
                telegram_bot_token=telegram_bot_token,
                method="setWebhook",
            ),
            http_method=HTTPMethod.POST,
            body=webhook_update_request.to_telegram_request()
        )

        http_response: HTTPResponse = HTTPService.make_http_request(http_request=http_request)
        
        cls.__LOGGER.log(
            level=INFO,
            msg=http_response
        )

    @classmethod
    def get_current_webhook(cls) -> WebhookInfoResponse:
        """
        Get the current information of webhook set in telegram
        :return: WebhookInfoResponse

        :raise: TelegramAdminServiceException
        """
        http_request: HTTPRequest = HTTPRequest(
            url=cls._build_telegram_api_url_for_method(
                cls.__recover_telegram_bot_token(),
                "getWebhookInfo"
            ),
            http_method=HTTPMethod.GET,
        )

        http_response: HTTPResponse = None
        try:
            http_response: HTTPResponse = HTTPService.make_http_request(http_request=http_request)
        except HTTPServiceConnectionRefusedException as e:
            raise TelegramAdminServiceException(e) from e

        telegram_response: dict = json.loads(http_response.response)
        del http_response

        cls._check_if_telegram_response_is_correct(telegram_response)

        return WebhookInfoResponse.build_from_telegram_response(
            telegram_response=telegram_response['result']
        )

    @classmethod
    def check_if_secret_token_is_correct(cls, secret_token: str) -> bool:
        """
        Check if secret_token given in a telegram request is correct
        """

        secret_token_in_cache: str = RedisService.get_value_as_str(BOT_SECRET_TOKEN_HEADER_CACHE_KEY)
        cls.__LOGGER.log(level=INFO, msg=f"Secret token from cache {secret_token}")
        if secret_token_in_cache is not None and secret_token_in_cache == secret_token:
            return True
        
        old_secret_token_in_cache: str = RedisService.get_value_as_str(OLD_BOT_SECRET_TOKEN_HEADER_CACHE_KEY)
        cls.__LOGGER.log(level=INFO, msg=f"Old secret token from cache {old_secret_token_in_cache}")
        if old_secret_token_in_cache is not None and old_secret_token_in_cache == secret_token:
            return True
        
        return False



    @staticmethod
    def generate_secret_token() -> str:
        """
        Generate a new secret http token for telegram requests
        """
        return str(uuid.uuid4())
    
    @staticmethod
    def __recover_telegram_bot_token() -> str:
        telegram_bot_token: str = RedisService.get_value_as_str(BOT_TOKEN_CACHE_KEY)
        if telegram_bot_token is None:
            raise TelegramAdminServiceException("Telegram bot token is None")
        return telegram_bot_token

class TelegramAdminServiceException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)