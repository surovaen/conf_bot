from django.contrib import admin

from server.apps.feedback.models import (
    BreakfastFeedback,
    ConferenceFeedback,
    GameFeedback,
)
from server.apps.notifications.models import (
    BreakfastNotification,
    ConferenceNotification,
    GameNotification,
)
from server.apps.products.core.admin import (
    AddChangeNotPermissionAdminMixin,
    AddPaidUserCountMixin,
    AddPrerecordUserCountMixin,
    ExportXlsxAdminMixin,
    NotificationAdmin,
)
from server.apps.products.models import (
    Breakfast,
    BreakfastUser,
    Conference,
    ConferenceUser,
    Course,
    CourseUser,
    Game,
    GameUser,
)


class ConferenceUserAdminInline(AddChangeNotPermissionAdminMixin, admin.TabularInline):
    model = ConferenceUser


class ConferenceNotificationAdminInline(NotificationAdmin):
    model = ConferenceNotification
    help_texts = {
        'description': 'Для автоматической подстановки даты и времени конференции вместо даты укажите {date}, '
                       'вместо времени укажите {time}, или заполните данные вручную',
    }

    def get_formset(self, request, obj=None, **kwargs):
        """Добавление help-текста в форму админки."""
        kwargs.update(
            {
                'help_texts': self.help_texts,
            },
        )
        return super().get_formset(request, obj=None, **kwargs)


class ConferenceFeedbackAdminInline(AddChangeNotPermissionAdminMixin, admin.StackedInline):
    model = ConferenceFeedback


@admin.register(Conference)
class ConferenceAdmin(AddPaidUserCountMixin, admin.ModelAdmin):
    inlines = (
        ConferenceUserAdminInline,
        ConferenceNotificationAdminInline,
        ConferenceFeedbackAdminInline,
    )
    fields = (
        'is_shown', 'date', 'time',
    )
    list_display = (
        'date', 'is_shown', 'user_paid_count',
    )


class CourseUserAdminInline(AddChangeNotPermissionAdminMixin, admin.TabularInline):
    model = CourseUser


@admin.register(Course)
class CourseAdmin(AddPrerecordUserCountMixin, admin.ModelAdmin):
    inlines = (CourseUserAdminInline,)
    fields = (
        'is_shown', 'date', 'time', 'questions',
    )
    list_display = (
        'date', 'is_shown', 'user_count',
    )


class BreakfastUserAdminInline(AddChangeNotPermissionAdminMixin, admin.TabularInline):
    model = BreakfastUser


class BreakfastNotificationAdminInline(NotificationAdmin):
    model = BreakfastNotification
    help_texts = {
        'description': 'Для автоматической подстановки темы, даты и времени коуч-завтрака вместо темы укажите {title}, '
                       'вместо даты укажите {date}, вместо времени укажите {time}, или заполните данные вручную',
    }

    def get_formset(self, request, obj=None, **kwargs):
        """Добавление help-текста в форму админки."""
        kwargs.update(
            {
                'help_texts': self.help_texts,
            },
        )
        return super().get_formset(request, obj=None, **kwargs)


class BreakfastFeedbackAdminInline(AddChangeNotPermissionAdminMixin, admin.StackedInline):
    model = BreakfastFeedback


@admin.register(Breakfast)
class BreakfastAdmin(AddPaidUserCountMixin, ExportXlsxAdminMixin, admin.ModelAdmin):
    inlines = (
        BreakfastUserAdminInline,
        BreakfastNotificationAdminInline,
        BreakfastFeedbackAdminInline,
    )
    fields = (
        'is_shown', 'title', 'date', 'time',
        'description', 'place', 'price', 'menu',
    )
    list_display = (
        'title', 'date', 'is_shown', 'user_paid_count',
    )
    actions = ('export_xlsx',)
    search_fields = ('title',)


class GameUserAdminInline(AddChangeNotPermissionAdminMixin, admin.TabularInline):
    model = GameUser


class GameNotificationAdminInline(NotificationAdmin):
    model = GameNotification
    fields = (
        'description', 'type', 'file', 'is_sent',
    )
    help_texts = {
        'description': 'Для автоматической подстановки даты и времени игры вместо даты укажите {date}, '
                       'вместо времени укажите {time}, или заполните данные вручную',
    }

    def get_formset(self, request, obj=None, **kwargs):
        """Добавление help-текста в форму админки."""
        kwargs.update(
            {
                'help_texts': self.help_texts,
            },
        )
        return super().get_formset(request, obj=None, **kwargs)


class GameFeedbackAdminInline(AddChangeNotPermissionAdminMixin, admin.StackedInline):
    model = GameFeedback


@admin.register(Game)
class GameAdmin(AddPaidUserCountMixin, admin.ModelAdmin):
    inlines = (
        GameUserAdminInline,
        GameNotificationAdminInline,
        GameFeedbackAdminInline,
    )
    fields = (
        'is_shown', 'date', 'time', 'type',
    )
    list_display = (
        '__str__', 'date', 'is_shown', 'user_paid_count',
    )
