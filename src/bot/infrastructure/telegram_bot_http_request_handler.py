from http.server import BaseHTTPRequestHandler
from logging import INFO, Logger
import logging

from src.bot.application.shared.redis.redis_service import RedisService
from src.bot.constants import BOT_SECRET_TOKEN_HEADER


class TelegramBotHttpRequestHandler(BaseHTTPRequestHandler):
    

    __LOGGER: Logger = logging.getLogger(__name__)

    def do_POST(self) -> None:
        secret_token: str = str(self.headers.get("X-Telegram-Bot-Api-Secret-Token"))

        secret_token_in_cache: str = RedisService.get_value_as_str(BOT_SECRET_TOKEN_HEADER)

        if secret_token is None or secret_token != secret_token_in_cache:
            self.__LOGGER.log(
                level=INFO,
                msg=f"Secret token is none or is not equals that secret token saved. Secret token {secret_token}, secret token saved {secret_token_in_cache}"
            )
            self.send_response(200)
            self.end_headers()
        else:
            
            content_length: int = int(self.headers.get("Content-Length"))
            request_content: str = str(self.rfile.read(content_length))

            self.send_response(200)

            """
            self.send_header("Content-Type", "application/json")

            self.wfile.write("Hello World".encode(encoding=DEFAULT_ENCODING))
            """
            self.end_headers()