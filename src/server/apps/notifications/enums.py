from django.db import models


class MassNotificationType(models.TextChoices):
    """Перечисление типов массовых рассылок."""

    MASS = 'MASS', 'Массовая'


class NotificationTypesEnum(models.TextChoices):
    """Перечисление типов рассылок."""

    BEFORE_EVENT = 'BEFORE_EVENT', 'До события'
    AFTER_EVENT = 'AFTER_EVENT', 'После события'
