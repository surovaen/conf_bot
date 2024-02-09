from django.contrib import admin
from django.http import HttpResponse

from server.apps.products.report.builder import ReportXlsxBuilder
from server.apps.products.report.provider import BreakfastReportProvider


class AddPrerecordUserCountMixin:
    """Класс-миксин добавления количества участников, прошедших предзапись."""

    def user_count(self, obj) -> int:
        """Получение количества пользователй, прошедших предзапись."""
        return obj.event_users.count()

    user_count.short_description = 'Пользователи, прошедшие предзапись'


class AddPaidUserCountMixin:
    """Класс-миксин добавления количества участников, оплативших участие."""

    def user_paid_count(self, obj) -> int:
        """Получение количества пользователй, оплативших участие."""
        return obj.users.filter(is_paid=True).count()

    user_paid_count.short_description = 'Пользователи, оплатившие участие'


class AddChangeNotPermissionAdminMixin:
    """Класс-миксин запрета редактирования и добавления записей."""

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class ExportXlsxAdminMixin:
    """Класс-миксин выгрузки данных в xlsx."""

    def export_xlsx(self, request, queryset):
        """Метод формирования отчета в xlsx."""
        if len(queryset) > 1:
            return self.message_user(
                request,
                'Для формирования отчета необходимо выбрать один Коуч-завтрак.',
            )

        data = BreakfastReportProvider(queryset).data
        report = ReportXlsxBuilder(data).build()

        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(
            content=report,
            content_type=content_type,
        )
        response['Content-Disposition'] = 'attachment; filename=report.xlsx'
        return response

    export_xlsx.short_description = 'Выгрузка данных в xlsx'


class NotificationAdmin(admin.StackedInline):
    """Инлайн-админ для уведомлений."""
    extra = 0
    fields = (
        'description', 'type', 'is_sent',
    )
