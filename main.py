#!/usr/bin/env python3.9

import sys
from http.server import HTTPServer

from config.constants import HTTP_SERVER_IP, HTTP_SERVER_PORT
from config.set_up_bot import SetUpBot
from src.infraestructure.telegram_bot_http_request_handler import TelegramBotHttpRequestHandler


if __name__ == "__main__":

    # Check python version 3.9
    if sys.version_info < (3, 9):
        print("Python version has to be at least 3.9")
        sys.exit(-1)

    # Config log


    SetUpBot.onStart()

    # Init http server
    server = HTTPServer(
        (HTTP_SERVER_IP, HTTP_SERVER_PORT),
        TelegramBotHttpRequestHandler
    )
    try:
        server.serve_forever()
    except Exception as e:
        print(e)
    finally:
        server.server_close()
        SetUpBot.onShutdown()
