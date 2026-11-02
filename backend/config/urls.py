from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from config.throttles import LoginRateThrottle

urlpatterns = [
    # ========================================================
    # ADMIN
    # ========================================================
    path(
        "admin/",
        admin.site.urls,
    ),
    # ========================================================
    # AUTH
    # ========================================================
    path(
        "api/auth/token/",
        TokenObtainPairView.as_view(
            throttle_classes=[LoginRateThrottle],
        ),
        name="token_obtain_pair",
    ),
    path(
        "api/auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    # ========================================================
    # COMPANY
    # ========================================================
    path(
        "api/company/",
        include("company.urls"),
    ),
    # ========================================================
    # SERVICES
    # ========================================================
    path(
        "api/services/",
        include("services.urls"),
    ),
    # ========================================================
    # CONTENT
    # ========================================================
    path(
        "api/content/",
        include("content.urls"),
    ),
    # ========================================================
    # SHOP
    # ========================================================
    path(
        "api/shop/",
        include("shop.urls"),
    ),

    # ========================================================
    # TRANSLATIONS
    # ========================================================
    path(
        "api/translations/",
        include("translations.urls"),
    ),

    # ========================================================
    # EMPLOYEES
    # ========================================================
    path(
        "api/employees/",
        include("employees.urls"),
    ),
    # ========================================================
    # SERVICE REQUESTS
    # ========================================================
    path(
        "api/service-requests/",
        include("service_requests.urls"),
    ),

    # ========================================================
    # CAREER
    # ========================================================
    path(
        "api/career/",
        include("career.urls"),
    ),
]


# ============================================================
# MEDIA
# ============================================================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
