from django.db import models
from solo.models import SingletonModel


class BaseConfiguration(SingletonModel):
    """Абстрактная модель общих настроек разделов бота."""

    text = models.TextField(
        'Описание',
    )

    class Meta:
        abstract = True
