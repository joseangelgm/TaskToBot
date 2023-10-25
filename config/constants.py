EMPTY_STRING: str = ''

DEFAULT_ENCODING: str = 'utf-8'

# Telegram bot http server
HTTP_SERVER_IP: str = "localhost"
HTTP_SERVER_PORT: int = 8080

# HTTP
CONNECT_TIMEOUT: int = 5
READ_TIMEOUT: int = 5

# NGROK
NGROK_IP: str = "127.0.0.1"
NGROK_PORT: int = 4040
NGROK_TUNNELS_API: str = "api/tunnels"
TELEGRAM_BOT_NGROK_TUNNEL_NAME: str = "telegram_bot"

# REDIS
REDIS_HOST: str = "127.0.0.1"
REDIS_PORT: int = 6379
REDIS_MAX_CONNECTIONS: int = 10
REDIS_CONNECTION_POOL_NAME: str = "pool"
