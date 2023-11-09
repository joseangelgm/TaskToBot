from dataclasses import dataclass, field
from bot.constants import EMPTY_STRING

from src.bot.application.shared.telegram.entities.telegram_chat import TelegramChat
from src.bot.application.shared.telegram.entities.telegram_user import TelegramUser

@dataclass(init=True, repr=True)
class TelegramMessage:
    message_id: int = field(default=None)
    message_thread_id: int = field(default=None)
    from_user: TelegramUser = field(default=None)
    date: int = field(default=None)
    chat: TelegramChat = field(default=None)
    text: str = field(default=EMPTY_STRING)

    def from_json(json: dict) -> 'TelegramMessage':
        telegram_message: 'TelegramMessage' = TelegramMessage()

        if 'message_id' in json:
            telegram_message.message_id = json['message_id']

        if 'message_thread_id' in json:
            telegram_message.message_thread_id = json['message_thread_id']

        if 'from' in json:
            telegram_message.from_user = TelegramUser.from_json(json['from'])

        if 'date' in json:
            telegram_message.date = json['date'] # TODO: Transform to date datatype

        if 'chat' in json:
            telegram_message.chat = TelegramChat.from_json(json['chat'])

        if 'text' in json:
            telegram_message.text = json['text']

        return telegram_message