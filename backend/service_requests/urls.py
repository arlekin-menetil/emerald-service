"""
URL-маршруты API заявок
ООО «Изумруд Сервис».
"""

from django.urls import path

from .views import (
    GeocodeAPIView,
    ServiceRequestCreateAPIView,
    ServiceRequestDetailAPIView,
    ServiceRequestListAPIView,
    ServiceRequestRatingAPIView,
    ServiceRequestStatsAPIView,
    ServiceRatingAPIView,
    ServiceRequestStatusAPIView,
)

urlpatterns = [
    # ========================================================
    # PUBLIC
    # ========================================================
    # Создание заявки клиентом.
    #
    # POST /api/service-requests/
    #
    # Авторизация не требуется.
    path(
        "",
        ServiceRequestCreateAPIView.as_view(),
        name="service-request-create",
    ),
    # ========================================================
    # PUBLIC GEOCODING
    # ========================================================
    # Преобразование адреса клиента в координаты.
    #
    # POST /api/service-requests/geocode/
    #
    # Авторизация не требуется.
    path(
        "geocode/",
        GeocodeAPIView.as_view(),
        name="service-request-geocode",
    ),
    # ========================================================
    # ADMIN LIST
    # ========================================================
    # Список заявок.
    #
    # GET /api/service-requests/list/
    #
    # Требуется JWT + права администратора.
    path(
        "list/",
        ServiceRequestListAPIView.as_view(),
        name="service-request-list",
    ),
    # ========================================================
    # ADMIN STATS
    # ========================================================
    # Статистика заявок.
    #
    # GET /api/service-requests/stats/
    #
    # Требуется JWT + права администратора.
    path(
        "stats/",
        ServiceRequestStatsAPIView.as_view(),
        name="service-request-stats",
    ),
    path(
        "ratings/",
        ServiceRatingAPIView.as_view(),
        name="service-rating-stats",
    ),
    # ========================================================
    # PUBLIC RATING
    # ========================================================
    # Оценка выполненной заявки.
    #
    # POST /api/service-requests/<rating_token>/rate/
    #
    # Авторизация не требуется.
    path(
        "<uuid:rating_token>/rate/",
        ServiceRequestRatingAPIView.as_view(),
        name="service-request-rate",
    ),
    # ========================================================
    # ADMIN STATUS
    # ========================================================
    # Изменение статуса заявки.
    #
    # PATCH /api/service-requests/<pk>/status/
    #
    # Требуется JWT + права администратора.
    path(
        "<int:pk>/status/",
        ServiceRequestStatusAPIView.as_view(),
        name="service-request-status",
    ),
    # ========================================================
    # ADMIN DETAIL
    # ========================================================
    # Получение одной заявки.
    #
    # GET /api/service-requests/<pk>/
    #
    # Требуется JWT + права администратора.
    path(
        "<int:pk>/",
        ServiceRequestDetailAPIView.as_view(),
        name="service-request-detail",
    ),
]
