"""
API для работы с заявками ООО «Изумруд Сервис».
"""

import logging
import requests
from datetime import datetime

from django.conf import settings
from django.db import transaction
from django.db.models import Avg, Count, Q
from django.utils import timezone

from rest_framework import generics, serializers, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from telegram_bot.notifications import notify_new_service_request
from telegram_bot.services import TelegramBotError

from .models import ServiceRequest
from .pagination import ServiceRequestPagination
from .serializers import (
    ServiceRequestAdminSerializer,
    ServiceRequestCreateSerializer,
    ServiceRequestRatingSerializer,
    ServiceRequestStatusSerializer,
)

logger = logging.getLogger(__name__)


# ============================================================
# PUBLIC GEOCODING
# ============================================================


class GeocodeAPIView(APIView):
    """
    Определение координат по текстовому адресу
    через Yandex Geocoder.

    POST:
        {
            "address": "Ташкент, улица Мукими, 15"
        }

    RESPONSE:
        {
            "address": "...",
            "latitude": 41.285,
            "longitude": 69.240,
            "found_address": "..."
        }
    """

    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        address = str(
            request.data.get("address", "")
        ).strip()

        if len(address) < 5:
            return Response(
                {
                    "detail": "Укажите корректный адрес."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        api_key = getattr(
            settings,
            "YANDEX_GEOCODER_API_KEY",
            "",
        )

        if not api_key:
            return Response(
                {
                    "detail": (
                        "Yandex Geocoder API key "
                        "не настроен."
                    )
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        try:
            response = requests.get(
                "https://geocode-maps.yandex.ru/1.x/",
                params={
                    "apikey": api_key,
                    "geocode": address,
                    "format": "json",
                    "lang": "ru_RU",
                    "results": 1,
                },
                timeout=10,
            )

            response.raise_for_status()

            data = response.json()

            members = (
                data
                .get("response", {})
                .get("GeoObjectCollection", {})
                .get("featureMember", [])
            )

            if not members:
                return Response(
                    {
                        "detail": "Адрес не найден."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            geo_object = members[0].get(
                "GeoObject",
                {},
            )

            point = geo_object.get(
                "Point",
                {},
            )

            pos = point.get(
                "pos",
                "",
            )

            if not pos:
                return Response(
                    {
                        "detail": (
                            "Координаты для адреса "
                            "не найдены."
                        )
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            longitude, latitude = pos.split()

            geocoder_metadata = (
                geo_object
                .get("metaDataProperty", {})
                .get("GeocoderMetaData", {})
            )

            found_address = geocoder_metadata.get(
                "text",
                address,
            )

            return Response(
                {
                    "address": address,
                    "latitude": float(latitude),
                    "longitude": float(longitude),
                    "found_address": found_address,
                },
                status=status.HTTP_200_OK,
            )

        except requests.RequestException as exc:
            logger.error(
                "Yandex Geocoder request error: %s",
                exc,
            )

            return Response(
                {
                    "detail": (
                        "Ошибка при обращении "
                        "к Yandex Geocoder."
                    )
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        except (
            ValueError,
            KeyError,
            TypeError,
        ) as exc:
            logger.error(
                "Yandex Geocoder response error: %s",
                exc,
            )

            return Response(
                {
                    "detail": (
                        "Некорректный ответ "
                        "от Yandex Geocoder."
                    )
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )


# ============================================================
# PUBLIC CREATE THROTTLE
# ============================================================


class ServiceRequestCreateThrottle(AnonRateThrottle):
    """
    Ограничение публичного создания заявок.

    Максимум:
        5 запросов за 10 минут
        с одного IP-адреса.

    Используется только для публичного endpoint создания заявки.

    Стандартный DRF понимает форматы:
        5/s
        5/m
        5/h
        5/d

    Поэтому здесь переопределяем parse_rate(),
    чтобы поддерживать:
        5/10m
    """

    scope = "service_request_create"

    rate = "5/10m"

    def parse_rate(self, rate):
        """
        Разбирает rate формата:

            5/s
            5/m
            5/h
            5/d

        а также нашего расширенного формата:

            5/10m
            5/30m
            10/2h

        Возвращает:

            (количество запросов, длительность в секундах)
        """

        if rate is None:
            return None, None

        num_requests, period = rate.split("/", 1)

        num_requests = int(num_requests)

        # ----------------------------------------------------
        # Стандартные периоды DRF
        # ----------------------------------------------------

        if len(period) == 1:
            duration = {
                "s": 1,
                "m": 60,
                "h": 3600,
                "d": 86400,
            }[period]

            return num_requests, duration

        # ----------------------------------------------------
        # Расширенный формат:
        #
        # 10m
        # 30m
        # 2h
        # ----------------------------------------------------

        unit = period[-1]
        amount = int(period[:-1])

        duration_multipliers = {
            "s": 1,
            "m": 60,
            "h": 3600,
            "d": 86400,
        }

        if unit not in duration_multipliers:
            raise ValueError(f"Неподдерживаемая единица времени в rate: {period}")

        duration = amount * duration_multipliers[unit]

        return num_requests, duration


# ============================================================
# PUBLIC CREATE
# ============================================================


class ServiceRequestCreateAPIView(generics.CreateAPIView):
    """
    Публичное создание заявки клиентом.

    Доступно без JWT.

    Клиент передаёт:

        name
        phone
        address
        service
        scheduled_at
        comment

    После создания заявки отправляется уведомление
    в рабочую Telegram-группу сотрудников.

    Ошибка Telegram не отменяет создание заявки.

    Ограничение:
        максимум 5 запросов за 10 минут с одного IP.
    """

    queryset = ServiceRequest.objects.all()

    serializer_class = ServiceRequestCreateSerializer

    permission_classes = [
        AllowAny,
    ]

    throttle_classes = [
        ServiceRequestCreateThrottle,
    ]

    def perform_create(self, serializer):
        """
        Создаёт заявку и отправляет уведомление сотрудникам.
        """

        service_request = serializer.save()

        try:
            notify_new_service_request(service_request)

        except TelegramBotError as exc:
            logger.error(
                "Telegram notification error for request #%s: %s",
                service_request.pk,
                exc,
            )

        except Exception:
            logger.exception(
                "Unexpected Telegram notification error " "for request #%s",
                service_request.pk,
            )


# ============================================================
# ADMIN LIST
# ============================================================


class ServiceRequestListAPIView(generics.ListAPIView):
    """
    Список заявок для административной панели.

    Доступ:
        только администратор.

    Поддерживаемые фильтры:

        ?status=new
        ?status=in_progress
        ?status=completed
        ?status=cancelled

        ?service=4

        ?search=Нигора
        ?search=998936206065
        ?search=Ташкент

        ?date_from=2026-09-01
        ?date_to=2026-09-03

        ?scheduled_date_from=2026-09-01
        ?scheduled_date_to=2026-09-03

        ?page=1
        ?page_size=20

    Фильтры можно комбинировать.
    """

    serializer_class = ServiceRequestAdminSerializer

    permission_classes = [
        IsAdminUser,
    ]

    pagination_class = ServiceRequestPagination

    def get_queryset(self):
        queryset = (
            ServiceRequest.objects.select_related("service")
            .prefetch_related("employees")
            .all()
        )

        request_status = self.request.query_params.get("status")
        service_id = self.request.query_params.get("service")
        search = self.request.query_params.get("search")

        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")

        scheduled_date_from = self.request.query_params.get("scheduled_date_from")

        scheduled_date_to = self.request.query_params.get("scheduled_date_to")

        # ====================================================
        # FILTER: STATUS
        # ====================================================

        if request_status:
            request_status = request_status.strip().lower()

            valid_statuses = {choice[0] for choice in ServiceRequest.STATUS_CHOICES}

            if request_status not in valid_statuses:
                raise serializers.ValidationError(
                    {
                        "status": (
                            "Недопустимый статус. "
                            "Используйте: new, in_progress, "
                            "completed или cancelled."
                        )
                    }
                )

            queryset = queryset.filter(
                status=request_status,
            )

        # ====================================================
        # FILTER: SERVICE
        # ====================================================

        if service_id:
            service_id = service_id.strip()

            if not service_id.isdigit():
                raise serializers.ValidationError(
                    {"service": ("ID услуги должен быть " "целым числом.")}
                )

            queryset = queryset.filter(
                service_id=int(service_id),
            )

        # ====================================================
        # FILTER: SEARCH
        # ====================================================

        if search:
            search = search.strip()

            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search)
                    | Q(phone__icontains=search)
                    | Q(address__icontains=search)
                    | Q(comment__icontains=search)
                )

        # ====================================================
        # CREATED DATE RANGE
        # ====================================================

        parsed_date_from = None
        parsed_date_to = None

        if date_from:
            date_from = date_from.strip()

            try:
                parsed_date_from = datetime.strptime(
                    date_from,
                    "%Y-%m-%d",
                ).date()

            except ValueError as exc:
                raise serializers.ValidationError(
                    {"date_from": ("Дата должна быть " "в формате YYYY-MM-DD.")}
                ) from exc

            queryset = queryset.filter(
                created_at__date__gte=parsed_date_from,
            )

        if date_to:
            date_to = date_to.strip()

            try:
                parsed_date_to = datetime.strptime(
                    date_to,
                    "%Y-%m-%d",
                ).date()

            except ValueError as exc:
                raise serializers.ValidationError(
                    {"date_to": ("Дата должна быть " "в формате YYYY-MM-DD.")}
                ) from exc

            queryset = queryset.filter(
                created_at__date__lte=parsed_date_to,
            )

        if (
            parsed_date_from is not None
            and parsed_date_to is not None
            and parsed_date_from > parsed_date_to
        ):
            raise serializers.ValidationError(
                {"date": ("Дата date_from не может " "быть позже date_to.")}
            )

        # ====================================================
        # SCHEDULED DATE RANGE
        # ====================================================

        parsed_scheduled_date_from = None
        parsed_scheduled_date_to = None

        if scheduled_date_from:
            scheduled_date_from = scheduled_date_from.strip()

            try:
                parsed_scheduled_date_from = datetime.strptime(
                    scheduled_date_from,
                    "%Y-%m-%d",
                ).date()

            except ValueError as exc:
                raise serializers.ValidationError(
                    {
                        "scheduled_date_from": (
                            "Дата должна быть " "в формате YYYY-MM-DD."
                        )
                    }
                ) from exc

            queryset = queryset.filter(
                scheduled_at__date__gte=parsed_scheduled_date_from,
            )

        if scheduled_date_to:
            scheduled_date_to = scheduled_date_to.strip()

            try:
                parsed_scheduled_date_to = datetime.strptime(
                    scheduled_date_to,
                    "%Y-%m-%d",
                ).date()

            except ValueError as exc:
                raise serializers.ValidationError(
                    {"scheduled_date_to": ("Дата должна быть " "в формате YYYY-MM-DD.")}
                ) from exc

            queryset = queryset.filter(
                scheduled_at__date__lte=parsed_scheduled_date_to,
            )

        if (
            parsed_scheduled_date_from is not None
            and parsed_scheduled_date_to is not None
            and parsed_scheduled_date_from > parsed_scheduled_date_to
        ):
            raise serializers.ValidationError(
                {
                    "scheduled_date": (
                        "Дата scheduled_date_from "
                        "не может быть позже "
                        "scheduled_date_to."
                    )
                }
            )

        return queryset


# ============================================================
# ADMIN STATS
# ============================================================


class ServiceRequestStatsAPIView(APIView):
    """
    Статистика заявок для административной панели.

    Доступ:
        только администратор.

    Возвращает:

        total
        new
        in_progress
        completed
        cancelled
        rated
        average_rating
    """

    permission_classes = [
        IsAdminUser,
    ]

    def get(self, request):
        stats = ServiceRequest.objects.aggregate(
            total=Count("id"),
            new=Count(
                "id",
                filter=Q(
                    status=ServiceRequest.STATUS_NEW,
                ),
            ),
            in_progress=Count(
                "id",
                filter=Q(
                    status=ServiceRequest.STATUS_IN_PROGRESS,
                ),
            ),
            completed=Count(
                "id",
                filter=Q(
                    status=ServiceRequest.STATUS_COMPLETED,
                ),
            ),
            cancelled=Count(
                "id",
                filter=Q(
                    status=ServiceRequest.STATUS_CANCELLED,
                ),
            ),
            rated=Count(
                "id",
                filter=Q(
                    rating__isnull=False,
                ),
            ),
            average_rating=Avg(
                "rating",
            ),
        )

        average_rating = stats["average_rating"]

        if average_rating is not None:
            average_rating = round(
                float(average_rating),
                2,
            )

        return Response(
            {
                "total": stats["total"],
                "new": stats["new"],
                "in_progress": stats["in_progress"],
                "completed": stats["completed"],
                "cancelled": stats["cancelled"],
                "rated": stats["rated"],
                "average_rating": average_rating,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# ADMIN DETAIL
# ============================================================


class ServiceRequestDetailAPIView(generics.RetrieveAPIView):
    """
    Получение одной заявки для административной панели.

    Доступ:
        только администратор.
    """

    queryset = (
        ServiceRequest.objects.select_related("service")
        .prefetch_related("employees")
        .all()
    )

    serializer_class = ServiceRequestAdminSerializer

    permission_classes = [
        IsAdminUser,
    ]


# ============================================================
# ADMIN STATUS
# ============================================================


class ServiceRequestStatusAPIView(APIView):
    """
    Изменение статуса заявки.

    Доступ:
        только администратор.

    Разрешённые переходы:

        new
            ├──> new
            ├──> in_progress
            └──> cancelled

        in_progress
            ├──> in_progress
            ├──> completed
            └──> cancelled

        completed
            └──> completed

        cancelled
            └──> cancelled
    """

    permission_classes = [
        IsAdminUser,
    ]

    ALLOWED_TRANSITIONS = {
        ServiceRequest.STATUS_NEW: {
            ServiceRequest.STATUS_NEW,
            ServiceRequest.STATUS_IN_PROGRESS,
            ServiceRequest.STATUS_CANCELLED,
        },
        ServiceRequest.STATUS_IN_PROGRESS: {
            ServiceRequest.STATUS_IN_PROGRESS,
            ServiceRequest.STATUS_COMPLETED,
            ServiceRequest.STATUS_CANCELLED,
        },
        ServiceRequest.STATUS_COMPLETED: {
            ServiceRequest.STATUS_COMPLETED,
        },
        ServiceRequest.STATUS_CANCELLED: {
            ServiceRequest.STATUS_CANCELLED,
        },
    }

    def patch(self, request, pk):
        # ====================================================
        # VALIDATE INPUT
        # ====================================================

        serializer = ServiceRequestStatusSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        new_status = serializer.validated_data["status"]

        # ====================================================
        # LOCK REQUEST
        # ====================================================

        try:
            with transaction.atomic():

                service_request = ServiceRequest.objects.select_for_update().get(pk=pk)

                current_status = service_request.status

                allowed_statuses = self.ALLOWED_TRANSITIONS.get(
                    current_status,
                    set(),
                )

                # ============================================
                # CHECK TRANSITION
                # ============================================

                if new_status not in allowed_statuses:
                    current_status_display = service_request.get_status_display()

                    new_status_display = dict(ServiceRequest.STATUS_CHOICES).get(
                        new_status,
                        new_status,
                    )

                    return Response(
                        {
                            "detail": (
                                "Недопустимый переход статуса: "
                                f"«{current_status_display}» → "
                                f"«{new_status_display}»."
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # ============================================
                # SAME STATUS
                # ============================================

                if new_status == current_status:
                    pass

                # ============================================
                # COMPLETED
                # ============================================

                elif new_status == ServiceRequest.STATUS_COMPLETED:

                    service_request.status = ServiceRequest.STATUS_COMPLETED

                    if service_request.completed_at is None:
                        service_request.completed_at = timezone.now()

                    service_request.save(
                        update_fields=[
                            "status",
                            "completed_at",
                            "updated_at",
                        ]
                    )

                # ============================================
                # CANCELLED
                # ============================================

                elif new_status == ServiceRequest.STATUS_CANCELLED:

                    service_request.status = ServiceRequest.STATUS_CANCELLED

                    service_request.completed_at = None

                    service_request.save(
                        update_fields=[
                            "status",
                            "completed_at",
                            "updated_at",
                        ]
                    )

                # ============================================
                # NEW / IN PROGRESS
                # ============================================

                else:

                    service_request.status = new_status

                    service_request.completed_at = None

                    service_request.save(
                        update_fields=[
                            "status",
                            "completed_at",
                            "updated_at",
                        ]
                    )

        except ServiceRequest.DoesNotExist:
            return Response(
                {
                    "detail": "Заявка не найдена.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # ====================================================
        # RELOAD
        # ====================================================

        service_request = (
            ServiceRequest.objects.select_related("service")
            .prefetch_related("employees")
            .get(
                pk=service_request.pk,
            )
        )

        # ====================================================
        # RESPONSE
        # ====================================================

        return Response(
            ServiceRequestAdminSerializer(
                service_request,
            ).data,
            status=status.HTTP_200_OK,
        )


# ============================================================
# PUBLIC RATING
# ============================================================


class ServiceRequestRatingAPIView(APIView):
    """
    Публичная оценка выполненной заявки.

    Доступ:
        без JWT.

    Заявка определяется по уникальному UUID rating_token.

    Условия:

        1. Заявка должна существовать.
        2. Заявка должна иметь статус completed.
        3. У заявки ещё не должно быть оценки.
        4. Оценка должна находиться в диапазоне 1-5.

    Для защиты от race condition используется
    select_for_update().
    """

    permission_classes = [
        AllowAny,
    ]

    def post(
        self,
        request,
        rating_token,
    ):
        # ====================================================
        # VALIDATE RATING
        # ====================================================

        serializer = ServiceRequestRatingSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        rating = serializer.validated_data["rating"]

        # ====================================================
        # LOCK REQUEST
        # ====================================================

        try:
            with transaction.atomic():

                service_request = (
                    ServiceRequest.objects.select_for_update()
                    .filter(
                        rating_token=rating_token,
                    )
                    .first()
                )

                # ============================================
                # NOT FOUND
                # ============================================

                if service_request is None:
                    return Response(
                        {
                            "detail": "Заявка не найдена.",
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )

                # ============================================
                # CHECK COMPLETED
                # ============================================

                if service_request.status != ServiceRequest.STATUS_COMPLETED:
                    return Response(
                        {"detail": ("Оценить можно только " "выполненную заявку.")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # ============================================
                # CHECK ALREADY RATED
                # ============================================

                if service_request.rating is not None:
                    return Response(
                        {"detail": ("Эта заявка уже была оценена.")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # ============================================
                # SAVE RATING
                # ============================================

                service_request.rating = rating

                service_request.save(
                    update_fields=[
                        "rating",
                        "updated_at",
                    ]
                )

        except Exception:
            # Не записываем полный rating_token в лог.
            logger.exception(
                "Unexpected error while rating " "service request #%s",
                getattr(
                    service_request,
                    "pk",
                    "unknown",
                ),
            )
            raise

        # ====================================================
        # PUBLIC RESPONSE
        # ====================================================

        return Response(
            {
                "detail": "Спасибо за вашу оценку!",
                "request_id": service_request.pk,
                "rating": service_request.rating,
            },
            status=status.HTTP_200_OK,
        )

# ==========================================================
# PUBLIC SERVICE RATINGS
# ==========================================================


class ServiceRatingAPIView(APIView):
    """
    Публичная статистика рейтинга услуг.

    Используются только реальные оценки:
    - заявка должна быть завершена;
    - rating должен быть установлен;
    - заявка должна быть связана с услугой.
    """

    permission_classes = []

    def get(self, request):
        language = request.query_params.get("lang", "ru").strip().lower()

        if language not in {"ru", "uz", "en", "zh"}:
            language = "ru"

        service_name_fields = {
            "ru": "service__name",
            "uz": "service__name_uz",
            "en": "service__name_en",
            "zh": "service__name_zh",
        }

        service_name_field = service_name_fields[language]

        rated_requests = (
            ServiceRequest.objects
            .filter(
                status=ServiceRequest.STATUS_COMPLETED,
                rating__isnull=False,
                service__isnull=False,
            )
            .select_related("service")
        )

        overall = rated_requests.aggregate(
            average_rating=Avg("rating"),
            total_ratings=Count("id"),
        )

        services = (
            rated_requests
            .values(
                "service_id",
                "service__name",
                "service__name_uz",
                "service__name_en",
                "service__name_zh",
                "service__image",
            )
            .annotate(
                average_rating=Avg("rating"),
                total_ratings=Count("id"),
            )
            .order_by(
                "-average_rating",
                service_name_field,
            )
        )

        result = []

        for item in services:
            image = item["service__image"]

            image_url = None

            if image:
                image_url = request.build_absolute_uri(
                    f"/media/{image}"
                )

            localized_name = item[service_name_field]

            if not localized_name:
                localized_name = item["service__name"]

            result.append(
                {
                    "id": item["service_id"],
                    "name": localized_name,
                    "image": image_url,
                    "average_rating": round(
                        float(item["average_rating"]),
                        2,
                    ),
                    "total_ratings": item["total_ratings"],
                }
            )

        return Response(
            {
                "average_rating": (
                    round(
                        float(overall["average_rating"]),
                        2,
                    )
                    if overall["average_rating"] is not None
                    else None
                ),
                "total_ratings": overall["total_ratings"],
                "services": result,
            },
            status=status.HTTP_200_OK,
        )
