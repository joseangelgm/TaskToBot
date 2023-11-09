from http.server import BaseHTTPRequestHandler
from logging import INFO, Logger
import logging
from src.bot.application.shared.telegram.admin.telegram_admin_service import TelegramAdminService

from src.bot.application.shared.redis.redis_service import RedisService
from src.bot.constants import BOT_SECRET_TOKEN_HEADER_CACHE_KEY


class TelegramBotHttpRequestHandler(BaseHTTPRequestHandler):
    

    __LOGGER: Logger = logging.getLogger(__name__)

    def do_POST(self) -> None:
        secret_token: str = str(self.headers.get("X-Telegram-Bot-Api-Secret-Token"))

        if secret_token is not None and TelegramAdminService.check_if_secret_token_is_correct(secret_token):
            self.__LOGGER.log(
                level=INFO,
                msg=f"Secret token {secret_token} is None or doesnt match with secrets saved"
            )
            self.send_response(200)
        else:
            content_length: int = int(self.headers.get("Content-Length"))
            request_content: str = str(self.rfile.read(content_length))

            self.send_response(200)

            """
            self.send_header("Content-Type", "application/json")

            self.wfile.write("Hello World".encode(encoding=DEFAULT_ENCODING))
            """
        self.end_headers()