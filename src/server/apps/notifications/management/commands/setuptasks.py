from django.conf import settings
from django.core.management import BaseCommand
from django_celery_beat.models import CrontabSchedule, PeriodicTask


class Command(BaseCommand):
    """Команда для создания периодических задач."""

    help = 'Создание периодических задач'

    def handle(self, *args, **options):
        """Создание периодических задач."""
        every_five_min_cron, _ = CrontabSchedule.objects.get_or_create(
            minute='*/5',
            timezone=settings.TIME_ZONE,
        )
        _ = PeriodicTask.objects.update_or_create(
            task='server.apps.notifications.tasks.check_notifications',
            defaults={
                'crontab': every_five_min_cron,
                'name': 'Проверка наличия уведомлений для отправки',
            }
        )
