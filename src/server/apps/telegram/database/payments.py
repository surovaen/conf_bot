from channels.db import database_sync_to_async

from server.apps.payments.models import Payment


class PaymentDBManager:
    """Класс-менеджер работы с моделью Payment."""

    @staticmethod
    @database_sync_to_async
    def create(data: dict) -> int:
        """Метод создания объекта платежа."""
        payment = Payment.objects.create(**data)
        return payment.pk
