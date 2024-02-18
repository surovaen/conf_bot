import abc
from typing import Optional, Tuple

from telebot.types import Message, ReplyKeyboardMarkup


class BaseStrategy(abc.ABC):
    """Абстрактный класс стратегии обработки состояний."""

    def __init__(self, state: int, message: Message):
        self._state = state
        self._message = message

    @abc.abstractmethod
    async def execute(self) -> Tuple[Optional[str], Optional[ReplyKeyboardMarkup], Optional[dict]]:
        """Метод обработки текущего состояния и получения данных следующего состояния."""

    @abc.abstractmethod
    def _get_next_state(self, *args, **kwargs) -> Optional[int]:
        """Метод получения следующего состояния."""

    @abc.abstractmethod
    def _get_cache_data(self, *args, **kwargs) -> dict:
        """Метод получения данных для записи в кэш."""
