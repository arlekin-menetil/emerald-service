from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "city",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "city",
    )

    search_fields = (
        "name",
        "short_name",
        "phone",
        "email",
        "address",
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
                    "short_name",
                    "description",
                    "logo",
                )
            },
        ),
        (
            "Контакты",
            {
                "fields": (
                    "phone",
                    "phone_secondary",
                    "email",
                )
            },
        ),
        (
            "Адрес",
            {
                "fields": (
                    "city",
                    "address",
                    "latitude",
                    "longitude",
                )
            },
        ),
        (
            "Режим работы",
            {
                "fields": (
                    "working_hours",
                    "work_start",
                    "work_end",
                    "booking_step_minutes",
                ),
                "description": (
                    "Настройки рабочего времени используются "
                    "для записи клиента на сайте."
                ),
            },
        ),
        (
            "Социальные сети",
            {
                "fields": (
                    "telegram_url",
                    "instagram_url",
                    "facebook_url",
                    "youtube_url",
                )
            },
        ),
        (
            "Служебная информация",
            {
                "fields": (
                    "is_active",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    ordering = ("-updated_at",)
