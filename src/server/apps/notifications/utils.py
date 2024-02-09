from datetime import time, timedelta
from typing import List, Optional

from django.conf import settings
from django.utils import timezone

from server.apps.notifications.core.models import BaseThematicNotification


def get_ready_notifications(
        notifications: List[BaseThematicNotification],
        is_before: bool = True,
) -> Optional[List[BaseThematicNotification]]:
    """Функция проверки готовности рассылки 'До события' или 'После события' к отправке."""
    ready_notifications = []

    if not notifications:
        return ready_notifications

    delta = timedelta(days=1)

    with timezone.override("Asia/Vladivostok"):
        date_now = timezone.localtime().date()
        time_now = timezone.localtime().time()

    notification_time = time(hour=settings.NOTIFICATION_TIME)
    for notification in notifications:
        event_date = notification.event.date

        if is_before:
            if date_now < event_date and event_date - date_now <= delta and time_now >= notification_time:
                ready_notifications.append(notification)
        else:
            if date_now > event_date and date_now - event_date >= delta and time_now >= notification_time:
                ready_notifications.append(notification)

    return ready_notifications
