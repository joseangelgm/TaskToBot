import logging
from http.server import BaseHTTPRequestHandler

from src.bot.application.command_executor import CommandExecutor
from src.bot.application.shared.telegram.admin.telegram_admin_service import TelegramAdminService


class TelegramBotHttpRequestHandler(BaseHTTPRequestHandler):
    

    __LOGGER: logging.Logger = logging.getLogger(__name__)


    def do_POST(self) -> None:
        secret_token: str = str(self.headers.get("X-Telegram-Bot-Api-Secret-Token"))

        if secret_token is not None and TelegramAdminService.check_if_secret_token_is_correct(secret_token):
            self.__LOGGER.log(
                level=logging.INFO,
                msg=f"Secret token {secret_token} is None or doesnt match with secrets saved"
            )
            self.send_response(200)
        else:
            content_length: int = int(self.headers.get("Content-Length"))
            request_content: str = str(self.rfile.read(content_length))

            CommandExecutor.process_message_and_execute_command(request_content)

            self.send_header("Content-Type", "text/plain")
            self.send_response(200)
            
        self.end_headers()