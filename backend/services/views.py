"""
API для публичного каталога услуг
ООО «Изумруд Сервис».
"""

from django.db.models import Avg, Count, Q

from rest_framework import generics, serializers
from rest_framework.permissions import AllowAny

from .models import ServiceCategory, Service
from .serializers import (
    ServiceCategorySerializer,
    ServiceSerializer,
)

# ============================================================
# HELPERS
# ============================================================


def active_service_categories_queryset():
    """
    Возвращает только активные категории услуг.
    """

    return ServiceCategory.objects.filter(
        is_active=True,
    )


def active_services_queryset():
    """
    Возвращает только активные услуги
    с рассчитанным рейтингом.

    В рейтинг попадают только выполненные заявки:

        status = completed
        rating IS NOT NULL
    """

    return (
        Service.objects.filter(
            is_active=True,
        )
        .select_related(
            "category",
        )
        .annotate(
            rating=Avg(
                "requests__rating",
                filter=Q(
                    requests__status="completed",
                    requests__rating__isnull=False,
                ),
            ),
            rating_count=Count(
                "requests",
                filter=Q(
                    requests__status="completed",
                    requests__rating__isnull=False,
                ),
            ),
        )
    )


def parse_boolean_query_param(
    request,
    parameter_name,
):
    """
    Безопасно разбирает boolean query-параметр.

    Разрешены только:

        true
        false

    Если параметр отсутствует:
        возвращается None.
    """

    value = request.query_params.get(
        parameter_name,
    )

    if value is None:
        return None

    value = value.strip().lower()

    if value not in {
        "true",
        "false",
    }:
        raise serializers.ValidationError(
            {parameter_name: ("Параметр должен быть true или false.")}
        )

    return value == "true"


# ============================================================
# PUBLIC CATEGORY LIST
# ============================================================


class ServiceCategoryListAPIView(generics.ListAPIView):
    """
    Публичный список активных категорий услуг.

    Авторизация не требуется.

    Поддерживает:

        ?search=ремонт

    В поиск входят:

        name
        description
    """

    serializer_class = ServiceCategorySerializer

    permission_classes = [
        AllowAny,
    ]

    def get_queryset(self):
        queryset = active_service_categories_queryset()

        # ====================================================
        # FILTER: SEARCH
        # ====================================================

        search = self.request.query_params.get(
            "search",
        )

        if search:
            search = search.strip()

            if search:
                queryset = queryset.filter(
                    Q(
                        name__icontains=search,
                    )
                    | Q(
                        description__icontains=search,
                    )
                )

        # ====================================================
        # ORDERING
        # ====================================================

        return queryset.order_by(
            "sort_order",
            "name",
        )


# ============================================================
# PUBLIC CATEGORY DETAIL
# ============================================================


class ServiceCategoryDetailAPIView(generics.RetrieveAPIView):
    """
    Публичное получение одной активной категории.

    Авторизация не требуется.

    Поиск выполняется по slug.
    """

    serializer_class = ServiceCategorySerializer

    permission_classes = [
        AllowAny,
    ]

    lookup_field = "slug"

    def get_queryset(self):
        return active_service_categories_queryset()


# ============================================================
# PUBLIC SERVICE LIST
# ============================================================


class ServiceListAPIView(generics.ListAPIView):
    """
    Публичный список активных услуг.

    Авторизация не требуется.

    Поддерживаемые фильтры:

        ?category=1

        ?category=montazh-santehniki

        ?popular=true
        ?popular=false

        ?homepage=true
        ?homepage=false

        ?search=труб
    """

    serializer_class = ServiceSerializer

    permission_classes = [
        AllowAny,
    ]

    def get_queryset(self):
        queryset = active_services_queryset()

        # ====================================================
        # FILTER: CATEGORY
        # ====================================================

        category = self.request.query_params.get(
            "category",
        )

        if category:
            category = category.strip()

            if category:
                if category.isdigit():
                    queryset = queryset.filter(
                        category_id=int(category),
                    )
                else:
                    queryset = queryset.filter(
                        category__slug=category,
                    )

        # ====================================================
        # FILTER: POPULAR
        # ====================================================

        popular = parse_boolean_query_param(
            self.request,
            "popular",
        )

        if popular is not None:
            queryset = queryset.filter(
                is_popular=popular,
            )

        # ====================================================
        # FILTER: HOMEPAGE
        # ====================================================

        homepage = parse_boolean_query_param(
            self.request,
            "homepage",
        )

        if homepage is not None:
            queryset = queryset.filter(
                show_on_homepage=homepage,
            )

        # ====================================================
        # FILTER: SEARCH
        # ====================================================

        search = self.request.query_params.get(
            "search",
        )

        if search:
            search = search.strip()

            if search:
                queryset = queryset.filter(
                    Q(
                        name__icontains=search,
                    )
                    | Q(
                        short_description__icontains=search,
                    )
                    | Q(
                        description__icontains=search,
                    )
                )

        # ====================================================
        # ORDERING
        # ====================================================

        return queryset.order_by(
            "sort_order",
            "name",
        )


# ============================================================
# PUBLIC SERVICE DETAIL
# ============================================================


class ServiceDetailAPIView(generics.RetrieveAPIView):
    """
    Публичное получение одной активной услуги.

    Авторизация не требуется.

    Поиск выполняется по slug.

    Вместе с услугой возвращаются:

        rating
        rating_count
    """

    serializer_class = ServiceSerializer

    permission_classes = [
        AllowAny,
    ]

    lookup_field = "slug"

    def get_queryset(self):
        return active_services_queryset()
