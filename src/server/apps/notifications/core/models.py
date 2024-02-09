from django.db import models

from server.apps.notifications.enums import MassNotificationType, NotificationTypesEnum


class BaseNotification(models.Model):
    """Абстрактная модель рассылки."""

    description = models.TextField(
        'Текст рассылки',
    )
    type = models.CharField(
        'Тип рассылки',
        max_length=255,
        choices=MassNotificationType.choices,
        default=MassNotificationType.MASS,
    )
    is_sent = models.BooleanField(
        'Отправлена',
        default=False,
    )

    class Meta:
        abstract = True


class BaseThematicNotification(BaseNotification):
    """Абстрактная модель тематической рассылки."""

    type = models.CharField(
        'Тип рассылки',
        max_length=255,
        choices=NotificationTypesEnum.choices,
        default=NotificationTypesEnum.BEFORE_EVENT,
    )

    class Meta:
        abstract = True
