from typing import Optional

from channels.db import database_sync_to_async

from server.apps.telegram.models import BotUser, MenuButton


class UserDBManager:
    """Класс-менеджер работы с моделью BotUser."""

    @staticmethod
    @database_sync_to_async
    def create(**kwargs) -> None:
        """Метод создания или обновления данных пользователя бота."""
        user, _ = BotUser.objects.update_or_create(
            tg_user_id=kwargs['tg_user_id'],
            defaults=kwargs,
        )

    @staticmethod
    @database_sync_to_async
    def get(user_id: int) -> Optional[BotUser]:
        """Метод получения пользователя бота."""
        user = BotUser.objects.filter(
            tg_user_id=str(user_id),
        ).first()
        return user


class MenuButtonDBManager:
    """Класс-менеджер работы с моделью MenuButton."""

    @staticmethod
    @database_sync_to_async
    def get_buttons() -> Optional[dict]:
        """Метод получения текущих кнопок меню."""
        buttons = MenuButton.objects.filter(
            is_shown=True,
        ).order_by(
            'pk',
        ).values(
            'title',
            'callback',
        )
        buttons = {
            button.get('title'): button.get('callback') for button in buttons
        }
        return buttons
