import json
import logging
from logging import INFO, Logger
import uuid

from src.bot.constants import BOT_SECRET_TOKEN_HEADER_CACHE_KEY, BOT_TOKEN_CACHE_KEY, TELEGRAM_BOT_NGROK_TUNNEL_NAME
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

    # Raise exception
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

    def get_current_webhook(self) -> WebhookInfoResponse:
        """
        Get the current information of webhook set in telegram
        :return: WebhookInfoResponse

        :raise: TelegramAdminServiceException
        """
        http_request: HTTPRequest = HTTPRequest(
            url=self._build_telegram_api_url_for_method(
                self.__telegram_bot_token,
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

        self._check_if_telegram_response_is_correct(telegram_response)

        return WebhookInfoResponse.build_from_telegram_response(
            telegram_response=telegram_response['result']
        )

    @classmethod
    def generate_secret_token(self) -> str:
        """
        Generate a new secret http token for telegram requests
        """
        return str(uuid.uuid4())
    
    @classmethod
    def __recover_telegram_bot_token(cls) -> str:
        telegram_bot_token: str = RedisService.get_value_as_str(BOT_TOKEN_CACHE_KEY)
        if telegram_bot_token is None:
            raise TelegramAdminServiceException("Telegram bot token is None")
        return telegram_bot_token

class TelegramAdminServiceException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)