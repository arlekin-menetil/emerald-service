from rest_framework import serializers

from .models import Category, Product, ProductImage


SUPPORTED_LANGUAGES = ("ru", "uz", "en", "zh")


def get_language(serializer):
    request = serializer.context.get("request")

    if not request:
        return "ru"

    language = request.query_params.get("lang", "ru")

    if language not in SUPPORTED_LANGUAGES:
        return "ru"

    return language


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "name_uz",
            "name_en",
            "name_zh",
            "slug",
            "description",
            "image",
            "sort_order",
        )

    def get_name(self, obj):
        language = get_language(self)

        if language == "uz" and obj.name_uz:
            return obj.name_uz

        if language == "en" and obj.name_en:
            return obj.name_en

        if language == "zh" and obj.name_zh:
            return obj.name_zh

        return obj.name

    def get_description(self, obj):
        return obj.description


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            "id",
            "image",
            "sort_order",
        )


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    category_slug = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    gallery = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "category_name",
            "category_slug",
            "name",
            "name_uz",
            "name_en",
            "name_zh",
            "slug",
            "sku",
            "description",
            "description_uz",
            "description_en",
            "description_zh",
            "price",
            "stock_quantity",
            "image",
            "gallery",
            "is_available",
            "is_featured",
            "sort_order",
        )

    def get_name(self, obj):
        language = get_language(self)

        if language == "uz" and obj.name_uz:
            return obj.name_uz

        if language == "en" and obj.name_en:
            return obj.name_en

        if language == "zh" and obj.name_zh:
            return obj.name_zh

        return obj.name

    def get_category_slug(self, obj):
        return obj.category.slug if obj.category else ""

    def get_category_name(self, obj):
        language = get_language(self)
        category = obj.category

        if language == "uz" and category.name_uz:
            return category.name_uz

        if language == "en" and category.name_en:
            return category.name_en

        if language == "zh" and category.name_zh:
            return category.name_zh

        return category.name

    def get_description(self, obj):
        language = get_language(self)

        if language == "uz" and obj.description_uz:
            return obj.description_uz

        if language == "en" and obj.description_en:
            return obj.description_en

        if language == "zh" and obj.description_zh:
            return obj.description_zh

        return obj.description
