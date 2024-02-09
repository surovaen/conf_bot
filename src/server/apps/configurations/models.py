from django.db import models

from server.apps.configurations.core.models import BaseConfiguration
from server.apps.telegram.models import BotUser


class CommonConference(BaseConfiguration):
    """Синглтон-модель раздела 'Конференция'."""

    class Meta:
        verbose_name = 'Конференция'


class ConferenceImage(models.Model):
    """Модель изображений для конференции."""

    conference = models.ForeignKey(
        CommonConference,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='conference',
    )

    def __str__(self):
        return f'{self.conference}'

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class CommonCourse(BaseConfiguration):
    """Синглтон-модель раздела 'Курс про деньги'."""

    class Meta:
        verbose_name = 'Курс про деньги'


class CourseImage(models.Model):
    """Модель изображений для курса."""

    course = models.ForeignKey(
        CommonCourse,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='course',
    )

    def __str__(self):
        return f'{self.course}'

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class CommonBreakfast(BaseConfiguration):
    """Синглтон-модель общей информации по разделу 'Коуч-завтраки'."""

    def __str__(self):
        return 'Коуч-завтрак'

    class Meta:
        verbose_name = 'Коуч-завтрак'


class BreakfastImage(models.Model):
    """Модель изображений для раздела 'Коуч-завтрак'."""

    breakfast = models.ForeignKey(
        CommonBreakfast,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='breakfast',
    )

    def __str__(self):
        return f'{self.breakfast}'

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class CommonGame(BaseConfiguration):
    """Синглтон-модель общей информации по разделу 'Игры'."""

    price = models.PositiveIntegerField(
        'Цена',
        default=0,
    )

    def __str__(self):
        return 'Игра'

    class Meta:
        verbose_name = 'Игра'


class GameImage(models.Model):
    """Модель изображений для раздела 'Игра'."""

    game = models.ForeignKey(
        CommonGame,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='games',
    )

    def __str__(self):
        return f'{self.game}'

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class PersonalWork(BaseConfiguration):
    """Синглтон-модель раздела 'Хочу в личную работу'."""

    personal_users = models.ManyToManyField(
        BotUser,
        related_name='users',
        verbose_name='Запросы от пользователей',
        through='PersonalWorkUser',
    )
    telegram_link = models.URLField(
        'Ссылка на Telegram ассистента',
    )
    whatsapp_link = models.URLField(
        'Ссылка на Whatsapp ассистента',
    )

    def __str__(self):
        return 'Хочу в личную работу'

    class Meta:
        verbose_name = 'Хочу в личную работу'


class PersonalWorkUser(models.Model):
    """Промежуточная модель запросов пользователей."""

    user = models.ForeignKey(
        BotUser,
        on_delete=models.CASCADE,
        related_name='personal_work',
        verbose_name='Пользователи',
    )
    personal_work = models.ForeignKey(
        PersonalWork,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name='Хочу в личную работу',
    )

    class Meta:
        verbose_name = 'Запрос пользователя'
        verbose_name_plural = 'Запросы пользователей'


class Podcast(BaseConfiguration):
    """Синглтон-модель раздела 'Посмотреть подкаст'."""

    def __str__(self):
        return 'Подкаст'

    class Meta:
        verbose_name = 'Подкасты'


class PodcastLink(models.Model):
    """Модель ссылки на подкаст."""

    podcast = models.ForeignKey(
        Podcast,
        on_delete=models.CASCADE,
        related_name='links',
    )
    title = models.CharField(
        'Наименование',
        max_length=255,
    )
    link = models.URLField(
        'Ссылка',
    )
    is_shown = models.BooleanField(
        'Показать в боте',
        default=True,
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Ссылка на подкаст'
        verbose_name_plural = 'Ссылки на подкасты'


class Gift(BaseConfiguration):
    """Синглтон-модель раздела 'Забрать подарок'."""

    def __str__(self):
        return 'Забрать подарок'

    class Meta:
        verbose_name = 'Забрать подарок'


class GiftFile(models.Model):
    """Модель файла для подарка."""

    gift = models.ForeignKey(
        Gift,
        on_delete=models.CASCADE,
        related_name='files',
    )
    title = models.CharField(
        'Наименование',
        max_length=255,
    )
    file = models.FileField(
        'Файл',
        upload_to='gifts',
    )
    is_shown = models.BooleanField(
        'Показать в боте',
        default=True,
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'


class GiftImage(models.Model):
    """Модель изображения для подарка."""

    gift = models.ForeignKey(
        Gift,
        on_delete=models.CASCADE,
        related_name='images',
    )
    title = models.CharField(
        'Наименование',
        max_length=255,
    )
    image = models.ImageField(
        'Изображение',
        upload_to='gifts',
    )
    is_shown = models.BooleanField(
        'Показать в боте',
        default=True,
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class GiftLink(models.Model):
    """Модель ссылки для подарка."""

    gift = models.ForeignKey(
        Gift,
        on_delete=models.CASCADE,
        related_name='links',
    )
    title = models.CharField(
        'Наименование',
        max_length=255,
    )
    link = models.URLField(
        'Ссылка',
    )
    is_shown = models.BooleanField(
        'Показать в боте',
        default=True,
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'
