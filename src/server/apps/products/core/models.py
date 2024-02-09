import uuid

from django.db import models


class BaseProductModel(models.Model):
    """Абстрактная модель продукта."""

    uuid = models.UUIDField(
        'UUID',
        primary_key=True,
        default=uuid.uuid4,
    )
    date = models.DateField(
        'Дата проведения события',
        null=True,
    )
    time = models.TimeField(
        'Время проведения события',
        null=True,
        blank=True,
    )
    is_shown = models.BooleanField(
        'Показать в боте',
        default=False,
    )

    class Meta:
        abstract = True
