from dataclasses import dataclass, field


@dataclass(init=True, repr=True)
class TelegramChat:
    id: str = field(default=None)
    chat_type: str = field(default=None) # TODO: is a enum -> https://core.telegram.org/bots/api#chat
    username: str = field(default=None)
    first_name: str = field(default=None)
    last_name: str = field(default=None)

    def from_json(json: dict) -> 'TelegramChat':
        telegram_chat: 'TelegramChat' = TelegramChat()

        if 'id' in json:
            telegram_chat.id = json['id']

        if 'type' in json:
            telegram_chat.chat_type = json['type'] # TODO: is a enum -> https://core.telegram.org/bots/api#chat

        if 'title' in json:
            telegram_chat.title = json['title']

        if 'username' in json:
            telegram_chat.username = json['username']

        if 'first_name' in json:
            telegram_chat.first_name = json['first_name']

        if 'last_name' in json:
            telegram_chat.last_name = json['last_name']

        return telegram_chat