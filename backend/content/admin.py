from django.contrib import admin

from .models import Video, Work


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "sort_order",
        "is_published",
        "created_at",
    )

    list_filter = (
        "category",
        "is_published",
    )

    search_fields = (
        "title",
        "title_uz",
        "title_en",
        "title_zh",
        "description",
        "description_uz",
        "description_en",
        "description_zh",
    )

    list_editable = (
        "sort_order",
        "is_published",
    )

    ordering = (
        "sort_order",
        "-created_at",
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
                    "title",
                    "description",
                    "category",
                    "image",
                )
            },
        ),
        (
            "O'zbekcha",
            {
                "fields": (
                    "title_uz",
                    "description_uz",
                )
            },
        ),
        (
            "English",
            {
                "fields": (
                    "title_en",
                    "description_en",
                )
            },
        ),
        (
            "中文",
            {
                "fields": (
                    "title_zh",
                    "description_zh",
                )
            },
        ),
        (
            "Публикация",
            {
                "fields": (
                    "sort_order",
                    "is_published",
                )
            },
        ),
        (
            "Системная информация",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "sort_order",
        "is_published",
        "created_at",
    )

    list_filter = (
        "category",
        "is_published",
    )

    search_fields = (
        "title",
        "title_uz",
        "title_en",
        "title_zh",
        "description",
        "description_uz",
        "description_en",
        "description_zh",
        "youtube_url",
        "youtube_id",
    )

    list_editable = (
        "sort_order",
        "is_published",
    )

    ordering = (
        "sort_order",
        "-created_at",
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
                    "title",
                    "description",
                    "category",
                    "youtube_url",
                    "youtube_id",
                    "thumbnail",
                )
            },
        ),
        (
            "O'zbekcha",
            {
                "fields": (
                    "title_uz",
                    "description_uz",
                )
            },
        ),
        (
            "English",
            {
                "fields": (
                    "title_en",
                    "description_en",
                )
            },
        ),
        (
            "中文",
            {
                "fields": (
                    "title_zh",
                    "description_zh",
                )
            },
        ),
        (
            "Публикация",
            {
                "fields": (
                    "sort_order",
                    "is_published",
                )
            },
        ),
        (
            "Системная информация",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
