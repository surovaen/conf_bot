from django.apps import AppConfig


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server.apps.payments'
    verbose_name = 'Платежи'

    def ready(self):
        import server.apps.payments.signals  # noqa F401