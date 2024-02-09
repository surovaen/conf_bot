from celery import group, signature

from server import celery_app
from server.apps.notifications.enums import MassNotificationType, NotificationTypesEnum
from server.apps.notifications.models import (
    BreakfastNotification,
    ConferenceNotification,
    GameNotification,
    MassNotification,
)
from server.apps.notifications.utils import get_ready_notifications
from server.apps.products.models import Breakfast, Conference, Game
from server.apps.telegram.handlers.enums import Callback
from server.apps.telegram.models import BotUser
from server.apps.telegram.states.enums import StateType


NOTIFICATIONS_MODELS_LIST = [
    ConferenceNotification,
    BreakfastNotification,
    GameNotification,
]

MASS_NOTIFICATIONS_MODELS_LIST = [
    MassNotification,
]

EVENT_CLASS_MAP = {
    Conference: 'conference',
    Breakfast: 'breakfast',
    Game: 'game',
}


@celery_app.task()
def check_notifications():
    """Задача проверки наличия уведомлений для отправки пользователям."""
    ready_notifications = []

    for model in NOTIFICATIONS_MODELS_LIST:
        not_sent_notifications = model.objects.filter(is_sent=False)

        if not_sent_notifications:
            before_notifications = not_sent_notifications.filter(
                type=NotificationTypesEnum.BEFORE_EVENT,
            )
            ready_before_notifications = get_ready_notifications(
                notifications=before_notifications,
                is_before=True,
            )
            ready_notifications.extend(ready_before_notifications)

            after_notifications = not_sent_notifications.filter(
                type=NotificationTypesEnum.AFTER_EVENT,
            )
            ready_after_notifications = get_ready_notifications(
                notifications=after_notifications,
                is_before=False,
            )
            ready_notifications.extend(ready_after_notifications)

    for model in MASS_NOTIFICATIONS_MODELS_LIST:
        not_sent_notifications = model.objects.filter(is_sent=False, is_send=True)

        if not_sent_notifications:
            ready_notifications.extend(not_sent_notifications)

    if ready_notifications:
        notify(ready_notifications)


def notify(notifications: list) -> None:
    """Функция запуска задач отправки уведомлений пользователям."""
    images = []
    file = None
    buttons = {}
    cache_data = {}

    for notification in notifications:
        message = notification.description

        if notification.type == MassNotificationType.MASS:
            chat_ids = BotUser.objects.all().values_list('tg_chat_id')
            images = list(notification.images.all().values_list('image'))
        else:
            chat_ids = notification.event.users.filter(is_paid=True).values_list('user__tg_chat_id')

        if notification.type == NotificationTypesEnum.BEFORE_EVENT:
            message = message.format(
                date=notification.event.date.strftime('%d.%m.%Y'),
                time=notification.event.time.strftime('%H:%M') if notification.event.time else '',
            )

            if isinstance(notification.event, Breakfast):
                message = message.format(
                    title=notification.event.title,
                )
                uuid = str(notification.event.uuid)
                menu = notification.event.menu.all()

                for position in menu:
                    buttons.update(
                        {
                            position.title: Callback.MENU_BREAKFAST.value.format(uuid=uuid, pk=position.pk),
                        },
                    )
            if isinstance(notification.event, Game):
                file = notification.file.path if notification.file else None

        if notification.type == NotificationTypesEnum.AFTER_EVENT:
            uuid = str(notification.event.uuid)
            event_type = notification.event
            event_type = EVENT_CLASS_MAP[event_type.__class__]

            for user in notification.event.users.all():
                user_id = user.user.tg_user_id
                chat_id = user.user.tg_chat_id
                cache_data.update(
                    {
                        chat_id: {
                            'state_type': StateType.FEEDBACK.value,
                            'tg_user_id': user_id,
                            'uuid': uuid,
                            'event_type': event_type,
                        },
                    },
                )

        group_tasks = group(
            signature(
                'send_message',
                args=(*chat_id, message, images, buttons, file),
                kwargs={
                    'cache_data': cache_data.get(*chat_id),
                }
            ) for chat_id in chat_ids
        )
        group_tasks()

        notification.is_sent = True
        notification.save()
