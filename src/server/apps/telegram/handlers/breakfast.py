from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, InputMediaPhoto

from server.apps.payments.enums import ProductTypes
from server.apps.telegram.cache.manager import RedisCacheManager
from server.apps.telegram.database.managers import (
    breakfast_db_manager,
    menu_db_manager,
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
async def breakfast_callback(callback: CallbackQuery, bot: AsyncTeleBot):
    """Обработка колбека по разделу 'Коуч-завтрак'."""
    text = messages.NOT_INFO_TEXT
    keyboard = KeyboardConstructor().create_menu_keyboard()

    common_data = await breakfast_db_manager.get_common_data()

    if not common_data or not common_data.text:
        return await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=keyboard,
        )

    text = common_data.text

    images = await breakfast_db_manager.get_images(obj=common_data)

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

    breakfasts = await breakfast_db_manager.get_all_current_data()

    for breakfast in breakfasts:
        text = '{date}\n{title}\n'.format(
            date=breakfast.get('date').strftime('%d.%m.%Y'),
            title=breakfast.get('title'),
        )
        uuid = str(breakfast.get('uuid'))
        keyboard = KeyboardConstructor().create_inline_keyboard(
            {
                buttons.DETAILS: Callback.BREAKFAST_DETAILS_UUID.value.format(uuid=uuid),
            }
        )
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=keyboard,
        )
    return


@ErrorHandler.create()
async def breakfast_details_callback(callback: CallbackQuery, bot: AsyncTeleBot):
    """Обработка получения информации о коуч-завтраке."""
    uuid = callback.data.split('_')[-1]

    breakfast = await breakfast_db_manager.get(uuid=uuid)
    text = '{date}\n{title}\n\n{description}\n\nМесто: {place}'.format(
        date=breakfast.date.strftime('%d.%m.%Y'),
        title=breakfast.title,
        description=breakfast.description,
        place=breakfast.place,
    )
    price = await breakfast_db_manager.get_price(obj=breakfast)
    keyboard = KeyboardConstructor().create_inline_keyboard(
        {
            buttons.PAID.format(price=price): Callback.BREAKFAST_PAYMENT_UUID.value.format(uuid=uuid),
        }
    )
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )


@ErrorHandler.create()
async def breakfast_payment_callback(callback: CallbackQuery, bot: AsyncTeleBot):
    """Обработка платежа за коуч-завтрак."""
    keyboard = KeyboardConstructor().create_menu_keyboard()
    uuid = callback.data.split('_')[-1]

    breakfast = await breakfast_db_manager.get(uuid=uuid)

    paid_count = await breakfast_db_manager.get_paid_count(obj=breakfast)
    breakfast_limit = await userlimit_db_manager.get_limit(type_limit='breakfast_limit')

    if paid_count >= breakfast_limit:
        text = messages.EXCEED_LIMIT_TEXT
        return await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=keyboard,
        )

    price = await breakfast_db_manager.get_price(obj=breakfast)
    user = await user_db_manager.get(
        user_id=callback.from_user.id,
    )

    if not user.is_data_filled:
        state = 0
        cache_data = {
            'state_type': StateType.USER_INFO.value,
            'state': state,
            'stage': StageType.BREAKFAST.value,
            'tg_user_id': callback.from_user.id,
            'uuid': uuid,
            'price': price,

        }
        RedisCacheManager.set(
            key=callback.from_user.id,
            **cache_data,
        )

        await bot.send_message(
            callback.message.chat.id,
            text=messages.USER_INFO_PAYMENT_TEXT,
            reply_markup=keyboard,
        )
        return await bot.send_message(
            callback.message.chat.id,
            text=messages.USER_INFO_MSG_MAP[state],
            reply_markup=keyboard,
        )

    payment_link = await create_payment(
        user_id=callback.from_user.id,
        product=ProductTypes.BREAKFAST,
        event_uuid=uuid,
        price=price,
    )

    text = messages.PAYMENT_URL_TEXT + '\n\n' + payment_link
    return await bot.send_message(
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )


@ErrorHandler.create()
async def menu_breakfast_callback(callback: CallbackQuery, bot: AsyncTeleBot):
    """Обработка колбека выбранной позиции меню по коуч-завтраку."""
    breakfast_uuid = callback.data.split('_')[1]
    position_id = callback.data.split('_')[-1]

    breakfast = await breakfast_db_manager.get(uuid=breakfast_uuid)
    position = await menu_db_manager.get(position_id=position_id)
    await breakfast_db_manager.add_menu_position_to_user(
        obj=breakfast,
        user_id=callback.from_user.id,
        position=position,
    )

    text = messages.BREAKFAST_CONFIRMATION_TEXT.format(place=breakfast.place)
    keyboard = KeyboardConstructor().create_menu_keyboard()
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )
