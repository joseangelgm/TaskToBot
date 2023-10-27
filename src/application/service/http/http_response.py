from dataclasses import dataclass, field

from config.constants import EMPTY_STRING


@dataclass(init=True, repr=True)
class HTTPResponse:
    http_code: int
    headers: dict[str, str] = field(default_factory=lambda: {})
    response: str = field(default=EMPTY_STRING)

    def is_bad_http_request(self) -> bool:
        return self.http_code > 299

