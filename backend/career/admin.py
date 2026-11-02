from django.contrib import admin

from .models import VacancyApplication


@admin.register(VacancyApplication)
class VacancyApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "phone",
        "specialization",
        "experience",
        "language",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "language",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "specialization",
        "experience",
        "about",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
