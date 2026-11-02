from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import Video, Work
from .serializers import VideoSerializer, WorkSerializer


class WorkListView(ListAPIView):
    serializer_class = WorkSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Work.objects.filter(
            is_published=True
        ).order_by(
            "sort_order",
            "-created_at",
        )


class VideoListView(ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Video.objects.filter(
            is_published=True
        ).order_by(
            "sort_order",
            "-created_at",
        )
