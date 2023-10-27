import logging
from typing import Any


class StaticStorageService:

    __storage: dict = None
    __LOGGER: logging.Logger = logging.getLogger(__name__)

    # TODO: Raise exception
    def __init__(self) -> None:
        pass

    @classmethod
    def initialize(cls) -> None:
        cls.__LOGGER.log(
            level=logging.INFO,
            msg=f"Initializing StaticStorageService..."
        )
        cls.__storage: dict = dict()

    @classmethod
    def get_value(cls, data_key: str) -> Any:
        return cls.__storage.get(data_key, None)

    @classmethod
    def set_value(cls, data_key: str, data_value: Any) -> None:
        cls.__storage[data_key] = data_value

    @classmethod
    def destroy(cls) -> None:
        del cls.__storage
