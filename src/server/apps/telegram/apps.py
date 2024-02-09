from django.apps import AppConfig


class TelegramConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server.apps.telegram'
    verbose_name = 'Настройки бота'
