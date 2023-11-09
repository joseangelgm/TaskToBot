from dataclasses import dataclass, field

from bot.constants import EMPTY_STRING


@dataclass(init=True, repr=True)
class TelegramUser:
    id: int = field(default=None)
    is_bot: bool = field(default=False)
    first_name: str = field(default=EMPTY_STRING)
    last_name: str = field(default=EMPTY_STRING)
    username: str = field(default=EMPTY_STRING)
    language_code: str = field(default=EMPTY_STRING)

    @staticmethod
    def from_json(json: dict) -> 'TelegramUser':
        
        telegram_user: 'TelegramUser' = TelegramUser()

        if 'id' in json:
            telegram_user.id = json['id']    

        if 'is_bot' in json:
            telegram_user.is_bot = json['is_bot']

        if 'first_name' in json:
            telegram_user.first_name = json['first_name']

        if 'last_name' in json:
            telegram_user.last_name = json['last_name']

        if 'username' in json:
            telegram_user.username = json['username']

        if 'language_code' in json:
            telegram_user.language_code = json['language_code']

        return telegram_user
