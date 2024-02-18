from django.contrib import admin

from server.apps.payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = (
        'user', 'product', 'price', 'status', 'data', 'ticket',
    )
    exclude = ('product_id',)
    list_display = ('__str__', 'user', 'product', 'price', 'status',)
    list_filter = ('status', 'product', 'ticket',)
