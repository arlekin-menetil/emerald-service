from django.contrib import admin

from .models import ServiceCategory, Service


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "sort_order",
        "updated_at",
    )

    list_filter = ("is_active",)

    search_fields = (
        "name",
        "name_uz",
        "name_en",
        "name_zh",
        "description",
        "description_uz",
        "description_en",
        "description_zh",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    ordering = (
        "sort_order",
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                    "image",
                    "is_active",
                    "sort_order",
                )
            },
        ),
        (
            "🇺🇿 O'zbekcha",
            {
                "fields": (
                    "name_uz",
                    "description_uz",
                )
            },
        ),
        (
            "🇬🇧 English",
            {
                "fields": (
                    "name_en",
                    "description_en",
                )
            },
        ),
        (
            "🇨🇳 中文",
            {
                "fields": (
                    "name_zh",
                    "description_zh",
                )
            },
        ),
        (
            "Служебная информация",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price_from",
        "is_popular",
        "show_on_homepage",
        "is_active",
        "sort_order",
        "updated_at",
    )

    list_filter = (
        "category",
        "is_popular",
        "show_on_homepage",
        "is_active",
    )

    search_fields = (
        "name",
        "name_uz",
        "name_en",
        "name_zh",
        "short_description",
        "short_description_uz",
        "short_description_en",
        "short_description_zh",
        "description",
        "description_uz",
        "description_en",
        "description_zh",
        "category__name",
        "category__name_uz",
        "category__name_en",
        "category__name_zh",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    ordering = (
        "sort_order",
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_per_page = 25

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "category",
                    "name",
                    "slug",
                    "short_description",
                    "description",
                )
            },
        ),
        (
            "🇺🇿 O'zbekcha",
            {
                "fields": (
                    "name_uz",
                    "short_description_uz",
                    "description_uz",
                )
            },
        ),
        (
            "🇬🇧 English",
            {
                "fields": (
                    "name_en",
                    "short_description_en",
                    "description_en",
                )
            },
        ),
        (
            "🇨🇳 中文",
            {
                "fields": (
                    "name_zh",
                    "short_description_zh",
                    "description_zh",
                )
            },
        ),
        (
            "Цена",
            {
                "fields": (
                    "price_from",
                    "price_unit",
                    "price_unit_uz",
                    "price_unit_en",
                    "price_unit_zh",
                )
            },
        ),
        (
            "Изображение",
            {"fields": ("image",)},
        ),
        (
            "Отображение",
            {
                "fields": (
                    "is_popular",
                    "show_on_homepage",
                    "is_active",
                    "sort_order",
                )
            },
        ),
        (
            "SEO",
            {
                "fields": (
                    "seo_title",
                    "seo_description",
                )
            },
        ),
        (
            "Служебная информация",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
