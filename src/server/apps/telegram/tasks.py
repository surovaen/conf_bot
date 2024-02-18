from typing import List

from asgiref.sync import async_to_sync
from telebot.types import InputMediaPhoto

from server import celery_app
from server.apps.telegram.cache.manager import RedisCacheManager
from server.apps.telegram.handlers.utils import get_media_path
from server.apps.telegram.main import bot
from server.apps.telegram.utils.keyboards import KeyboardConstructor


async def send_notification_message(
        chat_id: str,
        message: str,
        images: List[str] = None,
        buttons: dict = None,
        file: str = None,
        cache_data: dict = None,
):
    """Функция отправки сообщения в чат."""
    keyboard = KeyboardConstructor().create_menu_keyboard()

    if cache_data:
        RedisCacheManager.set(key=cache_data.get('tg_user_id'), **cache_data)

    if buttons:
        keyboard = KeyboardConstructor().create_inline_keyboard(buttons)

    if images:
        image_paths = [
            get_media_path(*image) for image in images
        ]
        first_image = open(image_paths[0], mode='rb')

        if len(image_paths) == 1:
            return await bot.send_photo(
                chat_id,
                photo=first_image,
                caption=message,
                reply_markup=keyboard,
            )

        media_group = [
            InputMediaPhoto(first_image, caption=message),
        ]
        media_group.extend(
            [
                InputMediaPhoto(open(image, mode='rb')) for image in image_paths[1:]
            ]
        )
        return await bot.send_media_group(
            chat_id,
            media=media_group,
        )

    await bot.send_message(
        chat_id,
        text=message,
        reply_markup=keyboard,
    )
    if file:
        await bot.send_document(
            chat_id,
            document=open(file, mode='rb'),
            reply_markup=keyboard,
        )


@celery_app.task(
    name='send_message',
    autoretry_for=(Exception,),
)
def send_message(
        chat_id: str,
        message: str,
        images: List[str] = None,
        buttons: dict = None,
        file: str = None,
        cache_data: dict = None,
):
    """Задача отправки сообщения в чат."""
    async_to_sync(send_notification_message)(
        chat_id=chat_id,
        message=message,
        images=images,
        buttons=buttons,
        file=file,
        cache_data=cache_data,
    )
