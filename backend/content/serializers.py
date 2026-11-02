from rest_framework import serializers

from .models import Video, Work


class WorkSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Work
        fields = [
            "id",
            "title",
            "title_uz",
            "title_en",
            "title_zh",
            "description",
            "description_uz",
            "description_en",
            "description_zh",
            "category",
            "image",
            "image_url",
            "sort_order",
            "is_published",
            "created_at",
            "updated_at",
        ]

    def get_image_url(self, obj):
        if not obj.image:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(obj.image.url)

        return obj.image.url


class VideoSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "title_uz",
            "title_en",
            "title_zh",
            "description",
            "description_uz",
            "description_en",
            "description_zh",
            "youtube_url",
            "youtube_id",
            "thumbnail",
            "thumbnail_url",
            "category",
            "sort_order",
            "is_published",
            "created_at",
            "updated_at",
        ]

    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(obj.thumbnail.url)

            return obj.thumbnail.url

        if obj.youtube_id:
            return f"https://img.youtube.com/vi/{obj.youtube_id}/maxresdefault.jpg"

        return None
