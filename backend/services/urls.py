"""
URL-маршруты публичного API услуг
ООО «Изумруд Сервис».
"""

from django.urls import path

from .views import (
    ServiceCategoryDetailAPIView,
    ServiceCategoryListAPIView,
    ServiceDetailAPIView,
    ServiceListAPIView,
)

urlpatterns = [
    # ========================================================
    # CATEGORIES
    # ========================================================
    # Список активных категорий.
    #
    # GET /api/services/categories/
    #
    # Авторизация не требуется.
    path(
        "categories/",
        ServiceCategoryListAPIView.as_view(),
        name="service-category-list",
    ),
    # Одна активная категория по slug.
    #
    # GET /api/services/categories/<slug>/
    #
    # Авторизация не требуется.
    path(
        "categories/<slug:slug>/",
        ServiceCategoryDetailAPIView.as_view(),
        name="service-category-detail",
    ),
    # ========================================================
    # SERVICES
    # ========================================================
    # Список активных услуг.
    #
    # GET /api/services/
    #
    # Авторизация не требуется.
    path(
        "",
        ServiceListAPIView.as_view(),
        name="service-list",
    ),
    # Одна активная услуга по slug.
    #
    # GET /api/services/<slug>/
    #
    # Авторизация не требуется.
    path(
        "<slug:slug>/",
        ServiceDetailAPIView.as_view(),
        name="service-detail",
    ),
]
