from http.server import BaseHTTPRequestHandler


class TelegramBotHttpRequestHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        secret_token: str = str(self.headers.get("X-Telegram-Bot-Api-Secret-Token"))

        content_length: int = int(self.headers.get("Content-Length"))
        request_content: str = str(self.rfile.read(content_length))

        print(f"Request body: {request_content}\nSecret token {secret_token}")

        self.send_response(200)

        """
        self.send_header("Content-Type", "application/json")

        self.wfile.write("Hello World".encode(encoding=DEFAULT_ENCODING))
        """
        self.end_headers()