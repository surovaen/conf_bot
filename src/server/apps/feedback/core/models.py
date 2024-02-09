from django.db import models

from server.apps.telegram.models import BotUser


class BaseFeedback(models.Model):
    """Абстрактная модель обратной связи."""

    user = models.ForeignKey(
        BotUser,
        on_delete=models.SET_NULL,
        verbose_name='Пользователь',
        null=True,
    )
    text = models.TextField(
        'Обратная связь',
        null=True,
    )

    class Meta:
        abstract = True
