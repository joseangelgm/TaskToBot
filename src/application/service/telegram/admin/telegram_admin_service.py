import json
import logging
from logging import INFO, Logger
import uuid

from config.constants import BOT_SECRET_TOKEN_HEADER, BOT_TOKEN_CACHE_KEY, TELEGRAM_BOT_NGROK_TUNNEL_NAME
from src.application.service.http.http_method import HTTPMethod
from src.application.service.http.http_request import HTTPRequest
from src.application.service.http.http_response import HTTPResponse
from src.application.service.http.http_service import HTTPService, HTTPServiceConnectionRefusedException
from src.application.service.ngrok_service import NgrokService, NgrokServiceException
from src.application.service.telegram.admin.response.webhook_info_response import WebhookInfoResponse
from src.application.service.telegram.admin.request.webhook_update_request import WebhookUpdateRequest
from src.application.service.telegram.telegram_service_commons import TelegramServiceCommons
from src.application.service.redis.redis_service import RedisService

class TelegramAdminService(TelegramServiceCommons):
    """
    Class that manage admin operations with telegram api
    """

    __LOGGER: Logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        super().__init__()
        telegram_bot_token: str = RedisService.get_value_as_str(BOT_TOKEN_CACHE_KEY)
        if telegram_bot_token is None:
            raise TelegramAdminServiceException("Telegram bot token is None")
        self.__telegram_bot_token: str = telegram_bot_token

    def update_webhook(self) -> None:
        """
        Update telegram bot endpoint. Refresh secret-token header

        :raise: TelegramAdminServiceException
        """

        self.__LOGGER.log(
            level=INFO,
            msg=f"Updating telegram bot webhook"
        )

        telegram_bot_public_url: str = None
        try:
            telegram_bot_public_url: str = NgrokService.get_tunnel_endpoint(TELEGRAM_BOT_NGROK_TUNNEL_NAME)
        except NgrokServiceException as e:
            raise TelegramAdminServiceException(e) from e
        
        secret_token: str = self.__generate_secret_token()

        webhook_update_request: WebhookUpdateRequest = WebhookUpdateRequest(
            url=telegram_bot_public_url,
            secret_token=secret_token
        )

        del telegram_bot_public_url

        http_request: HTTPRequest = HTTPRequest(
            url=self._build_telegram_api_url_for_method(
                telegram_bot_token=self.__telegram_bot_token,
                method="setWebhook",
            ),
            http_method=HTTPMethod.POST,
            body=webhook_update_request.to_telegram_request()
        )

        del webhook_update_request

        http_response: HTTPResponse = HTTPService.make_http_request(http_request=http_request)
        
        self.__LOGGER.log(
            level=INFO,
            msg=http_response
        )

        RedisService.set_value(BOT_SECRET_TOKEN_HEADER, secret_token)
        del secret_token

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

    def __generate_secret_token(self) -> str:
        """
        Generate a new secret http token for telegram requests
        """
        return str(uuid.uuid4())

class TelegramAdminServiceException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)