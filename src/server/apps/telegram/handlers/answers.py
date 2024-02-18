from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from server.apps.payments.enums import ProductTypes
from server.apps.telegram.cache.manager import RedisCacheManager
from server.apps.telegram.database.managers import (
    breakfast_db_manager,
    conference_db_manager,
    course_db_manager,
    feedback_db_manager,
    game_db_manager,
    user_db_manager,
)
from server.apps.telegram.handlers.decorator import ErrorHandler
from server.apps.telegram.handlers.enums import Callback
from server.apps.telegram.handlers.utils import check_promo, create_payment
from server.apps.telegram.states.enums import StageType, StateType
from server.apps.telegram.states.mapping import STATE_TYPE_MAPPING
from server.apps.telegram.utils import buttons, messages
from server.apps.telegram.utils.keyboards import KeyboardConstructor


EVENT_DB_MANAGER_MAP = {
    'conference': conference_db_manager,
    'breakfast': breakfast_db_manager,
    'game': game_db_manager,
}


@ErrorHandler.create()
async def process_answers(message: Message, bot: AsyncTeleBot):
    """Обработка ответов пользователей."""
    user_data = RedisCacheManager.get(
        key=message.from_user.id,
    )

    if not user_data:
        return

    state_type = user_data.pop('state_type')

    if state_type == StateType.PROMO.value:
        price = int(user_data.get('price'))
        uuid = user_data.get('uuid')
        is_promo_exist, discount = await check_promo(promo=message.text)

        if not is_promo_exist:
            text = messages.PROMO_ERROR_TEXT.format(promo=message.text)
            keyboard = KeyboardConstructor().create_inline_keyboard(
                {
                    buttons.PROMO: Callback.PROMO.value,
                    buttons.BUY.format(price=price): Callback.CONFERENCE_PAYMENT_UUID.value.format(uuid=uuid),
                }
            )
            return await bot.send_message(
                chat_id=message.chat.id,
                text=text,
                reply_markup=keyboard,
            )
        new_price = price - price * discount / 100
        new_price = int(new_price)
        user_data.update(
            {
                'price': str(new_price),
            },
        )
        RedisCacheManager.set(
            key=message.from_user.id,
            **user_data,
        )
        text = messages.PROMO_SUCCESS_TEXT.format(promo=message.text)
        keyboard = KeyboardConstructor().create_inline_keyboard(
            {
                buttons.BUY.format(price=new_price): Callback.CONFERENCE_PAYMENT_UUID.value.format(uuid=uuid),
            }
        )
        return await bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=keyboard,
        )

    if state_type == StateType.FEEDBACK.value:
        event = await EVENT_DB_MANAGER_MAP[user_data.get('event_type')].get(user_data.get('uuid'))
        user = await user_db_manager.get(user_id=message.from_user.id)
        await feedback_db_manager.add_feedback(
            event=event,
            event_type=user_data.get('event_type'),
            user=user,
            text=message.text,
        )
        RedisCacheManager.delete(
            key=message.from_user.id,
        )
        text = messages.FEEDBACK_TEXT
        keyboard = KeyboardConstructor().create_menu_keyboard()
        return await bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=keyboard,
        )

    text, keyboard, cache_data = await STATE_TYPE_MAPPING[
        state_type
    ](user_data.get('state'), message).execute()

    RedisCacheManager.set(
        key=message.from_user.id,
        **cache_data,
    )

    user_data = RedisCacheManager.get(
        key=message.from_user.id,
    )

    state_type = user_data.pop('state_type')
    state = user_data.pop('state')
    stage = user_data.pop('stage')

    if state is None:
        if state_type == StateType.USER_INFO.value:
            await user_db_manager.create(**user_data)
            await bot.send_message(
                chat_id=message.chat.id,
                text=text,
                reply_markup=keyboard,
            )

            if stage == StageType.START.value:
                text = messages.START_MENU_TEXT.format(name=user_data.get('first_name'))
                keyboard = await KeyboardConstructor().create_main_keyboard()
                RedisCacheManager.delete(
                    key=message.from_user.id,
                )

            if stage == StageType.COURSE_QUESTIONS.value:
                text = messages.CONTINUE_PRERECORD
                keyboard = KeyboardConstructor().create_inline_keyboard(
                    {
                        buttons.CONTINUE: Callback.COURSE_PRERECORD.value,
                    },
                )
                RedisCacheManager.delete(
                    key=message.from_user.id,
                )

            if stage == StageType.PERSONAL_WORK.value:
                text = messages.PERSONAL_WORK_TEXT
                keyboard = KeyboardConstructor().create_inline_keyboard(
                    {
                        buttons.PERSONAL_WORK: Callback.PERSONAL_WORK.value,
                    },
                )
                RedisCacheManager.delete(
                    key=message.from_user.id,
                )

            if stage == StageType.BREAKFAST.value:
                price = user_data.pop('price')
                uuid = user_data.pop('uuid')
                user_id = user_data.pop('tg_user_id')

                payment_link = await create_payment(
                    user_id=user_id,
                    product=ProductTypes.BREAKFAST,
                    event_uuid=uuid,
                    price=price,
                )

                text = messages.PAYMENT_URL_TEXT + '\n\n' + payment_link
                RedisCacheManager.delete(
                    key=message.from_user.id,
                )

            if stage == StageType.GAME.value:
                price = user_data.pop('price')
                uuid = user_data.pop('uuid')
                user_id = user_data.pop('tg_user_id')

                payment_link = await create_payment(
                    user_id=user_id,
                    product=ProductTypes.GAME,
                    event_uuid=uuid,
                    price=price,
                )

                text = messages.PAYMENT_URL_TEXT + '\n\n' + payment_link

                RedisCacheManager.delete(
                    key=message.from_user.id,
                )

            if stage == StageType.CONF_QUESTIONS.value:
                price = user_data.get('price')
                uuid = user_data.get('uuid')
                text = messages.CONFERENCE_PAID_TEXT
                keyboard = KeyboardConstructor().create_inline_keyboard(
                    {
                        buttons.BUY.format(price=price): Callback.CONFERENCE_PAYMENT_UUID.value.format(uuid=uuid),
                    }
                )

        if state_type == StateType.COURSE_QUESTIONS.value:
            uuid = user_data.pop('uuid')
            await course_db_manager.add_user_and_answers(
                user_id=message.from_user.id,
                uuid=uuid,
                answers=user_data,
            )
            text = messages.AFTER_COURSE_RECORDING_TEXT

            RedisCacheManager.delete(
                key=message.from_user.id,
            )

    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=keyboard,
    )
