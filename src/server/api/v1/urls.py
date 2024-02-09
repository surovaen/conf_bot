from django.urls import include, path

from server.api.v1.payment import urls as urls_payment


urlpatterns = [
    path('payment/', include(urls_payment)),
]
