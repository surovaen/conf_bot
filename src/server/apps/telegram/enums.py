from django.db import models


class CallbackTypes(models.TextChoices):
    """Перечисление типов колбеков для модели MenuButton."""

    CONFERENCE = 'conference', 'Конференция'
    COURSE = 'course', 'Курс про деньги'
    BREAKFAST = 'breakfast', 'Коуч-завтрак'
    GAME = 'game', 'Игра'
    PERSONAL_WORK = 'personal_work', 'Хочу в личную работу'
    PODCAST = 'podcast', 'Подкасты'
    GIFT = 'gift', 'Забрать подарок'
