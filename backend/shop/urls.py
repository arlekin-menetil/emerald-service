from django.urls import path

from .views import CategoryListAPIView, ProductListAPIView


urlpatterns = [
    path("categories/", CategoryListAPIView.as_view(), name="shop-categories"),
    path("products/", ProductListAPIView.as_view(), name="shop-products"),
]
