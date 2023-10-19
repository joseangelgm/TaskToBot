import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

from config.constants import DEFAULT_ENCODING
from service.telegram.admin.telegram_admin_service import TelegramAdminService


class WebRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):

        secret_token: str = self.headers.get("X-Telegram-Bot-Api-Secret-Token")

        print(f"Secret token {secret_token}")

        self.send_response(200)

        """
        self.send_header("Content-Type", "application/json")

        self.wfile.write("Hello World".encode(encoding=DEFAULT_ENCODING))
        self.end_headers()
        """


if __name__ == "__main__":

    # Check python version 3.9
    if sys.version_info < (3, 9):
        print("Python version has to be at least 3.9")
        sys.exit(-1)

    telegram_admin_service: TelegramAdminService = TelegramAdminService()
    telegram_admin_service.update_webhook()

    # Config log

    # Init http server
    server = HTTPServer(("localhost", 80), WebRequestHandler)
    server.serve_forever()
