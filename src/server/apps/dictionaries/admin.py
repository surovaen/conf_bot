from django.contrib import admin
from solo.admin import SingletonModelAdmin

from server.apps.dictionaries.models import (
    BreakfastPrice,
    Menu,
    PreRecordingQuestion,
    PromotionalCode,
    TicketCategory,
    UserLimit,
)


@admin.register(UserLimit)
class UserLimitAdmin(SingletonModelAdmin):
    pass


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass


@admin.register(BreakfastPrice)
class BreakfastPriceAdmin(admin.ModelAdmin):
    pass


@admin.register(PreRecordingQuestion)
class PreRecordingQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(PromotionalCode)
class PromotionalCodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount',)


@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ('type', 'price')
