import re

from rest_framework import serializers

from .models import VacancyApplication


class VacancyApplicationCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=150,
        trim_whitespace=True,
        allow_blank=False,
        required=True,
    )

    phone = serializers.CharField(
        max_length=50,
        trim_whitespace=True,
        allow_blank=False,
        required=True,
    )

    experience = serializers.CharField(
        max_length=500,
        trim_whitespace=True,
        allow_blank=False,
        required=True,
    )

    specialization = serializers.CharField(
        max_length=255,
        trim_whitespace=True,
        allow_blank=False,
        required=True,
    )

    about = serializers.CharField(
        max_length=3000,
        trim_whitespace=True,
        allow_blank=False,
        required=True,
    )

    language = serializers.ChoiceField(
        choices=VacancyApplication.LANGUAGE_CHOICES,
        required=True,
    )

    class Meta:
        model = VacancyApplication
        fields = (
            "id",
            "name",
            "phone",
            "experience",
            "specialization",
            "about",
            "language",
            "status",
            "created_at",
        )

        read_only_fields = (
            "id",
            "status",
            "created_at",
        )

    def validate_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Укажите имя минимум из 2 символов."
            )

        if "\x00" in value:
            raise serializers.ValidationError(
                "Имя содержит недопустимые символы."
            )

        return value

    def validate_phone(self, value):
        value = value.strip()

        if "\x00" in value:
            raise serializers.ValidationError(
                "Номер телефона содержит недопустимые символы."
            )

        normalized = re.sub(r"[()\s\-]", "", value)

        if normalized.startswith("998"):
            normalized = "+" + normalized
        elif normalized.startswith("9") and len(normalized) == 9:
            normalized = "+998" + normalized

        if not re.fullmatch(r"\+998\d{9}", normalized):
            raise serializers.ValidationError(
                "Укажите корректный номер телефона Узбекистана."
            )

        return normalized

    def validate_experience(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Укажите ваш опыт работы."
            )

        if "\x00" in value:
            raise serializers.ValidationError(
                "Опыт содержит недопустимые символы."
            )

        return value

    def validate_specialization(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Укажите специализацию."
            )

        if "\x00" in value:
            raise serializers.ValidationError(
                "Специализация содержит недопустимые символы."
            )

        return value

    def validate_about(self, value):
        value = value.strip()

        if len(value) < 5:
            raise serializers.ValidationError(
                "Расскажите немного о себе."
            )

        if "\x00" in value:
            raise serializers.ValidationError(
                "Описание содержит недопустимые символы."
            )

        return value
