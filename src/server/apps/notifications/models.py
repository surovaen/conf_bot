from django.db import models
from solo.models import SingletonModel

from server.apps.notifications.core.models import (
    BaseNotification,
    BaseThematicNotification,
)
from server.apps.products.models import Breakfast, Conference, Game


class MassNotification(BaseNotification):
    """Модель массовой рассылки."""

    is_send = models.BooleanField(
        'Отправить?',
        default=False,
    )

    class Meta:
        verbose_name = 'Массовая рассылка'
        verbose_name_plural = 'Массовые рассылки'

    def __str__(self):
        return f'Массовая рассылка № {self.pk}'


class MassNotificationImage(models.Model):
    """Модель изображений для массовой рассылки."""

    notification = models.ForeignKey(
        MassNotification,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Рассылка',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='notifications',
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class ConferenceNotification(BaseThematicNotification):
    """Модель рассылки по конференции."""

    event = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
        verbose_name='Конференция',
        related_name='notifications',
    )

    class Meta:
        verbose_name = 'Рассылка по конференции'
        verbose_name_plural = 'Рассылки по конференции'

    def __str__(self):
        return 'Рассылка'


class BreakfastNotification(BaseThematicNotification):
    """Модель рассылки по коуч-завтракам."""

    event = models.ForeignKey(
        Breakfast,
        on_delete=models.CASCADE,
        verbose_name='Завтрак',
        related_name='notifications',
    )

    class Meta:
        verbose_name = 'Рассылка по коуч-завтраку'
        verbose_name_plural = 'Рассылки по коуч-завтраку'

    def __str__(self):
        return 'Рассылка'


class GameNotification(BaseThematicNotification):
    """Модель рассылки по игре."""

    event = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        verbose_name='Игра',
        related_name='notifications',
    )
    file = models.FileField(
        'Файл',
        upload_to='notifications',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Рассылка по игре'
        verbose_name_plural = 'Рассылки по игре'

    def __str__(self):
        return 'Рассылка'


class PaymentNotification(SingletonModel):
    """Синглтон-модель сообщений об оплате."""

    success_payment = models.TextField(
        'Сообщение об успешной оплате',
        default='Оплата прошла успешно! Мы свяжемся с Вами накануне события.'
    )
    fail_payment = models.TextField(
        'Сообщение о неуспешной оплате',
        default='К сожалению, оплата не прошла.'
    )

    def __str__(self):
        return 'Сообщения об оплате'

    class Meta:
        verbose_name = 'Сообщение об оплате'
        verbose_name_plural = 'Сообщения об оплате'
