"""
URL-маршруты API информации о компании
ООО «Изумруд Сервис».
"""

from django.urls import path

from .views import CompanyListAPIView

urlpatterns = [
    # ========================================================
    # PUBLIC COMPANY
    # ========================================================
    # Получение активной информации о компании.
    #
    # GET /api/company/
    #
    # Авторизация не требуется.
    path(
        "",
        CompanyListAPIView.as_view(),
        name="company-list",
    ),
]
