from config.constants import TELEGRAM_API_ENDPOINT


class TelegramServiceCommons:

    def __init__(self) -> None:
        pass

    # TODO: Check use of this method with self in child classes
    @staticmethod
    def _check_if_telegram_response_is_correct(telegram_response: dict) -> None:
        """
        Check if telegram response has ok field and is true
        :param telegram_response:
        :return:
        """
        if ('ok' not in telegram_response
                or 'result' not in telegram_response
                or telegram_response['ok'] is False):
            raise TelegramServiceCommonsException(
                f'ok or result are not in telegram response or is false: {telegram_response}'
            )

    @staticmethod
    def _build_telegram_api_url_for_method(telegram_bot_token: str, method: str) -> str:
        """
        Build the telegram api endpoint for a given method
        :param telegram_bot_token: bot token for telegram api
        :param method: telegram api method
        :return:
        """
        return f"{TELEGRAM_API_ENDPOINT}{telegram_bot_token}/{method}"


class TelegramServiceCommonsException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)
