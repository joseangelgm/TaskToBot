from dataclasses import dataclass, field

from src.bot.constants import EMPTY_STRING, CONNECT_TIMEOUT, READ_TIMEOUT
from src.bot.application.shared.http.http_method import HTTPMethod


@dataclass(init=True, repr=True)
class HTTPRequest:
    http_method: HTTPMethod = field(default=HTTPMethod.GET)
    url: str = field(default=EMPTY_STRING)
    headers: dict[str, str] = field(default_factory=lambda: {})
    body: dict = field(default_factory=lambda: {})
    connect_timeout: int = field(default=CONNECT_TIMEOUT)
    read_timeout: int = field(default=READ_TIMEOUT)

