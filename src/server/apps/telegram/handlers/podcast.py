from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery

from server.apps.telegram.database.managers import podcast_db_manager, user_db_manager
from server.apps.telegram.handlers.decorator import ErrorHandler
from server.apps.telegram.utils import messages
from server.apps.telegram.utils.keyboards import KeyboardConstructor


@ErrorHandler.create()
async def podcast_callback(callback: CallbackQuery, bot: AsyncTeleBot):
    """Обработка колбека по разделу 'Подкасты'."""
    text = messages.NOT_INFO_TEXT
    keyboard = KeyboardConstructor().create_menu_keyboard()

    podcast_data = await podcast_db_manager.get_common_data()

    if not podcast_data or not podcast_data.text:
        return await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=keyboard,
        ),

    user = await user_db_manager.get(
        user_id=callback.from_user.id,
    )
    user_name = user.first_name if user.first_name else user.username
    text = podcast_data.text.format(name=user_name)

    podcast_links = await podcast_db_manager.get_links(podcast=podcast_data)

    if podcast_links:
        links = '\n\n'.join(
            [
                '{title}\n{link}'.format(
                    title=link.get('title'),
                    link=link.get('link'),
                ) for link in podcast_links
            ]
        )
        text += '\n\n' + links

    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=keyboard,
    ),
