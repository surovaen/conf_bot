from typing import List, Optional

from channels.db import database_sync_to_async

from server.apps.configurations.models import Gift, PersonalWork, Podcast
from server.apps.dictionaries.models import (
    Menu,
    PromotionalCode,
    TicketCategory,
    UserLimit,
)
from server.apps.telegram.database.core.managers import BaseSingletonDBManager
from server.apps.telegram.models import BotUser


class PersonalWorkDBManager(BaseSingletonDBManager):
    """Класс-менеджер работы с моделью PersonalWork."""

    _common_model = PersonalWork

    @staticmethod
    @database_sync_to_async
    def add_user(
            personal_work: PersonalWork,
            user: BotUser,
    ) -> None:
        """Метод добавления пользователя в запросы в личную работу."""
        personal_work.personal_users.add(user)


class PodcastDBManager(BaseSingletonDBManager):
    """Класс-менеджер работы с моделью Podcast."""

    _common_model = Podcast

    @staticmethod
    @database_sync_to_async
    def get_links(podcast: Podcast) -> Optional[List[dict]]:
        """Метод получения списка ссылок на подкасты."""
        data = podcast.links.filter(
            is_shown=True,
        ).values(
            'title',
            'link',
        )
        return list(data)


class GiftDBManager(BaseSingletonDBManager):
    """Класс-менеджер работы с моделью Gift."""

    _common_model = Gift

    @staticmethod
    @database_sync_to_async
    def get_files(gift: Gift) -> Optional[List[dict]]:
        """Метод получения списка файлов."""
        data = gift.files.filter(
            is_shown=True,
        ).values(
            'title',
            'file',
        )
        return list(data)

    @staticmethod
    @database_sync_to_async
    def get_links(gift: Gift) -> Optional[List[dict]]:
        """Метод получения списка ссылок."""
        data = gift.links.filter(
            is_shown=True,
        ).values(
            'title',
            'link',
        )
        return list(data)

    @staticmethod
    @database_sync_to_async
    def get_images(gift: Gift) -> Optional[List[dict]]:
        """Метод получения списка изображений."""
        data = gift.images.filter(
            is_shown=True,
        ).values(
            'title',
            'image',
        )
        return list(data)


class MenuDBManager:
    """Класс-менеджер работы с моделью Menu."""

    @staticmethod
    @database_sync_to_async
    def get(position_id: int) -> Optional[Menu]:
        """Метод получения объекта модели по id."""
        data = Menu.objects.filter(
            pk=position_id,
        ).first()
        return data


class UserLimitDBManager:
    """Класс-менеджер работы с моделью UserLimit."""

    @staticmethod
    @database_sync_to_async
    def get_limit(type_limit: str) -> Optional[int]:
        """Метод получения лимита участников."""
        limit = getattr(UserLimit.get_solo(), type_limit)
        return limit


class PromotionalCodeDBManager:
    """Класс-менеджер работы с моделью PromotionalCode."""

    @staticmethod
    @database_sync_to_async
    def get(promo: str) -> Optional[PromotionalCode]:
        """Метод получения промокода."""
        data = PromotionalCode.objects.filter(title=promo).first()
        return data


class TicketCategoryDBManager:
    """Класс-менеджер работы с моделью TicketCategory."""

    @staticmethod
    @database_sync_to_async
    def get_tickets() -> Optional[List[dict]]:
        """Метод получения билетов."""
        data = TicketCategory.objects.all().order_by('pk').values('type', 'description', 'price')
        return list(data)

    @staticmethod
    @database_sync_to_async
    def get_ticket(ticket_type: str) -> Optional[TicketCategory]:
        """Метод получения категории билетов."""
        data = TicketCategory.objects.filter(type=ticket_type).first()
        return data
