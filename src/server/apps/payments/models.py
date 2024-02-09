from django.db import models

from server.apps.payments.enums import PaymentStatuses, ProductTypes
from server.apps.telegram.models import BotUser


class Payment(models.Model):
    """Модель платежа."""

    user = models.ForeignKey(
        BotUser,
        on_delete=models.SET_NULL,
        verbose_name='Пользователь',
        related_name='payments',
        null=True,
    )
    product = models.CharField(
        'Продукт',
        max_length=255,
        choices=ProductTypes.choices,
        default=ProductTypes.CONFERENCE,
    )
    product_id = models.CharField(
        'UUID продукта',
        max_length=255,
    )
    price = models.PositiveIntegerField(
        'Цена',
    )
    status = models.CharField(
        'Статус платежа',
        max_length=255,
        choices=PaymentStatuses.choices,
        default=PaymentStatuses.NEW,
    )
    data = models.JSONField(
        'Данные платежа',
        null=True,
    )

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'Платеж № {self.pk}'
