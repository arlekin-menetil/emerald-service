from django.contrib import admin

from .models import ServiceRequest


@admin.action(description="Отметить выбранные заявки как выполненные")
def mark_as_completed(
    modeladmin,
    request,
    queryset,
):
    updated = 0

    for service_request in queryset:
        if service_request.status != ServiceRequest.STATUS_COMPLETED:
            service_request.mark_completed()
            updated += 1

    modeladmin.message_user(
        request,
        f"Заявок отмечено как выполненные: {updated}.",
    )


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "phone",
        "service",
        "status",
        "rating",
        "completed_at",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "rating",
        "service",
        "created_at",
        "completed_at",
    )

    search_fields = (
        "name",
        "phone",
        "address",
        "comment",
        "service__name",
        "employees__name",
    )

    autocomplete_fields = ("service",)

    filter_horizontal = ("employees",)

    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
        "completed_at",
    )

    actions = (mark_as_completed,)

    fieldsets = (
        (
            "Информация о клиенте",
            {
                "fields": (
                    "name",
                    "phone",
                    "address",
                ),
            },
        ),
        (
            "Заявка",
            {
                "fields": (
                    "service",
                    "employees",
                    "comment",
                    "status",
                ),
            },
        ),
        (
            "Выполнение",
            {
                "fields": ("completed_at",),
            },
        ),
        (
            "Оценка клиента",
            {
                "fields": ("rating",),
            },
        ),
        (
            "Служебная информация",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
