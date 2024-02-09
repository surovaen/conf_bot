from collections.abc import Iterable, Iterator
from typing import List

from server import settings


class StateIterator(Iterator):
    """Класс-итератор состояний."""

    def __init__(self, collection, position: int) -> None:
        self._collection = collection
        self._position = position + 1

    def __next__(self):
        """Переопределение метода next() с учетом текущей позиции."""
        try:
            value = self._collection[self._position]
        except IndexError:
            raise StopIteration()

        return value


class BaseState(Iterable):
    """Базовый класс состояний."""

    _collection: List[int] = []

    def __init__(self, position: int) -> None:
        self._position = position

    def __iter__(self) -> StateIterator:
        """Переопределение метода iter() с кастомным итератором."""
        return StateIterator(self._collection, self._position)


class UserInfoState(BaseState):
    """Класс состояний запроса информации о пользователе."""

    _collection = [0, 1, 2]


class QuestionState(BaseState):
    """Класс состояний ответов на вопросы предзаписи."""

    _collection = list(range(settings.QUESTIONS_MAX_COUNT))
