from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "position",
        "experience",
        "phone",
        "telegram_username",
        "telegram_id",
        "is_active",
        "is_published",
        "sort_order",
        "created_at",
    )

    list_editable = (
        "is_published",
        "sort_order",
    )

    list_filter = (
        "position",
        "is_active",
        "is_published",
    )

    search_fields = (
        "name",
        "phone",
        "telegram_username",
        "telegram_id",
    )

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
                    "website_name",
                    "position",
                    "experience",
                    "photo",
                    "is_active",
                )
            },
        ),
        (
            "Публикация на сайте",
            {
                "fields": (
                    "is_published",
                    "sort_order",
                ),
                "description": (
                    "Управление отображением сотрудника "
                    "на публичном сайте."
                ),
            },
        ),
        (
            "Контакты и Telegram",
            {
                "fields": (
                    "phone",
                    "telegram_id",
                    "telegram_username",
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
