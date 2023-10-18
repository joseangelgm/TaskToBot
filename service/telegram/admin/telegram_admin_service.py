import json
import logging
from logging import Logger

from service.http.http_method import HTTPMethod
from service.http.http_request import HTTPRequest
from service.http.http_response import HTTPResponse
from service.http.http_service import HTTPService
from service.telegram.admin.webhook_info_response import WebhookInfoResponse
from service.telegram.admin.webhook_update_request import WebhookUpdateRequest
from service.telegram.telegram_service_commons import TelegramServiceCommons


class TelegramAdminService(TelegramServiceCommons):
    __LOGGER: Logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        super().__init__()
        self.__telegram_bot_token: str = ""  # TODO: recover token from cache

    def update_webhook(self) -> None:
        # TODO: recover actual endpoint

        webhook_update_request: WebhookUpdateRequest = WebhookUpdateRequest(
            url="https://testurl.com"
        )

        http_request: HTTPRequest = HTTPRequest(
            url=self._build_telegram_api_url_for_method(
                telegram_bot_token=self.__telegram_bot_token,
                method="setWebhook",
            ),
            http_method=HTTPMethod.POST,
            body=webhook_update_request.to_telegram_request()
        )

        HTTPService.make_http_request(http_request=http_request)

    def get_current_webhook(self) -> WebhookInfoResponse:
        """
        Get the current information of webhook set in telegram
        :return:
        """
        http_request: HTTPRequest = HTTPRequest(
            url=self._build_telegram_api_url_for_method(
                self.__telegram_bot_token,
                "getWebhookInfo"
            ),
            http_method=HTTPMethod.GET,
        )

        http_response: HTTPResponse = HTTPService.make_http_request(http_request=http_request)

        telegram_response: dict = json.loads(http_response.response)
        self._check_if_telegram_response_is_correct(telegram_response)

        return WebhookInfoResponse.build_from_telegram_response(
            telegram_response=telegram_response['result']
        )
