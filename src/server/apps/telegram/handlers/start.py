from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from server.apps.telegram.cache.manager import RedisCacheManager
from server.apps.telegram.database.managers import user_db_manager
from server.apps.telegram.handlers.decorator import ErrorHandler
from server.apps.telegram.states.enums import StageType, StateType
from server.apps.telegram.utils import messages
from server.apps.telegram.utils.keyboards import KeyboardConstructor


@ErrorHandler.create()
async def start(message: Message, bot: AsyncTeleBot):
    """Обработка команды '/start'."""

    username = message.from_user.username if message.from_user.username else message.from_user.first_name
    user_data = {
        'username': username,
        'tg_user_id': message.from_user.id,
        'tg_chat_id': message.chat.id,
    }

    await user_db_manager.create(**user_data)

    state = 0
    user_data.update(
        {
            'state_type': StateType.USER_INFO.value,
            'state': state,
            'stage': StageType.START.value,
        }
    )
    RedisCacheManager.set(
        key=message.from_user.id,
        **user_data,
    )

    keyboard = KeyboardConstructor().create_menu_keyboard()

    await bot.send_message(
        chat_id=message.chat.id,
        text=messages.START_TEXT,
        reply_markup=keyboard,
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=messages.USER_INFO_MSG_MAP[state],
        reply_markup=keyboard,
    )
