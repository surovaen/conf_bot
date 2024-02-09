import abc
from typing import Optional, Tuple

from telebot.types import Message, ReplyKeyboardMarkup

from server.apps.telegram.states.states import QuestionState
from server.apps.telegram.utils.keyboards import KeyboardConstructor


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


class BaseQuestionStrategy(BaseStrategy):
    """Базовый класс стратегии обработки состояния ответов на вопросы предзаписи."""

    _db_manager = None

    async def execute(self) -> Tuple[Optional[str], Optional[ReplyKeyboardMarkup], Optional[dict]]:
        """Метод обработки текущего состояния и получения данных следующего состояния."""
        text = None
        keyboard = KeyboardConstructor().create_menu_keyboard()
        current_data = await self._db_manager.get_one_current_data()
        questions = await self._db_manager.get_questions(current_data)
        next_state = self._get_next_state(len(questions))

        if next_state:
            text = questions[next_state].get('text')

        previous_text = questions[self._state].get('text')
        cache_value = self._message.text
        cache_data = self._get_cache_data(
            next_state,
            previous_text,
            cache_value,
        )

        return text, keyboard, cache_data

    def _get_next_state(self, question_count: int) -> Optional[int]:
        """Метод получения следующего состояния."""
        state = QuestionState(position=self._state)
        state = iter(state)

        try:
            value = next(state)
            if question_count < (value + 1):
                value = None
        except StopIteration:
            value = None

        return value

    def _get_cache_data(
            self,
            state: int,
            question: str,
            answer: str,
    ) -> dict:
        """Метод получения данных для записи в кэш."""
        data = {
            'state': state,
            question: answer,
        }
        return data
