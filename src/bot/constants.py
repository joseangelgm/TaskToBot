EMPTY_STRING: str = ''

DEFAULT_ENCODING: str = 'utf-8'

### TELEGRAM BOT
TELEGRAM_API_ENDPOINT: str = "https://api.telegram.org/bot"
BOT_MAX_CONNECTIONS: int = 10
BOT_DROP_PENDING_UPDATES: bool = False

# TELEGRAM CACHE KEYS
BOT_TOKEN_CACHE_KEY: str = "BOT_TOKEN"
BOT_SECRET_TOKEN_HEADER_CACHE_KEY: str = "BOT_SECRET_TOKEN" # This data telegram sends you in each request
OLD_BOT_SECRET_TOKEN_HEADER_CACHE_KEY: str = "OLD_BOT_SECRET_TOKEN"

### Telegram bot http server
HTTP_SERVER_IP: str = "localhost"
HTTP_SERVER_PORT: int = 8080

### HTTP
CONNECT_TIMEOUT: int = 5
READ_TIMEOUT: int = 5

### NGROK
NGROK_IP: str = "127.0.0.1"
NGROK_PORT: int = 5555
NGROK_TUNNELS_API: str = "api/tunnels"
TELEGRAM_BOT_NGROK_TUNNEL_NAME: str = "telegram_bot"

### REDIS
REDIS_HOST: str = "127.0.0.1"
REDIS_PORT: int = 6379
REDIS_MAX_CONNECTIONS: int = 10
REDIS_CONNECTION_POOL_NAME: str = "telegram_bot_pool"
