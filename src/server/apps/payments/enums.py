from django.db import models


class ProductTypes(models.TextChoices):
    """Перечисление типов оплаты."""

    CONFERENCE = 'CONFERENCE', 'Конференция'
    BREAKFAST = 'BREAKFAST', 'Коуч-завтрак'
    GAME = 'GAME', 'Игра'


class PaymentStatuses(models.TextChoices):
    """Перечисление статусов платежа."""

    SUCCESS = 'SUCCESS', 'Успех'
    FAIL = 'FAIL', 'Ошибка'
    NEW = 'NEW', 'Новый'
