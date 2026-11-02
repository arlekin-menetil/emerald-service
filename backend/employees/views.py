from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeListAPIView(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Employee.objects.filter(
            is_active=True,
            is_published=True,
        ).order_by("sort_order", "name")


class EmployeeDetailAPIView(generics.RetrieveAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Employee.objects.filter(is_active=True)
