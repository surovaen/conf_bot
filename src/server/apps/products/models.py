from django.db import models

from server.apps.dictionaries.models import BreakfastPrice, Menu, PreRecordingQuestion
from server.apps.products.core.models import BaseProductModel
from server.apps.telegram.models import BotUser


class Conference(BaseProductModel):
    """Модель конференций."""

    event_users = models.ManyToManyField(
        BotUser,
        verbose_name='Участники',
        through='ConferenceUser',
    )
    questions = models.ManyToManyField(
        PreRecordingQuestion,
        verbose_name='Вопросы предзаписи',
        blank=True,
    )
    price = models.PositiveIntegerField(
        'Стоимость участия',
    )

    class Meta:
        verbose_name = 'Конференция'
        verbose_name_plural = 'Расписание конференций'

    def __str__(self):
        return f'{self.date}'


class ConferenceUser(models.Model):
    """Промежуточная модель Участники конференции."""

    event = models.ForeignKey(
        Conference,
        verbose_name='Конференция',
        on_delete=models.CASCADE,
        related_name='users',
    )
    user = models.ForeignKey(
        BotUser,
        verbose_name='Участник',
        on_delete=models.CASCADE,
        related_name='conferences',
    )
    answers = models.JSONField(
        'Ответы на вопросы предзаписи',
        blank=True,
        null=True,
    )
    is_paid = models.BooleanField(
        'Оплачено',
        default=False,
    )

    class Meta:
        verbose_name = 'Участник конференции'
        verbose_name_plural = 'Участники конференции'


class Course(BaseProductModel):
    """Модель курсов."""

    event_users = models.ManyToManyField(
        BotUser,
        verbose_name='Участники',
        through='CourseUser',
    )
    questions = models.ManyToManyField(
        PreRecordingQuestion,
        verbose_name='Вопросы предзаписи',
        blank=True,
    )

    class Meta:
        verbose_name = 'Курс про деньги'
        verbose_name_plural = 'Расписание курсов про деньги'

    def __str__(self):
        return f'{self.date}'


class CourseUser(models.Model):
    """Промежуточная модель Участники курса."""

    event = models.ForeignKey(
        Course,
        verbose_name='Курс',
        on_delete=models.CASCADE,
        related_name='users',
    )
    user = models.ForeignKey(
        BotUser,
        verbose_name='Участник',
        on_delete=models.CASCADE,
        related_name='courses',
    )
    answers = models.JSONField(
        'Ответы на вопросы предзаписи',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Участник курса'
        verbose_name_plural = 'Участники курса'


class Breakfast(BaseProductModel):
    """Модель коуч-завтраков."""

    event_users = models.ManyToManyField(
        BotUser,
        verbose_name='Участники',
        through='BreakfastUser',
    )
    menu = models.ManyToManyField(
        Menu,
        verbose_name='Меню',
    )
    price = models.ForeignKey(
        BreakfastPrice,
        verbose_name='Стоимость',
        on_delete=models.SET_NULL,
        null=True,
    )
    title = models.CharField(
        'Тема',
        max_length=255,
    )
    description = models.TextField(
        'Описание',
    )
    place = models.CharField(
        'Место проведения',
        max_length=255,
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Коуч-завтрак'
        verbose_name_plural = 'Расписание коуч-завтраков'
        ordering = ('date',)


class BreakfastUser(models.Model):
    """Промежуточная модель Участники коуч-завтраков."""

    breakfast = models.ForeignKey(
        Breakfast,
        verbose_name='Коуч-завтрак',
        on_delete=models.CASCADE,
        related_name='users',
    )
    user = models.ForeignKey(
        BotUser,
        verbose_name='Участник',
        on_delete=models.CASCADE,
        related_name='breakfasts',
    )
    menu = models.ForeignKey(
        Menu,
        verbose_name='Выбранный завтрак',
        on_delete=models.SET_NULL,
        null=True,
    )
    is_paid = models.BooleanField(
        'Оплачено',
        default=False,
    )

    class Meta:
        verbose_name = 'Участник коуч-завтрака'
        verbose_name_plural = 'Участники коуч-завтрака'


class Game(BaseProductModel):
    """Модель игры."""

    class GameTypes(models.TextChoices):
        """Перечисление типов игр."""
        ONLINE = 'ONLINE', 'Online'
        OFFLINE = 'OFFLINE', 'Offline'

    event_users = models.ManyToManyField(
        BotUser,
        verbose_name='Участники',
        through='GameUser',
    )
    type = models.CharField(
        'Тип игры',
        max_length=255,
        choices=GameTypes.choices,
        default=GameTypes.ONLINE,
    )

    def __str__(self):
        return f'{self.type}'

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Расписание игр'
        ordering = ('date',)


class GameUser(models.Model):
    """Промежуточная модель Участники игры."""

    game = models.ForeignKey(
        Game,
        verbose_name='Игра',
        on_delete=models.CASCADE,
        related_name='users',
    )
    user = models.ForeignKey(
        BotUser,
        verbose_name='Участник',
        on_delete=models.CASCADE,
        related_name='games',
    )
    is_paid = models.BooleanField(
        'Оплачено',
        default=False,
    )

    class Meta:
        verbose_name = 'Участник игры'
        verbose_name_plural = 'Участники игры'
