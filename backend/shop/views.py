import uuid

from datetime import timedelta
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Category, Product, UzumClick
from .serializers import CategorySerializer, ProductSerializer


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = (
            Product.objects
            .filter(
                is_available=True,
                category__is_active=True,
            )
            .select_related("category")
        )

        category = self.request.query_params.get("category")

        if category:
            queryset = queryset.filter(
                category__slug=category
            )

        return queryset


def redirect_to_uzum(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if not product.uzum_url:
        raise Http404("Ссылка Uzum для товара не задана")

    visitor_id = request.COOKIES.get("uzum_visitor_id")
    set_cookie = False

    try:
        visitor_id = str(uuid.UUID(visitor_id))
    except (ValueError, TypeError, AttributeError):
        visitor_id = str(uuid.uuid4())
        set_cookie = True

    UzumClick.objects.create(
        product=product,
        visitor_id=visitor_id,
    )

    response = HttpResponseRedirect(product.uzum_url)

    if set_cookie:
        response.set_cookie(
            "uzum_visitor_id",
            visitor_id,
            max_age=30 * 24 * 60 * 60,
            httponly=True,
            secure=request.is_secure(),
            samesite="Lax",
        )

    return response
