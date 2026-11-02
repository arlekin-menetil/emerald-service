from django.urls import path

from .views import (
    EmployeeDetailAPIView,
    EmployeeListAPIView,
)

urlpatterns = [
    path(
        "",
        EmployeeListAPIView.as_view(),
        name="employee-list",
    ),
    path(
        "<int:pk>/",
        EmployeeDetailAPIView.as_view(),
        name="employee-detail",
    ),
]
