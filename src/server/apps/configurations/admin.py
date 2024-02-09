from django.contrib import admin
from django.contrib.auth.models import Group
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from solo.admin import SingletonModelAdmin

from server.apps.configurations.core.admin import BaseAdminInline
from server.apps.configurations.models import (
    BreakfastImage,
    CommonBreakfast,
    CommonConference,
    CommonCourse,
    CommonGame,
    ConferenceImage,
    CourseImage,
    GameImage,
    Gift,
    GiftFile,
    GiftImage,
    GiftLink,
    PersonalWork,
    PersonalWorkUser,
    Podcast,
    PodcastLink,
)


class ConferenceImageAdminInline(BaseAdminInline):
    model = ConferenceImage


@admin.register(CommonConference)
class CommonConferenceAdmin(SingletonModelAdmin):
    inlines = (ConferenceImageAdminInline,)


class CourseImageAdminInline(BaseAdminInline):
    model = CourseImage


@admin.register(CommonCourse)
class CommonCourseAdmin(SingletonModelAdmin):
    inlines = (CourseImageAdminInline,)


class BreakfastImageAdminInline(BaseAdminInline):
    model = BreakfastImage


@admin.register(CommonBreakfast)
class CommonBreakfastAdmin(SingletonModelAdmin):
    inlines = (BreakfastImageAdminInline,)


class GameImageAdminInline(BaseAdminInline):
    model = GameImage


@admin.register(CommonGame)
class CommonGameAdmin(SingletonModelAdmin):
    inlines = (GameImageAdminInline,)


class PersonalWorkUserAdminInline(admin.TabularInline):
    model = PersonalWorkUser

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(PersonalWork)
class PersonalWorkAdmin(SingletonModelAdmin):
    inlines = (PersonalWorkUserAdminInline,)
    help_texts = {
        'text': 'На месте, где должно быть имя пользователя, укажите {name}. Например: {name}, приняли твой запрос! '
                'На месте, где должна быть расположена ссылка на телеграм - укажите {telegram}. '
                'На месте, где должна быть расположена ссылка на whatsapp - укажите {whatsapp}. ',
    }

    def get_form(self, *args, **kwargs):
        kwargs.update(
            {'help_texts': self.help_texts},
        )
        return super().get_form(*args, **kwargs)


class PodcastLinkAdminInline(BaseAdminInline):
    model = PodcastLink


@admin.register(Podcast)
class PodcastAdmin(SingletonModelAdmin):
    inlines = (PodcastLinkAdminInline,)
    help_texts = {
        'text': 'На месте, где должно быть имя пользователя, укажите {name}. Например: Отличный выбор, {name}!',
    }

    def get_form(self, *args, **kwargs):
        kwargs.update(
            {'help_texts': self.help_texts},
        )
        return super().get_form(*args, **kwargs)


class GiftFileAdminInline(BaseAdminInline):
    model = GiftFile


class GiftLinkAdminInline(BaseAdminInline):
    model = GiftLink


class GiftImageAdminInline(BaseAdminInline):
    model = GiftImage


@admin.register(Gift)
class GiftAdmin(SingletonModelAdmin):
    inlines = (
        GiftFileAdminInline,
        GiftLinkAdminInline,
        GiftImageAdminInline,
    )


admin.site.unregister(Group)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(PeriodicTask)
