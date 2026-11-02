from rest_framework import serializers

from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "short_name",
            "description",
            "phone",
            "phone_secondary",
            "email",
            "address",
            "city",
            "latitude",
            "longitude",
            "working_hours",
            "work_start",
            "work_end",
            "booking_step_minutes",
            "telegram_url",
            "instagram_url",
            "facebook_url",
            "youtube_url",
            "logo",
            "logo_url",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "logo_url",
            "created_at",
            "updated_at",
        )

    def get_logo_url(self, obj):
        request = self.context.get("request")

        if not obj.logo:
            return None

        url = obj.logo.url

        if request:
            return request.build_absolute_uri(url)

        return url
