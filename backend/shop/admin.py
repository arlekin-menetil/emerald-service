from django.contrib import admin

from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import Category, Product, ProductImage, UzumClick


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 4
    fields = (
        "image",
        "sort_order",
    )
    ordering = (
        "sort_order",
        "id",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "sort_order",
        "is_active",
        "image",
    )
    list_filter = (
        "is_active",
    )
    search_fields = (
        "name",
        "name_uz",
        "name_en",
        "name_zh",
        "slug",
    )
    ordering = (
        "sort_order",
        "name",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "sku",
        "price",
        "total_uzum_clicks",
        "unique_uzum_visitors",
        "stock_quantity",
        "is_available",
        "is_featured",
    )
    list_filter = (
        "category",
        "is_available",
        "is_featured",
    )
    search_fields = (
        "name",
        "name_uz",
        "name_en",
        "name_zh",
        "sku",
        "slug",
        "uzum_url",
    )
    ordering = (
        "sort_order",
        "-created_at",
    )
    prepopulated_fields = {
        "slug": ("name",),
    }
    inlines = (
        ProductImageInline,
    )


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        since = timezone.now() - timedelta(days=30)
        return queryset.annotate(
            uzum_total=Count("uzum_clicks"),
            uzum_unique_30=Count(
                "uzum_clicks__visitor_id",
                filter=Q(uzum_clicks__clicked_at__gte=since),
                distinct=True,
            ),
        )

    @admin.display(description="Всего переходов", ordering="uzum_total")
    def total_uzum_clicks(self, obj):
        return obj.uzum_total

    @admin.display(description="Уникальные за 30 дней", ordering="uzum_unique_30")
    def unique_uzum_visitors(self, obj):
        return obj.uzum_unique_30
