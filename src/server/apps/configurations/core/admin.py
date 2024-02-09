from django.contrib import admin


class BaseAdminInline(admin.TabularInline):
    """Базовая инлайн-модель админки."""

    extra = 1
