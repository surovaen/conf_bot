from channels.db import database_sync_to_async

from server.apps.feedback.models import (
    BreakfastFeedback,
    ConferenceFeedback,
    GameFeedback,
)
from server.apps.telegram.models import BotUser


CLASS_MAP = {
    'conference': ConferenceFeedback,
    'breakfast': BreakfastFeedback,
    'game': GameFeedback,
}


class FeedbackDBManager:
    """Класс-менеджер работы с моделью Feedback."""

    @staticmethod
    @database_sync_to_async
    def add_feedback(
            event,
            event_type: str,
            user: BotUser,
            text: str,
    ) -> None:
        """Метод добавления обратной связи пользователя к событию."""
        CLASS_MAP[event_type].objects.create(
            event=event,
            user=user,
            text=text,
        )
