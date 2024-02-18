from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, InputMediaPhoto

from server.apps.payments.enums import ProductTypes
from server.apps.telegram.cache.manager import RedisCacheManager
from server.apps.telegram.database.managers import (
    conference_db_manager,
    payment_db_manager,
    tickets_db_manager,
    user_db_manager,
)
from server.apps.telegram.handlers.decorator import ErrorHandler
from server.apps.telegram.handlers.enums import Callback
from server.apps.telegram.handlers.utils import create_payment, get_media_path
from server.apps.telegram.states.enums import StageType, StateType
from server.apps.telegram.utils import buttons, messages
from server.apps.telegram.utils.keyboards import KeyboardConstructor


@ErrorHandler.create()
async def conference_callback(callback: CallbackQuery, bot: AsyncTeleBot):
    """Обработка колбека по разделу 'Конференция'."""
    text = messages.NOT_INFO_TEXT
    keyboard = KeyboardConstructor().create_menu_keyboard()

    common_data = await conference_db_manager.get_common_data()

    if not common_data or not common_data.text:
        return await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=keyboard,
        )

    text = common_data.text
    keyboard = KeyboardConstructor().create_inline_keyboard(
        {
            buttons.PREPAID: Callback.CONFERENCE_PRERECORD.value,
        },
    )

    images = await conference_db_manager.get_images(obj=common_data)

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
async def conference_prerecord_callback(callback: CallbackQuery, bot: AsyncTeleBot):
    """Обработка предзаписи на конференцию."""
    keyboard = KeyboardConstructor().create_menu_keyboard()
    conference = await conference_db_manager.get_one_current_data()

    if not conference:
        text = messages.NOT_PRERECORDING_TEXT
        return await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=keyboard,
        )

    uuid = str(conference.uuid)
    text = messages.TICKET_CATEGORY_TEXT
    tickets = await tickets_db_manager.get_tickets()
    ticket_buttons = {
        buttons.TICKET.format(
            type=ticket.get('type'),
        ): Callback.CONFERENCE_TICKET_UUID.value.format(
            uuid=uuid,
            type=ticket.get('type'),
        )
        for ticket in tickets
    }
    keyboard = KeyboardConstructor().create_inline_keyboard(
        ticket_buttons,
    )
    return await bot.send_message(
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )


@ErrorHandler.create()
async def conference_ticket_callback(callback: CallbackQuery, bot: AsyncTeleBot):
    """Обработка категории билета на конференцию."""
    ticket_type = callback.data.split('_')[-1]
    uuid = callback.data.split('_')[-2]
    ticket = await tickets_db_manager.get_ticket(ticket_type=ticket_type)
    paid_count = await payment_db_manager.get_count_ticket_payments(ticket=ticket_type)

    text = ticket.description
    if paid_count >= ticket.limit:
        keyboard = KeyboardConstructor().create_inline_keyboard(
            {
                buttons.SOLD_OUT: Callback.NONE.value
                # buttons.BUY.format(price=price): Callback.CONFERENCE_PAYMENT_UUID.value.format(uuid=uuid),
            }
        )
        return await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=keyboard,
        )

    price = ticket.price
    keyboard = KeyboardConstructor().create_inline_keyboard(
        {
            buttons.PROMO: Callback.PROMO.value,
            buttons.BUY.format(price=price): Callback.CONFERENCE_PAYMENT_UUID.value.format(uuid=uuid),
        }
    )
    cache_data = {
        'state_type': StateType.PROMO.value,
        'price': price,
        'uuid': uuid,
        'ticket_type': ticket_type,
    }
    RedisCacheManager.set(
        key=callback.from_user.id,
        **cache_data,
    )
    return await bot.send_message(
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )


@ErrorHandler.create()
async def none_callback(callback: CallbackQuery, bot: AsyncTeleBot):
    """Обработка оплаты за участие в конференции."""
    return


@ErrorHandler.create()
async def conference_payment_callback(callback: CallbackQuery, bot: AsyncTeleBot):
    """Обработка оплаты за участие в конференции."""
    uuid = callback.data.split('_')[-1]
    keyboard = KeyboardConstructor().create_menu_keyboard()

    user_data = RedisCacheManager.get(
        key=callback.from_user.id,
    )

    price = user_data.get('price')
    user = await user_db_manager.get(
        user_id=callback.from_user.id,
    )

    if not user.is_data_filled:
        state = 0
        cache_data = {
            'state_type': StateType.USER_INFO.value,
            'state': state,
            'stage': StageType.CONF_QUESTIONS.value,
            'tg_user_id': callback.from_user.id,
            'price': price,
            'uuid': uuid,
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

    ticket = user_data.get('ticket_type')
    payment_link = await create_payment(
        user_id=callback.from_user.id,
        product=ProductTypes.CONFERENCE,
        event_uuid=uuid,
        price=int(price),
        ticket=ticket,
    )

    text = messages.PAYMENT_URL_TEXT + '\n\n' + payment_link

    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )


@ErrorHandler.create()
async def promo_callback(callback: CallbackQuery, bot: AsyncTeleBot):
    """Обработка."""
    text = messages.PROMO_TEXT
    keyboard = KeyboardConstructor().create_menu_keyboard()

    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )
