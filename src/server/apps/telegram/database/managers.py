from server.apps.telegram.database.configurations import (
    GiftDBManager,
    MenuDBManager,
    PersonalWorkDBManager,
    PodcastDBManager,
    PromotionalCodeDBManager,
    TicketCategoryDBManager,
    UserLimitDBManager,
)
from server.apps.telegram.database.feedback import FeedbackDBManager
from server.apps.telegram.database.payments import PaymentDBManager
from server.apps.telegram.database.products import (
    BreakfastDBManager,
    ConferenceDBManager,
    CourseDBManager,
    GameDBManager,
)
from server.apps.telegram.database.telegram import MenuButtonDBManager, UserDBManager


user_db_manager = UserDBManager()
personal_work_db_manager = PersonalWorkDBManager()
podcast_db_manager = PodcastDBManager()
gift_db_manager = GiftDBManager()
conference_db_manager = ConferenceDBManager()
breakfast_db_manager = BreakfastDBManager()
game_db_manager = GameDBManager()
course_db_manager = CourseDBManager()
payment_db_manager = PaymentDBManager()
menu_db_manager = MenuDBManager()
feedback_db_manager = FeedbackDBManager()
userlimit_db_manager = UserLimitDBManager()
menubutton_db_manager = MenuButtonDBManager()
promo_db_manager = PromotionalCodeDBManager()
tickets_db_manager = TicketCategoryDBManager()
