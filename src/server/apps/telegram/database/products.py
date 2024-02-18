from typing import Optional

from channels.db import database_sync_to_async

from server.apps.configurations.models import (
    CommonBreakfast,
    CommonConference,
    CommonCourse,
    CommonGame,
)
from server.apps.dictionaries.models import Menu
from server.apps.products.models import (
    Breakfast,
    BreakfastUser,
    Conference,
    Course,
    CourseUser,
    Game,
)
from server.apps.telegram.database.core.managers import (
    BaseProductDBManager,
    ProductLimitUserDBManager,
    ProductQuestionsDBManager,
)


class ConferenceDBManager(BaseProductDBManager):
    """Класс-менеджер работы с моделями CommonConference и Conference."""

    _common_model = CommonConference
    _model = Conference


class CourseDBManager(ProductQuestionsDBManager):
    """Класс-менеджер работы с моделями CommonCourse и Course."""

    _common_model = CommonCourse
    _model = Course
    _user_model = CourseUser


class BreakfastDBManager(ProductLimitUserDBManager):
    """Класс-менеджер работы с моделями CommonBreakfast и Breakfast."""

    _common_model = CommonBreakfast
    _model = Breakfast

    @staticmethod
    @database_sync_to_async
    def get_price(obj: Breakfast) -> Optional[int]:
        """Метод получения цены коуч-завтрака."""
        return obj.price.price

    @staticmethod
    @database_sync_to_async
    def add_menu_position_to_user(
            obj: Breakfast,
            user_id: int,
            position: Menu,
    ) -> None:
        """Метод добавления позиции меню участнику коуч-завтрака."""
        user = BreakfastUser.objects.filter(
            breakfast=obj,
            user__tg_user_id=user_id,
        ).first()
        user.menu = position
        user.save()


class GameDBManager(ProductLimitUserDBManager):
    """Класс-менеджер работы с моделями CommonGame и Game."""

    _common_model = CommonGame
    _model = Game
