import logging
import traceback
from typing import Union

from telebot import logger
from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, Message

from server.apps.telegram.utils import messages
from server.apps.telegram.utils.keyboards import KeyboardConstructor


logger = logger
logger.setLevel(logging.DEBUG)


class ErrorHandler:
    """Класс-декоратор обработки ошибок в хэндлерах бота."""

    def __init__(self, callback):
        """Определение функции хэндлера как аргумента."""
        self.callback = callback

    async def __call__(
            self,
            message: Union[CallbackQuery, Message],
            bot: AsyncTeleBot,
    ):
        """Вызов хэндлера."""
        try:
            await self.callback(message, bot)
        except Exception:
            trace = traceback.format_exc()
            return await self._on_failure(
                message=message,
                bot=bot,
                trace=trace,
            )

    async def _on_failure(
            self,
            message: Union[CallbackQuery, Message],
            bot: AsyncTeleBot,
            trace: str,
    ):
        """Метод обработки ошибки вызова хэндлера."""
        logger.error(trace)
        text = messages.ERROR_BOT_TEXT
        keyboard = KeyboardConstructor().create_menu_keyboard()

        try:
            chat_id = message.message.chat.id
        except AttributeError:
            chat_id = message.chat.id

        return await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=keyboard,
        )

    @classmethod
    def create(cls):
        """Декоратор для создания экземпляра хэндлера."""
        def decorator(function):
            async def wrapper(
                    message: Union[CallbackQuery, Message],
                    bot: AsyncTeleBot,
            ):
                result = cls(function)
                return await result(message, bot)
            return wrapper
        return decorator
