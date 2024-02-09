from django.urls import path

from server.api.v1.payment.views import process_payment


urlpatterns = [
    path('status/', process_payment),
]
