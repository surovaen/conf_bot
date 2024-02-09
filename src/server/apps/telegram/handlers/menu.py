from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from server.apps.telegram.cache.manager import RedisCacheManager
from server.apps.telegram.database.managers import user_db_manager
from server.apps.telegram.handlers.decorator import ErrorHandler
from server.apps.telegram.utils import messages
from server.apps.telegram.utils.keyboards import KeyboardConstructor


@ErrorHandler.create()
async def menu(message: Message, bot: AsyncTeleBot):
    """Обработка кнопки 'МЕНЮ'."""
    cache_data = RedisCacheManager.get(key=message.from_user.id)
    if cache_data:
        RedisCacheManager.delete(key=message.from_user.id)

    user = await user_db_manager.get(user_id=message.from_user.id)
    name = user.first_name if user.first_name else user.username
    text = messages.WELCOME_TEXT.format(name=name)
    keyboard = KeyboardConstructor().create_menu_keyboard()

    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=keyboard,
    )

    text = messages.MENU_TEXT
    keyboard = await KeyboardConstructor().create_main_keyboard()

    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=keyboard,
    )
