from django.urls import path

from .views import CategoryListAPIView, ProductListAPIView, redirect_to_uzum


urlpatterns = [
    path("categories/", CategoryListAPIView.as_view(), name="shop-categories"),
    path("products/", ProductListAPIView.as_view(), name="shop-products"),
    path("products/<int:pk>/uzum/", redirect_to_uzum, name="shop-uzum-redirect"),
]
