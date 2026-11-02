"""
API для информации о компании
ООО «Изумруд Сервис».
"""

from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Company
from .serializers import CompanySerializer

# ============================================================
# PUBLIC COMPANY
# ============================================================


class CompanyListAPIView(generics.ListAPIView):
    """
    Публичный список активных компаний.

    Авторизация не требуется.

    Обычно на сайте используется одна основная компания,
    но API поддерживает несколько активных записей.

    Возвращаются только компании,
    у которых is_active=True.
    """

    serializer_class = CompanySerializer

    permission_classes = [
        AllowAny,
    ]

    def get_queryset(self):
        """
        Возвращает только активные компании.

        Сначала показываются недавно изменённые записи.
        """

        return Company.objects.filter(
            is_active=True,
        ).order_by(
            "-updated_at",
        )
