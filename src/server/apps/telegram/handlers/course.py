from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, InputMediaPhoto

from server.apps.telegram.cache.manager import RedisCacheManager
from server.apps.telegram.database.managers import course_db_manager, user_db_manager
from server.apps.telegram.handlers.decorator import ErrorHandler
from server.apps.telegram.handlers.enums import Callback
from server.apps.telegram.handlers.utils import get_media_path
from server.apps.telegram.states.enums import StageType, StateType
from server.apps.telegram.utils import buttons, messages
from server.apps.telegram.utils.keyboards import KeyboardConstructor


@ErrorHandler.create()
async def course_callback(callback: CallbackQuery, bot: AsyncTeleBot):
    """Обработка колбека по разделу 'Курс про деньги'."""
    text = messages.NOT_INFO_TEXT
    keyboard = KeyboardConstructor().create_menu_keyboard()

    common_data = await course_db_manager.get_common_data()

    if not common_data or not common_data.text:
        return await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=keyboard,
        )

    text = common_data.text
    keyboard = KeyboardConstructor().create_inline_keyboard(
        {
            buttons.PRERECORD: Callback.COURSE_PRERECORD.value,
        },
    )

    images = await course_db_manager.get_images(common_data)

    if images:
        image_paths = [
            get_media_path(image.get('image')) for image in images
        ]
        first_image = image_paths[0].open(mode='rb')

        if len(image_paths) == 1:
            return await bot.send_photo(
                chat_id=callback.message.chat.id,
                photo=first_image,
                caption=text,
                reply_markup=keyboard,
            )

        media_group = [
            InputMediaPhoto(image.open(mode='rb')) for image in image_paths
        ]
        await bot.send_media_group(
            chat_id=callback.message.chat.id,
            media=media_group,
        )
    return await bot.send_message(
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )


@ErrorHandler.create()
async def course_prerecord_callback(callback: CallbackQuery, bot: AsyncTeleBot):
    """Обработка предзаписи на курс."""
    keyboard = KeyboardConstructor().create_menu_keyboard()

    user = await user_db_manager.get(
        user_id=callback.from_user.id,
    )

    if not user.is_data_filled:
        state = 0
        cache_data = {
            'state_type': StateType.USER_INFO.value,
            'state': state,
            'stage': StageType.COURSE_QUESTIONS.value,
            'tg_user_id': callback.from_user.id,
        }
        RedisCacheManager.set(
            key=callback.from_user.id,
            **cache_data,
        )

        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=messages.USER_INFO_PRERECORDING_TEXT,
            reply_markup=keyboard,
        )
        return await bot.send_message(
            chat_id=callback.message.chat.id,
            text=messages.USER_INFO_MSG_MAP[state],
            reply_markup=keyboard,
        )

    course = await course_db_manager.get_one_current_data()
    uuid = str(course.uuid)

    if not course:
        text = messages.NOT_PRERECORDING_TEXT
        return await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=keyboard,
        )

    questions = await course_db_manager.get_questions(obj=course)

    if questions:
        cache_data = {
            'state_type': StateType.COURSE_QUESTIONS.value,
            'state': 0,
            'stage': StageType.COURSE_QUESTIONS.value,
            'uuid': uuid,
        }
        RedisCacheManager.set(
            key=callback.from_user.id,
            **cache_data,
        )
        text = messages.PRERECORDING_TEXT
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=keyboard,
        )
        text = questions[0].get('text')
        return await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=keyboard,
        )

    text = messages.COURSE_RECORDING_TEXT
    await course_db_manager.add_user_and_answers(
        user_id=callback.from_user.id,
        uuid=uuid,
        answers=None,
    )
    return await bot.send_message(
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )
