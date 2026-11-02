from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Category, Product
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
