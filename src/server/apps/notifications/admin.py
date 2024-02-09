from django.contrib import admin
from solo.admin import SingletonModelAdmin

from server.apps.notifications.models import (
    MassNotification,
    MassNotificationImage,
    PaymentNotification,
)


class MassNotificationImageAdminInline(admin.TabularInline):
    model = MassNotificationImage


@admin.register(MassNotification)
class MassNotificationAdmin(admin.ModelAdmin):
    inlines = (MassNotificationImageAdminInline,)
    fields = (
        'is_send', 'description', 'is_sent',
    )
    list_display = (
        '__str__', 'is_send', 'is_sent',
    )


@admin.register(PaymentNotification)
class PaymentNotificationAdmin(SingletonModelAdmin):
    pass
