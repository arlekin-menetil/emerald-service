import re

from django.utils import timezone
from rest_framework import serializers

from services.models import Service
from company.models import Company
from .models import ServiceRequest

# ============================================================
# PUBLIC CREATE
# ============================================================


class ServiceRequestCreateSerializer(serializers.ModelSerializer):
    """
    Публичное создание заявки клиентом с сайта.

    Клиент может передать только:
    - имя;
    - телефон;
    - адрес;
    - координаты;
    - услугу;
    - желаемое время приезда;
    - комментарий.

    Системные поля заявки клиент изменить не может.
    """

    service = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.filter(
            is_active=True,
        ),
    )

    name = serializers.CharField(
        max_length=150,
        trim_whitespace=True,
        allow_blank=False,
    )

    phone = serializers.CharField(
        max_length=50,
        trim_whitespace=True,
        allow_blank=False,
    )

    address = serializers.CharField(
        max_length=500,
        trim_whitespace=True,
        allow_blank=False,
    )

    latitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6,
        required=False,
        allow_null=True,
    )

    longitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6,
        required=False,
        allow_null=True,
    )

    comment = serializers.CharField(
        max_length=2000,
        trim_whitespace=True,
        required=False,
        allow_blank=True,
    )

    language = serializers.ChoiceField(
        choices=ServiceRequest.LANGUAGE_CHOICES,
        required=False,
    )

    scheduled_at = serializers.DateTimeField(
        required=True,
        allow_null=False,
    )

    class Meta:
        model = ServiceRequest

        fields = (
            "id",
            "name",
            "phone",
            "address",
            "latitude",
            "longitude",
            "service",
            "scheduled_at",
            "comment",
            "language",
            "status",
            "created_at",
            "rating_token",
        )

        read_only_fields = (
            "id",
            "status",
            "created_at",
            "rating_token",
        )

    # ========================================================
    # NAME
    # ========================================================

    def validate_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError("Имя должно содержать минимум 2 символа.")

        if "\x00" in value:
            raise serializers.ValidationError("Имя содержит недопустимые символы.")

        return value

    # ========================================================
    # PHONE
    # ========================================================

    def validate_phone(self, value):
        value = value.strip()

        if "\x00" in value:
            raise serializers.ValidationError(
                "Номер телефона содержит недопустимые символы."
            )

        # Убираем пробелы, скобки и дефисы.
        normalized = re.sub(r"[()\s\-]", "", value)

        # 998901234567 -> +998901234567
        if normalized.startswith("998"):
            normalized = "+" + normalized

        # 901234567 -> +998901234567
        elif normalized.startswith("9") and len(normalized) == 9:
            normalized = "+998" + normalized

        # Итоговый формат:
        # +998 + 9 цифр
        if not re.fullmatch(r"\+998\d{9}", normalized):
            raise serializers.ValidationError(
                "Укажите корректный номер телефона Узбекистана."
            )

        return normalized

    # ========================================================
    # ADDRESS
    # ========================================================

    def validate_address(self, value):
        value = value.strip()

        if len(value) < 5:
            raise serializers.ValidationError("Укажите корректный адрес.")

        if "\x00" in value:
            raise serializers.ValidationError("Адрес содержит недопустимые символы.")

        return value

    # ========================================================
    # SCHEDULED AT
    # ========================================================

    def validate_scheduled_at(self, value):
        if value is None:
            raise serializers.ValidationError(
                "Укажите желаемое время приезда сантехника."
            )

        now = timezone.now()

        if value <= now:
            raise serializers.ValidationError(
                "Желаемое время приезда должно быть в будущем."
            )

        company = (
            Company.objects
            .filter(is_active=True)
            .order_by("id")
            .first()
        )

        if company:
            local_value = timezone.localtime(value)
            selected_time = local_value.time().replace(
                second=0,
                microsecond=0,
            )

            work_start = company.work_start
            work_end = company.work_end

            if selected_time < work_start or selected_time > work_end:
                raise serializers.ValidationError(
                    f"Выберите время в рабочем диапазоне "
                    f"{work_start.strftime('%H:%M')}–"
                    f"{work_end.strftime('%H:%M')}."
                )

            step = company.booking_step_minutes

            if step > 0:
                start_minutes = (
                    work_start.hour * 60 +
                    work_start.minute
                )

                selected_minutes = (
                    selected_time.hour * 60 +
                    selected_time.minute
                )

                if (selected_minutes - start_minutes) % step != 0:
                    raise serializers.ValidationError(
                        f"Время можно выбрать с шагом {step} минут, "
                        f"начиная с {work_start.strftime('%H:%M')}."
                    )

        return value

    # ========================================================
    # COMMENT
    # ========================================================

    def validate_comment(self, value):
        value = value.strip()

        if "\x00" in value:
            raise serializers.ValidationError(
                "Комментарий содержит недопустимые символы."
            )

        return value


# ============================================================
# ADMIN
# ============================================================


class ServiceRequestAdminSerializer(serializers.ModelSerializer):
    """
    Представление заявки для административной части.

    Системные поля:
    - status;
    - completed_at;
    - rating;
    - created_at;
    - updated_at

    нельзя изменить через этот serializer.

    Изменение статуса выполняется отдельным
    защищённым endpoint.
    """

    service_name = serializers.CharField(
        source="service.name",
        read_only=True,
    )

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    is_rated = serializers.BooleanField(
        read_only=True,
    )

    name = serializers.CharField(
        max_length=150,
        trim_whitespace=True,
        allow_blank=False,
    )

    phone = serializers.CharField(
        max_length=50,
        trim_whitespace=True,
        allow_blank=False,
    )

    address = serializers.CharField(
        max_length=500,
        trim_whitespace=True,
        allow_blank=False,
    )

    comment = serializers.CharField(
        max_length=2000,
        trim_whitespace=True,
        required=False,
        allow_blank=True,
    )

    class Meta:
        model = ServiceRequest

        fields = (
            "id",
            "name",
            "phone",
            "address",
            "latitude",
            "longitude",
            "service",
            "service_name",
            "scheduled_at",
            "comment",
            "status",
            "status_display",
            "completed_at",
            "rating",
            "is_rated",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "service_name",
            "status",
            "status_display",
            "completed_at",
            "rating",
            "is_rated",
            "created_at",
            "updated_at",
        )

    # ========================================================
    # NAME
    # ========================================================

    def validate_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError("Имя должно содержать минимум 2 символа.")

        if "\x00" in value:
            raise serializers.ValidationError("Имя содержит недопустимые символы.")

        return value

    # ========================================================
    # PHONE
    # ========================================================

    def validate_phone(self, value):
        value = value.strip()

        if "\x00" in value:
            raise serializers.ValidationError(
                "Номер телефона содержит недопустимые символы."
            )

        # Убираем пробелы, скобки и дефисы.
        normalized = re.sub(r"[()\s\-]", "", value)

        # 998901234567 -> +998901234567
        if normalized.startswith("998"):
            normalized = "+" + normalized

        # 901234567 -> +998901234567
        elif normalized.startswith("9") and len(normalized) == 9:
            normalized = "+998" + normalized

        # Итоговый формат:
        # +998 + 9 цифр
        if not re.fullmatch(r"\+998\d{9}", normalized):
            raise serializers.ValidationError(
                "Укажите корректный номер телефона Узбекистана."
            )

        return normalized

    # ========================================================
    # ADDRESS
    # ========================================================

    def validate_address(self, value):
        value = value.strip()

        if len(value) < 5:
            raise serializers.ValidationError("Укажите корректный адрес.")

        if "\x00" in value:
            raise serializers.ValidationError("Адрес содержит недопустимые символы.")

        return value

    # ========================================================
    # COMMENT
    # ========================================================

    def validate_comment(self, value):
        value = value.strip()

        if "\x00" in value:
            raise serializers.ValidationError(
                "Комментарий содержит недопустимые символы."
            )

        return value


# ============================================================
# PUBLIC RATING
# ============================================================


class ServiceRequestRatingSerializer(serializers.Serializer):
    """
    Публичная оценка выполненной заявки.

    Разрешены только целые значения от 1 до 5.
    """

    rating = serializers.IntegerField(
        min_value=1,
        max_value=5,
        required=True,
    )


# ============================================================
# ADMIN STATUS
# ============================================================


class ServiceRequestStatusSerializer(serializers.Serializer):
    """
    Изменение статуса заявки менеджером.
    """

    status = serializers.ChoiceField(
        choices=ServiceRequest.STATUS_CHOICES,
        required=True,
    )
