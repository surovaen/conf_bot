from django.urls import include, path

from server.api.v1 import urls as urls_v1


urlpatterns = [
    path('v1/', include((urls_v1, 'api_v1'))),
]
