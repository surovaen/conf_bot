import asyncio
import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from telebot.types import Update

from server.apps.telegram.main import bot


class BotWebHookView(APIView):
    """Класс-вью обработки вебхука для бота."""

    def post(self, request, *args, **kwargs):
        """Принимает хук запросы."""
        json_string = request.body.decode('utf-8')
        data = json.loads(json_string)
        update = Update.de_json(data)
        asyncio.run(bot.process_new_updates([update]))

        return Response(status=status.HTTP_200_OK)
