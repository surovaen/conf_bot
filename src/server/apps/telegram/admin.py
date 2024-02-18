from django.contrib import admin

from server.apps.telegram.models import BotUser, MenuButton


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'phone_number',)
    fields = (
        'username', 'first_name', 'last_name',
        'phone_number', 'instagram', 'tg_user_id', 'tg_chat_id',
    )


@admin.register(MenuButton)
class MenuButtonAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_shown',)
