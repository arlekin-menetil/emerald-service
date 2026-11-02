from rest_framework import serializers

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "id",
            "name",
            "website_name",
            "position",
            "experience",
            "photo",
            "is_active",
            "is_published",
            "sort_order",
        ]
        read_only_fields = ["id"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        request = self.context.get("request")
        language = "ru"

        if request:
            language = request.query_params.get(
                "lang",
                "ru",
            ).strip().lower()

        if language not in {"ru", "uz", "en", "zh"}:
            language = "ru"

        # ==========================================
        # ЛОКАЛИЗАЦИЯ ИМЕНИ
        # ==========================================

        name_fields = {
            "ru": "name",
            "uz": "name_uz",
            "en": "name_en",
            "zh": "name_zh",
        }

        translated_name = getattr(
            instance,
            name_fields[language],
            "",
        )

        if translated_name:
            data["name"] = translated_name

        # ==========================================
        # ЛОКАЛИЗАЦИЯ ДОЛЖНОСТИ
        # ==========================================

        website_name_fields = {
            "ru": "website_name",
            "uz": "website_name_uz",
            "en": "website_name_en",
            "zh": "website_name_zh",
        }

        translated_website_name = getattr(
            instance,
            website_name_fields[language],
            "",
        )

        if translated_website_name:
            data["website_name"] = translated_website_name

        position_fields = {
            "ru": "position",
            "uz": "position_uz",
            "en": "position_en",
            "zh": "position_zh",
        }

        translated_position = getattr(
            instance,
            position_fields[language],
            "",
        )

        if translated_position:
            data["position"] = translated_position

        return data
