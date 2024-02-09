from django.db import models

from server.apps.telegram.enums import CallbackTypes


class BotUser(models.Model):
    """Модель пользователя чат-бота."""

    username = models.CharField(
        'Имя пользователя',
        max_length=255,
    )
    tg_user_id = models.CharField(
        'user_id',
        max_length=255,
    )
    first_name = models.CharField(
        'Имя',
        max_length=255,
        null=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=255,
        null=True,
    )
    phone_number = models.CharField(
        'Номер телефона',
        max_length=255,
        null=True,
    )
    tg_chat_id = models.CharField(
        'chat_id',
        max_length=255,
    )

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'

    def __str__(self):
        name = f'{self.username}'

        if self.first_name and self.last_name:
            name = f'{self.first_name} {self.last_name}'

        return name

    @property
    def full_name(self):
        """Полное имя пользователя."""
        return f'{self.first_name} {self.last_name}'

    @property
    def is_data_filled(self):
        """Проверка наличия информации о пользователе."""
        if self.first_name and self.last_name and self.phone_number:
            return True

        return False


class MenuButton(models.Model):
    """Модель кнопок меню бота."""

    title = models.CharField(
        'Кнопка',
        max_length=255,
    )
    callback = models.CharField(
        'Обработчик',
        max_length=255,
        choices=CallbackTypes.choices,
        default=None,
    )
    is_shown = models.BooleanField(
        'Показать в боте',
        default=True,
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Кнопка меню'
        verbose_name_plural = 'Кнопки меню'
        ordering = ('pk',)
