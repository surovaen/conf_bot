from celery import signature
from django.db.models.signals import post_save
from django.dispatch import receiver

from server.apps.notifications.models import PaymentNotification
from server.apps.payments.enums import PaymentStatuses, ProductTypes
from server.apps.payments.models import Payment
from server.apps.products.models import Breakfast, Conference, Game


PRODUCT_MODEL_MAP = {
    ProductTypes.CONFERENCE: Conference,
    ProductTypes.BREAKFAST: Breakfast,
    ProductTypes.GAME: Game,
}


@receiver(post_save, sender=Payment)
def process_payment_status(sender, instance, update_fields, **kwargs):
    """Обработчик сигнала сохранения объекта с изменением статуса платежа."""
    if update_fields is not None and 'status' in update_fields:
        message = ''

        if instance.status == PaymentStatuses.SUCCESS:
            model = PRODUCT_MODEL_MAP[instance.product]
            product = model.objects.filter(uuid=instance.product_id).first()
            product.users.update_or_create(
                user=instance.user,
                defaults={'is_paid': True},
            )

            payment_notification = PaymentNotification.objects.first()
            message = payment_notification.success_payment

        if instance.status == PaymentStatuses.FAIL:
            payment_notification = PaymentNotification.objects.first()
            message = payment_notification.fail_payment

        signature('send_message').apply_async(args=(instance.user.tg_chat_id, message))
