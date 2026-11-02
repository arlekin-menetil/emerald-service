import logging

from rest_framework import generics
from rest_framework.permissions import AllowAny

from telegram_bot.notifications import notify_new_vacancy_application
from telegram_bot.services import TelegramBotError

from .models import VacancyApplication
from .serializers import VacancyApplicationCreateSerializer

logger = logging.getLogger(__name__)


class VacancyApplicationCreateAPIView(generics.CreateAPIView):
    queryset = VacancyApplication.objects.all()
    serializer_class = VacancyApplicationCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        application = serializer.save()

        try:
            notify_new_vacancy_application(application)
            logger.info(
                "Vacancy application #%s sent to Telegram group.",
                application.id,
            )
        except TelegramBotError as exc:
            logger.error(
                "Failed to send vacancy application #%s to Telegram: %s",
                application.id,
                exc,
                exc_info=True,
            )
