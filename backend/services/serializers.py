from rest_framework import serializers

from .models import ServiceCategory, Service


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory

        fields = (
            "id",
            "name",
            "slug",
            "description",
            "is_active",
            "sort_order",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    image_url = serializers.SerializerMethodField()

    rating = serializers.FloatField(read_only=True)
    rating_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Service

        fields = (
            "id",
            "category",
            "category_name",
            "name",
            "slug",
            "short_description",
            "description",
            "price_from",
            "price_unit",
            "image",
            "image_url",
            "is_popular",
            "show_on_homepage",
            "is_active",
            "sort_order",
            "seo_title",
            "seo_description",
            "rating",
            "rating_count",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "category_name",
            "image_url",
            "rating",
            "rating_count",
            "created_at",
            "updated_at",
        )

    def get_image_url(self, obj):
        request = self.context.get("request")

        if not obj.image:
            return None

        url = obj.image.url

        if request:
            return request.build_absolute_uri(url)

        return url

    def to_representation(self, instance):
        data = super().to_representation(instance)

        request = self.context.get("request")
        language = "ru"

        if request:
            language = request.query_params.get("lang", "ru").strip().lower()

        if language not in {"ru", "uz", "en", "zh"}:
            language = "ru"

        fields_map = {
            "name": {
                "ru": "name",
                "uz": "name_uz",
                "en": "name_en",
                "zh": "name_zh",
            },
            "short_description": {
                "ru": "short_description",
                "uz": "short_description_uz",
                "en": "short_description_en",
                "zh": "short_description_zh",
            },
            "description": {
                "ru": "description",
                "uz": "description_uz",
                "en": "description_en",
                "zh": "description_zh",
            },
            "price_unit": {
                "ru": "price_unit",
                "uz": "price_unit_uz",
                "en": "price_unit_en",
                "zh": "price_unit_zh",
            },
        }

        for output_field, language_fields in fields_map.items():
            translated_field = language_fields[language]
            translated_value = getattr(instance, translated_field, "")

            if translated_value:
                data[output_field] = translated_value

        return data

