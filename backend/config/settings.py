"""
Django settings for config project.

ООО «Изумруд Сервис»
Сантехнические услуги в Ташкенте.
"""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv


# ============================================================
# BASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Загружаем переменные окружения из backend/.env.
#
# override=True нужен для того, чтобы старые переменные,
# которые могли остаться в shell, не перекрывали актуальный .env.
load_dotenv(
    BASE_DIR / ".env",
    override=True,
)


# ============================================================
# ENV HELPERS
# ============================================================


def env_bool(name, default=False):
    """
    Безопасно читает boolean-переменную из environment.
    """
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def env_list(name, default=""):
    """
    Читает список значений из environment.

    Пример:

        HOSTS=a.com,b.com,localhost
    """
    return [
        item.strip()
        for item in os.getenv(name, default).split(",")
        if item.strip()
    ]


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "",
)

DEBUG = env_bool(
    "DJANGO_DEBUG",
    default=True,
)

ALLOWED_HOSTS = env_list(
    "DJANGO_ALLOWED_HOSTS",
    default="127.0.0.1,localhost",
)

# В production секретный ключ обязателен.
if not DEBUG and not SECRET_KEY:
    raise RuntimeError(
        "DJANGO_SECRET_KEY должен быть задан в production."
    )

# В production запрещаем development/insecure secret key.
if not DEBUG and SECRET_KEY.startswith("django-insecure-"):
    raise RuntimeError(
        "В production нельзя использовать insecure DJANGO_SECRET_KEY."
    )


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    'career',
    # --------------------------------------------------------
    # Django
    # --------------------------------------------------------
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # --------------------------------------------------------
    # Third-party
    # --------------------------------------------------------
    "corsheaders",
    "rest_framework",

    # JWT refresh-token blacklist.
    "rest_framework_simplejwt.token_blacklist",

    # --------------------------------------------------------
    # Local apps
    # --------------------------------------------------------
    "company",
    "services",
    "content",
    "shop",
    "service_requests",
    "telegram_bot",
    "telegram_clients",
    "employees",
    "translations",
    "service_calculator",
    "telegram_structure",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # CORS должен находиться как можно выше.
    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# CORS
# ============================================================

# Локальный frontend.
#
# В production обязательно заменить значениями
# настоящего frontend-домена через .env.
CORS_ALLOWED_ORIGINS = env_list(
    "CORS_ALLOWED_ORIGINS",
    default=(
        "http://localhost:5173,"
        "http://127.0.0.1:5173,"
        "http://localhost:5175,"
        "http://127.0.0.1:5175"
    ),
)

# JWT передаётся через Authorization header,
# поэтому credentials для CORS нам не нужны.
CORS_ALLOW_CREDENTIALS = False


# ============================================================
# CSRF
# ============================================================

CSRF_TRUSTED_ORIGINS = env_list(
    "CSRF_TRUSTED_ORIGINS",
    default=(
        "http://localhost:5173,"
        "http://127.0.0.1:5173,"
        "http://localhost:5175,"
        "http://127.0.0.1:5175"
    ),
)


# ============================================================
# TELEGRAM BOT
# ============================================================

# Секрет хранится только в .env.
YANDEX_GEOCODER_API_KEY = os.getenv(
    "YANDEX_GEOCODER_API_KEY",
    "",
)

TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN",
    "",
)

# ID рабочей Telegram-группы.
TELEGRAM_CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID",
    "",
)


# ============================================================
# YANDEX TRANSLATE
# ============================================================

# Секретный API-ключ Yandex Cloud хранится только в .env.
YANDEX_TRANSLATE_API_KEY = os.getenv(
    "YANDEX_TRANSLATE_API_KEY",
    "",
)

# ID каталога Yandex Cloud.
YANDEX_CLOUD_FOLDER_ID = os.getenv(
    "YANDEX_CLOUD_FOLDER_ID",
    "",
)


# ============================================================
# URLS / WSGI
# ============================================================

ROOT_URLCONF = "config.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"


# ============================================================
# DATABASE
# PostgreSQL
# ============================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",

        "NAME": os.getenv(
            "POSTGRES_DB",
            "emerald_service",
        ),

        "USER": os.getenv(
            "POSTGRES_USER",
            "emerald_service",
        ),

        "PASSWORD": os.getenv(
            "POSTGRES_PASSWORD",
            "emerald_service_dev",
        ),

        "HOST": os.getenv(
            "POSTGRES_HOST",
            "localhost",
        ),

        "PORT": os.getenv(
            "POSTGRES_PORT",
            "5432",
        ),

        # Держим соединение ограниченное время.
        "CONN_MAX_AGE": 60,

        "OPTIONS": {
            # Для локального PostgreSQL оставляем prefer.
            #
            # В production рекомендуется:
            #
            # POSTGRES_SSLMODE=require
            #
            "sslmode": os.getenv(
                "POSTGRES_SSLMODE",
                "prefer",
            ),
        },
    },
}


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"


# ============================================================
# MEDIA FILES
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# DJANGO REST FRAMEWORK
# ============================================================

REST_FRAMEWORK = {
    # --------------------------------------------------------
    # Authentication
    # --------------------------------------------------------
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),

    # --------------------------------------------------------
    # Permissions
    # --------------------------------------------------------
    # Fail-closed:
    # новые API endpoint'ы по умолчанию требуют авторизацию.
    #
    # Публичные endpoint'ы должны явно использовать AllowAny.
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),

    # --------------------------------------------------------
    # Throttling
    # --------------------------------------------------------
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),

    "DEFAULT_THROTTLE_RATES": {
        # Базовая защита анонимных запросов.
        "anon": "120/min",

        # Базовая защита авторизованных пользователей.
        "user": "300/min",

        # Публичное создание заявок.
        #
        # Дополнительно применяется непосредственно
        # ServiceRequestCreateAPIView.
        "service_request_create": "5/10m",
    },

    # --------------------------------------------------------
    # Pagination
    # --------------------------------------------------------
    "DEFAULT_PAGINATION_CLASS": (
        "service_requests.pagination.ServiceRequestPagination"
    ),
}


# ============================================================
# JWT
# ============================================================

SIMPLE_JWT = {
    # --------------------------------------------------------
    # Access token
    # --------------------------------------------------------
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=30,
    ),

    # --------------------------------------------------------
    # Refresh token
    # --------------------------------------------------------
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=7,
    ),

    # При refresh создаётся новый refresh token.
    "ROTATE_REFRESH_TOKENS": True,

    # Старый refresh token после rotation
    # помещается в blacklist.
    "BLACKLIST_AFTER_ROTATION": True,

    # --------------------------------------------------------
    # Authorization header
    # --------------------------------------------------------
    "AUTH_HEADER_TYPES": ("Bearer",),

    # --------------------------------------------------------
    # User identification
    # --------------------------------------------------------
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",

    # --------------------------------------------------------
    # Token behaviour
    # --------------------------------------------------------
    "UPDATE_LAST_LOGIN": False,
    "TOKEN_TYPE_CLAIM": "token_type",
}


# ============================================================
# PRODUCTION SECURITY
# ============================================================

if not DEBUG:

    # --------------------------------------------------------
    # HTTPS
    # --------------------------------------------------------

    SECURE_SSL_REDIRECT = True

    # Используется, если Django находится за reverse proxy.
    #
    # Nginx/Caddy должен передавать:
    #
    # X-Forwarded-Proto: https
    #
    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )

    # --------------------------------------------------------
    # Cookies
    # --------------------------------------------------------

    SESSION_COOKIE_SECURE = True

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"

    CSRF_COOKIE_SECURE = True

    # CSRF cookie должен быть доступен JavaScript,
    # если frontend использует стандартную CSRF-механику.
    CSRF_COOKIE_HTTPONLY = False

    CSRF_COOKIE_SAMESITE = "Lax"

    # --------------------------------------------------------
    # HSTS
    # --------------------------------------------------------

    SECURE_HSTS_SECONDS = 31536000

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_HSTS_PRELOAD = True

    # --------------------------------------------------------
    # Browser security
    # --------------------------------------------------------

    SECURE_CONTENT_TYPE_NOSNIFF = True

    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

    SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"

    X_FRAME_OPTIONS = "DENY"


else:

    # ========================================================
    # DEVELOPMENT
    # ========================================================

    SECURE_SSL_REDIRECT = False

    SESSION_COOKIE_SECURE = False

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"

    CSRF_COOKIE_SECURE = False

    CSRF_COOKIE_HTTPONLY = False

    CSRF_COOKIE_SAMESITE = "Lax"

    SECURE_HSTS_SECONDS = 0

    SECURE_HSTS_INCLUDE_SUBDOMAINS = False

    SECURE_HSTS_PRELOAD = False

    SECURE_CONTENT_TYPE_NOSNIFF = True

    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

    SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"

    X_FRAME_OPTIONS = "DENY"


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"