from dataclasses import dataclass, field
from typing import List

from config.constants import EMPTY_STRING


@dataclass(init=True, repr=True)
class WebhookInfoResponse:
    url: str = field(default=EMPTY_STRING)
    has_custom_certificate: bool = field(default=False)
    pending_update_count: int = field(default=0)
    ip_address: str = field(default=EMPTY_STRING)
    last_error_date: int = field(default=0)
    last_error_message: str = field(default=EMPTY_STRING)
    last_synchronization_error_date: int = field(default=0)
    max_connections: int = field(default=0)
    allowed_updates: List[str] = field(default_factory=lambda: list())

    @staticmethod
    def build_from_telegram_response(telegram_response: dict) -> 'WebhookInfoResponse':

        webhook_info: WebhookInfoResponse = WebhookInfoResponse()

        webhook_info.url = telegram_response.get('url', EMPTY_STRING)
        webhook_info.has_custom_certificate = telegram_response.get('has_custom_certificate', False)
        webhook_info.pending_update_count = telegram_response.get('pending_update_count', 0)
        webhook_info.ip_address = telegram_response.get('ip_address', EMPTY_STRING)

        # TODO: convert to date. Change data type of attribute
        webhook_info.last_error_date = telegram_response.get('last_error_date', 0)

        webhook_info.last_error_message = telegram_response.get('last_error_message', EMPTY_STRING)

        # TODO: convert to date. Change data type of attribute
        webhook_info.last_synchronization_error_date = telegram_response.get('last_synchronization_error_date', 0)

        webhook_info.max_connections = telegram_response.get('max_connections', 0)

        if 'allowed_updates' in telegram_response.keys():
            for allowed_updates in telegram_response.get('allowed_updates'):
                webhook_info.allowed_updates.append(allowed_updates)

        return webhook_info
