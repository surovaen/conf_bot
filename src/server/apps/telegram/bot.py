import logging

from django.conf import settings
from telebot import logger
from telebot.async_telebot import AsyncTeleBot, ExceptionHandler

from server.apps.telegram.handlers.answers import process_answers
from server.apps.telegram.handlers.breakfast import (
    breakfast_callback,
    breakfast_details_callback,
    breakfast_payment_callback,
    menu_breakfast_callback,
)
from server.apps.telegram.handlers.conference import (
    conference_callback,
    conference_payment_callback,
    conference_prerecord_callback,
    promo_callback,
)
from server.apps.telegram.handlers.course import (
    course_callback,
    course_prerecord_callback,
)
from server.apps.telegram.handlers.enums import Callback
from server.apps.telegram.handlers.game import game_callback, game_payment_callback
from server.apps.telegram.handlers.gift import gift_callback
from server.apps.telegram.handlers.menu import menu
from server.apps.telegram.handlers.personal_work import personal_work_callback
from server.apps.telegram.handlers.podcast import podcast_callback
from server.apps.telegram.handlers.start import start
from server.apps.telegram.utils import buttons


logger = logger
logger.setLevel(logging.DEBUG)


class BotExceptionHandler(ExceptionHandler):
    async def handle(self, exception):
        logger.error(exception)


bot = AsyncTeleBot(
    settings.BOT_TOKEN,
    # exception_handler=BotExceptionHandler(),
)


MESSAGE_HANDLERS_MAP = {
    start: {
        'commands': ['start'],
    },
    menu: {
        'func': lambda message: message.text == buttons.MENU,
    },
    process_answers: {
        'content_types': ['text', 'contact'],
    },
}


CALLBACK_HANDLERS_MAP = {
    conference_callback: {
        'func': lambda callback: callback.data == Callback.CONFERENCE.value,
    },
    conference_prerecord_callback: {
        'func': lambda callback: callback.data == Callback.CONFERENCE_PRERECORD.value,
    },
    conference_payment_callback: {
        'func': lambda callback: callback.data.startswith(Callback.CONFERENCE_PAYMENT.value),
    },
    promo_callback: {
        'func': lambda callback: callback.data == Callback.PROMO.value,
    },
    course_callback: {
        'func': lambda callback: callback.data == Callback.COURSE.value,
    },
    course_prerecord_callback: {
        'func': lambda callback: callback.data == Callback.COURSE_PRERECORD.value,
    },
    breakfast_callback: {
        'func': lambda callback: callback.data == Callback.BREAKFAST.value,
    },
    breakfast_details_callback: {
        'func': lambda callback: callback.data.startswith(Callback.BREAKFAST_DETAILS.value),
    },
    breakfast_payment_callback: {
        'func': lambda callback: callback.data.startswith(Callback.BREAKFAST_PAYMENT.value),
    },
    menu_breakfast_callback: {
        'func': lambda callback: callback.data.startswith(Callback.MENU.value),
    },
    game_callback: {
        'func': lambda callback: callback.data == Callback.GAME.value,
    },
    game_payment_callback: {
        'func': lambda callback: callback.data.startswith(Callback.GAME_PAYMENT.value),
    },
    personal_work_callback: {
        'func': lambda callback: callback.data == Callback.PERSONAL_WORK.value,
    },
    podcast_callback: {
        'func': lambda callback: callback.data == Callback.PODCAST.value,
    },
    gift_callback: {
        'func': lambda callback: callback.data == Callback.GIFT.value,
    },
}


def register_handlers():
    """Функция регистрации обработчиков бота."""
    for func, params in MESSAGE_HANDLERS_MAP.items():
        bot.register_message_handler(
            func,
            **params,
            pass_bot=True,
        )

    for func, params in CALLBACK_HANDLERS_MAP.items():
        bot.register_callback_query_handler(
            func,
            **params,
            pass_bot=True,
        )


register_handlers()
