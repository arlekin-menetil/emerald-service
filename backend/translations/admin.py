from django.contrib import admin

from .models import Translation


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "is_active",
        "source_file",
        "source_line",
        "updated_at",
    )

    list_display_links = ("key",)

    list_filter = (
        "is_active",
    )

    search_fields = (
        "key",
        "ru",
        "uz",
        "en",
        "zh",
        "source_file",
        "source_text",
    )

    ordering = ("key",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Переводы",
            {
                "fields": (
                    "key",
                    "ru",
                    "uz",
                    "en",
                    "zh",
                    "is_active",
                )
            },
        ),
        (
            "Источник",
            {
                "fields": (
                    "source_file",
                    "source_text",
                    "source_line",
                    "description",
                )
            },
        ),
        (
            "Система",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
