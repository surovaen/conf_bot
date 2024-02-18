from typing import Optional, Tuple

from telebot.types import ReplyKeyboardMarkup

from server.apps.telegram.database.managers import course_db_manager
from server.apps.telegram.states.base_strategy import BaseStrategy
from server.apps.telegram.states.enums import MessageContentTypeEnum
from server.apps.telegram.states.states import QuestionState, UserInfoState
from server.apps.telegram.states.utils import PhoneNumberNotValid, validate_phone_number
from server.apps.telegram.utils import messages
from server.apps.telegram.utils.keyboards import KeyboardConstructor


CACHE_USER_VALUES_MAP = {
    0: 'first_name',
    1: 'last_name',
    2: 'instagram',
    3: 'phone_number',
}


class UserInfoStrategy(BaseStrategy):
    """Класс-стратегия обработки состояний запроса информации о пользователе."""

    async def execute(self) -> Tuple[Optional[str], Optional[ReplyKeyboardMarkup], Optional[dict]]:
        """Метод обработки текущего состояния и получения данных следующего состояния."""
        text = messages.RECORDING_TEXT
        keyboard = KeyboardConstructor().create_menu_keyboard()
        cache_value = None
        next_state = self._get_next_state()

        if next_state:
            text = messages.USER_INFO_MSG_MAP[next_state]
            cache_value = self._message.text

            if next_state == 3:
                keyboard = KeyboardConstructor().create_phone_keyboard()
        else:
            if self._message.content_type == MessageContentTypeEnum.TEXT.value:
                try:
                    cache_value = validate_phone_number(self._message.text)
                except PhoneNumberNotValid:
                    next_state = self._state
                    text = messages.USER_INFO_MSG_MAP[4]
                    keyboard = KeyboardConstructor().create_phone_keyboard()

            if self._message.content_type == MessageContentTypeEnum.CONTACT.value:
                cache_value = self._message.contact.phone_number

        cache_data = self._get_cache_data(
            next_state,
            cache_value,
        )

        return text, keyboard, cache_data

    def _get_next_state(self):
        """Метод получения следующего состояния."""
        user_state = UserInfoState(position=self._state)
        user_state = iter(user_state)

        try:
            value = next(user_state)
        except StopIteration:
            value = None

        return value

    def _get_cache_data(
            self,
            state: int,
            text: str,
    ) -> dict:
        """Метод получения данных для записи в кэш."""
        data = {
            'state': state,
            CACHE_USER_VALUES_MAP[self._state]: text,
        }
        return data


class CourseQuestionsStrategy(BaseStrategy):
    """Класс-стратегия обработки состояний ответов на вопросы предзаписи на курс."""

    _db_manager = course_db_manager

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
