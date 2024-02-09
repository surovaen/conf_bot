from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery

from server.apps.telegram.database.managers import gift_db_manager
from server.apps.telegram.handlers.decorator import ErrorHandler
from server.apps.telegram.handlers.utils import get_media_path
from server.apps.telegram.utils import messages
from server.apps.telegram.utils.keyboards import KeyboardConstructor


@ErrorHandler.create()
async def gift_callback(callback: CallbackQuery, bot: AsyncTeleBot):
    """Обработка колбека по разделу 'Забрать подарок'."""
    keyboard = KeyboardConstructor().create_menu_keyboard()
    text = messages.NOT_INFO_TEXT

    gift_data = await gift_db_manager.get_common_data()

    if not gift_data or not gift_data.text:
        return await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=keyboard,
        )

    text = gift_data.text
    links = await gift_db_manager.get_links(gift=gift_data)
    files = await gift_db_manager.get_files(gift=gift_data)
    images = await gift_db_manager.get_images(gift=gift_data)

    if not (links or files or images):
        text += '\n\n' + messages.NOT_GIFTS
        return await bot.send_message(
            chat_id=callback.message.chat.id,
            text=text,
            reply_markup=keyboard,
        )

    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )

    if links:
        links_data = '\n\n'.join(
            [
                '{title}\n{link}'.format(
                    title=link.get('title'),
                    link=link.get('link'),
                ) for link in links
            ]
        )
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=links_data,
            reply_markup=keyboard,
        )

    if images:
        image_data = {
            image.get('title'): get_media_path(image.get('image')) for image in images
        }

        for text, path in image_data.items():
            await bot.send_photo(
                chat_id=callback.message.chat.id,
                photo=path.open(mode='rb'),
                caption=text,
                reply_markup=keyboard,
            )

    if files:
        file_data = {
            file.get('title'): get_media_path(file.get('file')) for file in files
        }
        for text, path in file_data.items():
            await bot.send_document(
                chat_id=callback.message.chat.id,
                document=path.open(mode='rb'),
                caption=text,
                reply_markup=keyboard,
            )
