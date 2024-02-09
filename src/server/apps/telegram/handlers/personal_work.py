from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery

from server.apps.telegram.cache.manager import RedisCacheManager
from server.apps.telegram.database.managers import (
    personal_work_db_manager,
    user_db_manager,
)
from server.apps.telegram.handlers.decorator import ErrorHandler
from server.apps.telegram.states.enums import StageType, StateType
from server.apps.telegram.utils import messages
from server.apps.telegram.utils.keyboards import KeyboardConstructor


@ErrorHandler.create()
async def personal_work_callback(callback: CallbackQuery, bot: AsyncTeleBot):
    """Обработка колбека по разделу 'Хочу в личную работу'."""
    keyboard = KeyboardConstructor().create_menu_keyboard()
    text = messages.NOT_INFO_TEXT
    personal_work_data = await personal_work_db_manager.get_common_data()

    if not personal_work_data or not personal_work_data.text:
        return await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=keyboard,
        )

    user = await user_db_manager.get(
        user_id=callback.from_user.id,
    )

    if not user.is_data_filled:
        state = 0
        cache_data = {
            'state_type': StateType.USER_INFO.value,
            'state': state,
            'stage': StageType.PERSONAL_WORK.value,
            'tg_user_id': callback.from_user.id,
        }

        RedisCacheManager.set(
            key=callback.from_user.id,
            **cache_data,
        )
        await bot.send_message(
            callback.message.chat.id,
            text=messages.USER_INFO_PERSONAL_WORK_TEXT,
            reply_markup=keyboard,
        )
        return await bot.send_message(
            callback.message.chat.id,
            text=messages.USER_INFO_MSG_MAP[state],
            reply_markup=keyboard,
        )

    text = personal_work_data.text.format(
        name=user.first_name,
        telegram=personal_work_data.telegram_link,
        whatsapp=personal_work_data.whatsapp_link,
    )
    await personal_work_db_manager.add_user(
        personal_work=personal_work_data,
        user=user,
    )
    return await bot.send_message(
        callback.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )
