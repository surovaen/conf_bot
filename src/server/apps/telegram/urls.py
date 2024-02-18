from django.urls import path

from server.apps.telegram.views import BotWebHookView


urlpatterns = [
    path('webhook/', BotWebHookView.as_view()),
]
