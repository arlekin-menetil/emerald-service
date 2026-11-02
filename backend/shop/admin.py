from django.contrib import admin

from .models import Category, Product, ProductImage


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
