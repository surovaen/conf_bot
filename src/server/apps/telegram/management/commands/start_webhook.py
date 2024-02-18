from django.conf import settings
from django.core.management import BaseCommand
from loguru import logger
import requests
from rest_framework import status


class Command(BaseCommand):
    """Команда для установки вебхука для бота."""

    help = 'Запуск телеграм бота'

    def handle(self, *args, **options):
        delete_webhook_url = 'https://api.telegram.org/bot{token}/deleteWebHook'.format(
            token=settings.BOT_TOKEN,
        )
        set_webhook_url = 'https://api.telegram.org/bot{token}/setWebHook?url={domain}/bot/webhook/'.format(
            token=settings.BOT_TOKEN,
            domain=settings.WEBHOOK_URL,
        )
        try:
            response = requests.get(delete_webhook_url)
            status_code = response.status_code

            if status_code != status.HTTP_200_OK:
                logger.error(
                    'Ошибка удаления вебхука для бота: {exc}\n{trace}'.format(
                        exc=status_code,
                        trace=response.raise_for_status(),
                    ),
                )
                raise Exception

            response = requests.get(set_webhook_url)
            status_code = response.status_code

            if status_code != status.HTTP_200_OK:
                logger.error(
                    'Ошибка установки вебхука для бота: {exc}\n{trace}'.format(
                        exc=status_code,
                        trace=response.raise_for_status(),
                    ),
                )
                raise Exception
        except Exception as exc:
            logger.error('Ошибка запуска бота: {exc}'.format(exc=exc))
