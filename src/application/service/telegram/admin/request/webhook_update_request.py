from dataclasses import dataclass, field
from typing import List

from config.constants import BOT_DROP_PENDING_UPDATES, BOT_MAX_CONNECTIONS, EMPTY_STRING


@dataclass(init=True, repr=True)
class WebhookUpdateRequest:
    url: str = field(default=EMPTY_STRING)
    # certificate: InputFile ...
    # ip_address: str = field(default=EMPTY_STRING)
    max_connections: int = field(default=BOT_MAX_CONNECTIONS)
    allowed_updates: List[str] = field(default_factory=lambda: list())
    drop_pending_updates: bool = field(default=BOT_DROP_PENDING_UPDATES)
    secret_token: str = field(default=EMPTY_STRING)

    def to_telegram_request(self) -> dict:
        """
        Transform the instance into a telegram request structure (dict)
        :return:
        """
        telegram_request: dict = {
            'url': self.url,
            'max_connections': self.max_connections,
            'allowed_updates': self.allowed_updates,
            'drop_pending_updates': self.drop_pending_updates,
            'secret_token': self.secret_token
        }

        return telegram_request
