from django.urls import path

from .views import VideoListView, WorkListView


urlpatterns = [
    path("works/", WorkListView.as_view(), name="content-works"),
    path("videos/", VideoListView.as_view(), name="content-videos"),
]
