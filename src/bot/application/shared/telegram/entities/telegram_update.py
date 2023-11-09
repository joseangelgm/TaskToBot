from dataclasses import dataclass, field

from bot.application.shared.telegram.entities.telegram_message import TelegramMessage


@dataclass(init=True, repr=True)
class TelegramUpdate:
    update_id: int = field(default=None)
    message: TelegramMessage = field(default=None)
    edited_message: TelegramMessage = field(default=None)

    def from_json(json: dict) -> 'TelegramUpdate':

        telegram_update: 'TelegramUpdate' = TelegramUpdate()

        if 'update_id' in json:
            telegram_update.update_id = json['update_id']

        if 'message' in json:
            telegram_update.message = TelegramMessage.from_json(json['message'])

        if 'edited_message' in json:
            telegram_update.edited_message = TelegramMessage.from_json(json['edited_message'])

        return telegram_update