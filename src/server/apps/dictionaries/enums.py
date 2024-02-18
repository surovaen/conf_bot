from django.db import models


class TicketType(models.TextChoices):
    """Перечисление категорий билетов."""

    SILVER = 'SILVER', 'SILVER'
    GOLD = 'GOLD', 'GOLD'
    PLATINUM = 'PLATINUM', 'PLATINUM'
    NONE = 'NONE', 'NONE'
