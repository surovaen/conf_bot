from django.db import models

from server.apps.feedback.core.models import BaseFeedback
from server.apps.products.models import Breakfast, Conference, Game


class ConferenceFeedback(BaseFeedback):
    """Модель обратной связи по конференции."""

    event = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
        related_name='conferences',
        verbose_name='Конференция',
    )

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return 'Обратная связь'


class BreakfastFeedback(BaseFeedback):
    """Модель обратной связи по коуч-завтраку."""

    event = models.ForeignKey(
        Breakfast,
        on_delete=models.CASCADE,
        related_name='breakfasts',
        verbose_name='Коуч-завтрак',
    )

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return 'Обратная связь'


class GameFeedback(BaseFeedback):
    """Модель обратной связи по игре."""

    event = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='games',
        verbose_name='Игра',
    )

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return 'Обратная связь'
