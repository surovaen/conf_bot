from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, InputMediaPhoto

from server.apps.payments.enums import ProductTypes
from server.apps.telegram.cache.manager import RedisCacheManager
from server.apps.telegram.database.managers import (
    game_db_manager,
    user_db_manager,
    userlimit_db_manager,
)
from server.apps.telegram.handlers.decorator import ErrorHandler
from server.apps.telegram.handlers.enums import Callback
from server.apps.telegram.handlers.utils import create_payment, get_media_path
from server.apps.telegram.states.enums import StageType, StateType
from server.apps.telegram.utils import buttons, messages
from server.apps.telegram.utils.keyboards import KeyboardConstructor


@ErrorHandler.create()
async def game_callback(callback: CallbackQuery, bot: AsyncTeleBot):
    """Обработка колбека по разделу 'Игра'."""
    text = messages.NOT_INFO_TEXT
    keyboard = KeyboardConstructor().create_menu_keyboard()

    common_data = await game_db_manager.get_common_data()

    if not common_data or not common_data.text:
        return await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=keyboard,
        )

    text = common_data.text
    price = common_data.price

    images = await game_db_manager.get_images(obj=common_data)

    if images:
        image_paths = [
            get_media_path(image.get('image')) for image in images
        ]
        first_image = image_paths[0].open(mode='rb')

        if len(image_paths) == 1:
            await bot.send_photo(
                chat_id=callback.message.chat.id,
                photo=first_image,
                caption=text,
                reply_markup=keyboard,
            )
        else:
            media_group = [
                InputMediaPhoto(first_image, caption=text),
            ]
            media_group.extend(
                [
                    InputMediaPhoto(image.open(mode='rb')) for image in image_paths[1:]
                ]
            )
            await bot.send_media_group(
                chat_id=callback.message.chat.id,
                media=media_group,
            )
    else:
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=keyboard,
        )

    games = await game_db_manager.get_all_current_data()

    for game in games:
        text = '{date} {type}'.format(
            date=game.get('date').strftime('%d.%m.%Y'),
            type=game.get('type'),
        )
        uuid = str(game.get('uuid'))
        keyboard = KeyboardConstructor().create_inline_keyboard(
            {
                buttons.PAID.format(price=price): Callback.GAME_PAYMENT_UUID.value.format(uuid=uuid),
            },
        )
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=keyboard,
        )
    return


@ErrorHandler.create()
async def game_payment_callback(callback: CallbackQuery, bot: AsyncTeleBot):
    """Обработка платежа участия в игре."""
    keyboard = KeyboardConstructor().create_menu_keyboard()
    uuid = callback.data.split('_')[-1]

    game = await game_db_manager.get(uuid=uuid)

    paid_count = await game_db_manager.get_paid_count(obj=game)
    game_limit = await userlimit_db_manager.get_limit(type_limit='game_limit')

    if paid_count >= game_limit:
        text = messages.EXCEED_LIMIT_TEXT
        return await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=keyboard,
        )

    common_data = await game_db_manager.get_common_data()
    price = common_data.price
    user = await user_db_manager.get(
        user_id=callback.from_user.id,
    )

    if not user.is_data_filled:
        state = 0
        cache_data = {
            'state_type': StateType.USER_INFO.value,
            'state': state,
            'stage': StageType.GAME.value,
            'tg_user_id': callback.from_user.id,
            'uuid': uuid,
            'price': price,
        }
        RedisCacheManager.set(
            key=callback.from_user.id,
            **cache_data,
        )
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=messages.USER_INFO_PAYMENT_TEXT,
            reply_markup=keyboard,
        )
        return await bot.send_message(
            chat_id=callback.message.chat.id,
            text=messages.USER_INFO_MSG_MAP[state],
            reply_markup=keyboard,
        )

    payment_link = await create_payment(
        user_id=callback.from_user.id,
        product=ProductTypes.GAME,
        event_uuid=uuid,
        price=price,
    )

    text = messages.PAYMENT_URL_TEXT + '\n\n' + payment_link
    return await bot.send_message(
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )
