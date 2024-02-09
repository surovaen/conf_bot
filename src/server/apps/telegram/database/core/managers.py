import abc
from datetime import datetime
from typing import List, Optional

from channels.db import database_sync_to_async

from server.apps.configurations.core.models import BaseConfiguration
from server.apps.products.core.models import BaseProductModel
from server.apps.telegram.models import BotUser


class BaseSingletonDBManager(abc.ABC):
    """Абстрактный класс менеджера соло-объектов."""

    _common_model = None

    @database_sync_to_async
    def get_common_data(self) -> Optional[BaseConfiguration]:
        """Метод получения соло-объекта."""
        data = self._common_model.objects.first()
        return data


class BaseProductDBManager(BaseSingletonDBManager, abc.ABC):
    """Абстрактный класс менеджера конкретных объектов."""

    _model = None

    @database_sync_to_async
    def get_one_current_data(self) -> Optional[BaseProductModel]:
        """Метод получения одного текущего объекта."""
        data = self._model.objects.filter(
            is_shown=True,
            date__gt=datetime.now(),
        ).first()
        return data

    @database_sync_to_async
    def get_all_current_data(self) -> Optional[List[dict]]:
        """Метод получения всех текущих объектов."""
        data = self._model.objects.filter(
            is_shown=True,
            date__gt=datetime.now(),
        ).all().order_by('date').values()
        return list(data)

    @database_sync_to_async
    def get(self, uuid: str) -> Optional[BaseProductModel]:
        """Получение объекта модели по UUID."""
        data = self._model.objects.filter(
            uuid=uuid,
        ).first()
        return data

    @staticmethod
    @database_sync_to_async
    def get_images(obj: BaseConfiguration) -> Optional[List[dict]]:
        """Метод получения списка изображений."""
        data = obj.images.all().values(
            'image',
        )
        return list(data)


class ProductQuestionsDBManager(BaseProductDBManager):
    """Класс менеджера объектов с вопросами предзаписи."""

    _user_model = None

    @staticmethod
    @database_sync_to_async
    def get_questions(obj: BaseProductModel) -> Optional[List[dict]]:
        """Метод получения вопросов предзаписи."""
        questions = obj.questions.all().order_by('id').values()
        return list(questions)

    @database_sync_to_async
    def add_user_and_answers(
            self,
            user_id: int,
            uuid: str,
            answers: dict,
    ) -> None:
        """Метод добавления пользователя и его ответов в участники события."""
        user = BotUser.objects.filter(
            tg_user_id=user_id,
        ).first()
        event = self._model.objects.filter(uuid=uuid).first()
        self._user_model.objects.update_or_create(
            event=event,
            user=user,
            defaults={'answers': answers},
        )


class ProductLimitUserDBManager(BaseProductDBManager):
    """Класс менеджера объектов с ограничением количества участников.."""

    @staticmethod
    @database_sync_to_async
    def get_paid_count(obj: BaseProductModel) -> Optional[int]:
        """Метод получения количества оплативших участников."""
        paid_count = obj.users.filter(
            is_paid=True,
        ).count()
        return paid_count
