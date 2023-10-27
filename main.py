import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

from config.constants import HTTP_SERVER_IP, HTTP_SERVER_PORT
from config.set_up_bot import SetUpBot
from service.telegram.admin.telegram_admin_service import TelegramAdminService


class WebRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        secret_token: str = self.headers.get("X-Telegram-Bot-Api-Secret-Token")

        content_length: int = int(self.headers.get("Content-Length"))
        request_content: str = str(self.rfile.read(content_length))

        print(f"Request body: {request_content}\nSecret token {secret_token}")

        self.send_response(200)

        """
        self.send_header("Content-Type", "application/json")

        self.wfile.write("Hello World".encode(encoding=DEFAULT_ENCODING))
        """
        self.end_headers()


if __name__ == "__main__":

    # Check python version 3.9
    if sys.version_info < (3, 9):
        print("Python version has to be at least 3.9")
        sys.exit(-1)

    """
    telegram_admin_service: TelegramAdminService = TelegramAdminService()
    telegram_admin_service.update_webhook()

    # Config log
    """

    SetUpBot.onStart()

    telegram_admin_service: TelegramAdminService = TelegramAdminService()
    telegram_admin_service.update_webhook()

    # Init http server
    server = HTTPServer((HTTP_SERVER_IP, HTTP_SERVER_PORT), WebRequestHandler)
    try:
        server.serve_forever()
    except Exception as e:
        print(e)
    finally:
        server.server_close()
        SetUpBot.onShutdown()
