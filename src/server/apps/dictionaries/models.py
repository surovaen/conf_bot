from django.db import models
from solo.models import SingletonModel


class Menu(models.Model):
    """Модель завтраков."""

    title = models.CharField(
        'Наименование',
        max_length=255,
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Завтрак'
        verbose_name_plural = 'Завтраки'


class BreakfastPrice(models.Model):
    """Модель стоимости коуч-завтраки."""

    title = models.CharField(
        'Тип',
        max_length=255,
    )
    price = models.PositiveIntegerField(
        'Стоимость',
        default=0,
    )

    def __str__(self):
        return f'{self.title} - {self.price}'

    class Meta:
        verbose_name = 'Стоимость коуч-завтрака'
        verbose_name_plural = 'Стоимость коуч-завтраков'


class PreRecordingQuestion(models.Model):
    """Модель вопросов предзаписи."""

    text = models.CharField(
        'Текст вопроса предзаписи',
        max_length=255,
    )

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = 'Вопрос предзаписи'
        verbose_name_plural = 'Вопросы предзаписи'


class UserLimit(SingletonModel):
    """Синглтон-модель настроек лимита участников."""

    breakfast_limit = models.PositiveIntegerField(
        'Лимит участников на коуч-завтрак',
        default=20,
    )
    game_limit = models.PositiveIntegerField(
        'Лимит участников на игру',
        default=4,
    )

    def __str__(self):
        return 'Лимит участников'

    class Meta:
        verbose_name = 'Лимит участников'
        verbose_name_plural = 'Лимит участников'


class PromotionalCode(models.Model):
    """Модель промокода."""

    title = models.CharField(
        'Промокод',
        max_length=255,
    )
    discount = models.PositiveIntegerField(
        'Процент скидки',
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
