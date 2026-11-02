from django.urls import path

from .views import VacancyApplicationCreateAPIView


urlpatterns = [
    path(
        "applications/",
        VacancyApplicationCreateAPIView.as_view(),
        name="vacancy-application-create",
    ),
]
