import uuid
from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from services.models import Service, ServiceCategory
from service_requests.models import ServiceRequest
from service_requests.views import ServiceRequestCreateAPIView


class ServiceRequestModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = ServiceCategory.objects.create(
            name="Тестовая категория",
            slug="test-category",
            is_active=True,
        )

        cls.service = Service.objects.create(
            category=cls.category,
            name="Тестовая услуга",
            slug="test-service",
            is_active=True,
        )

    def create_request(self, **kwargs):
        defaults = {
            "name": "Тестовый клиент",
            "phone": "+998901234567",
            "service": self.service,
            "scheduled_at": timezone.now() + timedelta(hours=2),
        }

        defaults.update(kwargs)

        return ServiceRequest.objects.create(**defaults)

    def test_new_request_has_new_status(self):
        request = self.create_request()

        self.assertEqual(
            request.status,
            ServiceRequest.STATUS_NEW,
        )

    def test_is_rated_false_without_rating(self):
        request = self.create_request()

        self.assertFalse(request.is_rated)

    def test_is_rated_true_with_rating(self):
        request = self.create_request(rating=5)

        self.assertTrue(request.is_rated)

    def test_mark_completed_sets_status_and_completed_at(self):
        request = self.create_request()

        self.assertIsNone(request.completed_at)

        request.mark_completed()
        request.refresh_from_db()

        self.assertEqual(
            request.status,
            ServiceRequest.STATUS_COMPLETED,
        )

        self.assertIsNotNone(
            request.completed_at,
        )

    def test_mark_completed_does_not_overwrite_existing_completed_at(self):
        completed_at = timezone.now() - timedelta(hours=1)

        request = self.create_request(
            status=ServiceRequest.STATUS_COMPLETED,
            completed_at=completed_at,
        )

        request.mark_completed()
        request.refresh_from_db()

        self.assertEqual(
            request.status,
            ServiceRequest.STATUS_COMPLETED,
        )

        self.assertEqual(
            request.completed_at,
            completed_at,
        )


class ServiceRequestCreateAPITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = ServiceCategory.objects.create(
            name="API категория",
            slug="api-category",
            is_active=True,
        )

        cls.service = Service.objects.create(
            category=cls.category,
            name="API услуга",
            slug="api-service",
            is_active=True,
        )

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/service-requests/"

        self.original_throttle_classes = ServiceRequestCreateAPIView.throttle_classes

        ServiceRequestCreateAPIView.throttle_classes = []

        self.telegram_patcher = patch(
            "service_requests.views.notify_new_service_request"
        )

        self.mock_notify = self.telegram_patcher.start()

    def tearDown(self):
        self.telegram_patcher.stop()

        ServiceRequestCreateAPIView.throttle_classes = self.original_throttle_classes

        super().tearDown()

    def valid_payload(self):
        return {
            "name": "Иван Иванов",
            "phone": "+998901234567",
            "address": "Ташкент, улица Навои, 10",
            "service": self.service.id,
            "scheduled_at": (timezone.now() + timedelta(days=1)).isoformat(),
            "comment": "Нужен ремонт крана",
        }

    def test_create_service_request(self):
        response = self.client.post(
            self.url,
            self.valid_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        request = ServiceRequest.objects.get(
            id=response.data["id"],
        )

        self.assertEqual(
            request.name,
            "Иван Иванов",
        )

        self.assertEqual(
            request.phone,
            "+998901234567",
        )

        self.assertEqual(
            request.status,
            ServiceRequest.STATUS_NEW,
        )

        self.mock_notify.assert_called_once_with(
            request,
        )

    def test_create_without_name(self):
        payload = self.valid_payload()
        payload.pop("name")

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.mock_notify.assert_not_called()

    def test_create_with_too_long_name(self):
        payload = self.valid_payload()
        payload["name"] = "A" * 151

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.mock_notify.assert_not_called()

    def test_create_with_past_scheduled_at(self):
        payload = self.valid_payload()

        payload["scheduled_at"] = (timezone.now() - timedelta(hours=1)).isoformat()

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.mock_notify.assert_not_called()

    def test_create_with_invalid_service(self):
        payload = self.valid_payload()
        payload["service"] = 999999

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.mock_notify.assert_not_called()

    def test_create_with_invalid_phone(self):
        payload = self.valid_payload()
        payload["phone"] = "123456"

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.mock_notify.assert_not_called()

    def test_phone_is_normalized(self):
        payload = self.valid_payload()
        payload["phone"] = "901234567"

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        request = ServiceRequest.objects.get(
            id=response.data["id"],
        )

        self.assertEqual(
            request.phone,
            "+998901234567",
        )

        self.mock_notify.assert_called_once_with(
            request,
        )

    def test_sql_injection_is_stored_as_plain_text(self):
        payload = self.valid_payload()
        payload["name"] = "' OR 1=1 --"

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        request = ServiceRequest.objects.get(
            id=response.data["id"],
        )

        self.assertEqual(
            request.name,
            "' OR 1=1 --",
        )

        self.mock_notify.assert_called_once_with(
            request,
        )

    def test_xss_is_stored_as_plain_text(self):
        payload = self.valid_payload()
        payload["name"] = "<script>alert(1)</script>"

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        request = ServiceRequest.objects.get(
            id=response.data["id"],
        )

        self.assertEqual(
            request.name,
            "<script>alert(1)</script>",
        )

        self.mock_notify.assert_called_once_with(
            request,
        )

    def test_public_create_cannot_set_status(self):
        payload = self.valid_payload()
        payload["status"] = ServiceRequest.STATUS_COMPLETED

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        request = ServiceRequest.objects.get(
            id=response.data["id"],
        )

        self.assertEqual(
            request.status,
            ServiceRequest.STATUS_NEW,
        )

        self.mock_notify.assert_called_once_with(
            request,
        )

    def test_public_create_cannot_set_completed_at(self):
        payload = self.valid_payload()
        payload["completed_at"] = timezone.now().isoformat()

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        request = ServiceRequest.objects.get(
            id=response.data["id"],
        )

        self.assertIsNone(
            request.completed_at,
        )

        self.mock_notify.assert_called_once_with(
            request,
        )


class ServiceRequestPermissionAPITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = ServiceCategory.objects.create(
            name="Permission категория",
            slug="permission-category",
            is_active=True,
        )

        cls.service = Service.objects.create(
            category=cls.category,
            name="Permission услуга",
            slug="permission-service",
            is_active=True,
        )

        cls.service_request = ServiceRequest.objects.create(
            name="Тестовый клиент",
            phone="+998901234567",
            address="Ташкент",
            service=cls.service,
            scheduled_at=timezone.now() + timedelta(days=1),
        )

        User = get_user_model()

        cls.regular_user = User.objects.create_user(
            username="test_regular_user",
            password="TestPassword123!",
        )

        cls.admin_user = User.objects.create_user(
            username="test_admin_user",
            password="TestPassword123!",
            is_staff=True,
            is_superuser=True,
        )

    def setUp(self):
        self.client = APIClient()

        self.list_url = "/api/service-requests/list/"

        self.detail_url = f"/api/service-requests/{self.service_request.pk}/"

        self.status_url = f"/api/service-requests/{self.service_request.pk}/status/"

    def test_list_without_authentication(self):
        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            401,
        )

    def test_list_regular_user_forbidden(self):
        self.client.force_authenticate(
            user=self.regular_user,
        )

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_list_admin_allowed(self):
        self.client.force_authenticate(
            user=self.admin_user,
        )

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_detail_without_authentication(self):
        response = self.client.get(
            self.detail_url,
        )

        self.assertEqual(
            response.status_code,
            401,
        )

    def test_detail_regular_user_forbidden(self):
        self.client.force_authenticate(
            user=self.regular_user,
        )

        response = self.client.get(
            self.detail_url,
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_detail_admin_allowed(self):
        self.client.force_authenticate(
            user=self.admin_user,
        )

        response = self.client.get(
            self.detail_url,
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_status_without_authentication(self):
        response = self.client.patch(
            self.status_url,
            {
                "status": ServiceRequest.STATUS_IN_PROGRESS,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            401,
        )

    def test_status_regular_user_forbidden(self):
        self.client.force_authenticate(
            user=self.regular_user,
        )

        response = self.client.patch(
            self.status_url,
            {
                "status": ServiceRequest.STATUS_IN_PROGRESS,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_status_admin_allowed(self):
        self.client.force_authenticate(
            user=self.admin_user,
        )

        response = self.client.patch(
            self.status_url,
            {
                "status": ServiceRequest.STATUS_IN_PROGRESS,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.service_request.refresh_from_db()

        self.assertEqual(
            self.service_request.status,
            ServiceRequest.STATUS_IN_PROGRESS,
        )


class ServiceRequestStatusAPITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = ServiceCategory.objects.create(
            name="Status категория",
            slug="status-category",
            is_active=True,
        )

        cls.service = Service.objects.create(
            category=cls.category,
            name="Status услуга",
            slug="status-service",
            is_active=True,
        )

        User = get_user_model()

        cls.admin_user = User.objects.create_user(
            username="status_admin",
            password="TestPassword123!",
            is_staff=True,
            is_superuser=True,
        )

    def setUp(self):
        self.client = APIClient()

        self.service_request = ServiceRequest.objects.create(
            name="Тестовый клиент",
            phone="+998901234567",
            address="Ташкент",
            service=self.service,
            scheduled_at=timezone.now() + timedelta(days=1),
        )

        self.url = f"/api/service-requests/" f"{self.service_request.pk}/status/"

        self.client.force_authenticate(
            user=self.admin_user,
        )

    def change_status(self, new_status):
        return self.client.patch(
            self.url,
            {
                "status": new_status,
            },
            format="json",
        )

    def test_new_to_new(self):
        response = self.change_status(
            ServiceRequest.STATUS_NEW,
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.service_request.refresh_from_db()

        self.assertEqual(
            self.service_request.status,
            ServiceRequest.STATUS_NEW,
        )

        self.assertIsNone(
            self.service_request.completed_at,
        )

    def test_new_to_in_progress(self):
        response = self.change_status(
            ServiceRequest.STATUS_IN_PROGRESS,
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.service_request.refresh_from_db()

        self.assertEqual(
            self.service_request.status,
            ServiceRequest.STATUS_IN_PROGRESS,
        )

        self.assertIsNone(
            self.service_request.completed_at,
        )

    def test_new_to_cancelled(self):
        response = self.change_status(
            ServiceRequest.STATUS_CANCELLED,
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.service_request.refresh_from_db()

        self.assertEqual(
            self.service_request.status,
            ServiceRequest.STATUS_CANCELLED,
        )

        self.assertIsNone(
            self.service_request.completed_at,
        )

    def test_new_to_completed_is_forbidden(self):
        response = self.change_status(
            ServiceRequest.STATUS_COMPLETED,
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.service_request.refresh_from_db()

        self.assertEqual(
            self.service_request.status,
            ServiceRequest.STATUS_NEW,
        )

    def test_in_progress_to_completed(self):
        self.service_request.status = ServiceRequest.STATUS_IN_PROGRESS

        self.service_request.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        response = self.change_status(
            ServiceRequest.STATUS_COMPLETED,
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.service_request.refresh_from_db()

        self.assertEqual(
            self.service_request.status,
            ServiceRequest.STATUS_COMPLETED,
        )

        self.assertIsNotNone(
            self.service_request.completed_at,
        )

    def test_in_progress_to_cancelled(self):
        self.service_request.status = ServiceRequest.STATUS_IN_PROGRESS

        self.service_request.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        response = self.change_status(
            ServiceRequest.STATUS_CANCELLED,
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.service_request.refresh_from_db()

        self.assertEqual(
            self.service_request.status,
            ServiceRequest.STATUS_CANCELLED,
        )

        self.assertIsNone(
            self.service_request.completed_at,
        )

    def test_in_progress_to_new_is_forbidden(self):
        self.service_request.status = ServiceRequest.STATUS_IN_PROGRESS

        self.service_request.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        response = self.change_status(
            ServiceRequest.STATUS_NEW,
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.service_request.refresh_from_db()

        self.assertEqual(
            self.service_request.status,
            ServiceRequest.STATUS_IN_PROGRESS,
        )

    def test_completed_to_new_is_forbidden(self):
        self.service_request.status = ServiceRequest.STATUS_COMPLETED

        self.service_request.completed_at = timezone.now()

        self.service_request.save(
            update_fields=[
                "status",
                "completed_at",
                "updated_at",
            ],
        )

        response = self.change_status(
            ServiceRequest.STATUS_NEW,
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.service_request.refresh_from_db()

        self.assertEqual(
            self.service_request.status,
            ServiceRequest.STATUS_COMPLETED,
        )

        self.assertIsNotNone(
            self.service_request.completed_at,
        )

    def test_completed_to_in_progress_is_forbidden(self):
        self.service_request.status = ServiceRequest.STATUS_COMPLETED

        self.service_request.completed_at = timezone.now()

        self.service_request.save(
            update_fields=[
                "status",
                "completed_at",
                "updated_at",
            ],
        )

        response = self.change_status(
            ServiceRequest.STATUS_IN_PROGRESS,
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.service_request.refresh_from_db()

        self.assertEqual(
            self.service_request.status,
            ServiceRequest.STATUS_COMPLETED,
        )

    def test_completed_to_cancelled_is_forbidden(self):
        self.service_request.status = ServiceRequest.STATUS_COMPLETED

        self.service_request.completed_at = timezone.now()

        self.service_request.save(
            update_fields=[
                "status",
                "completed_at",
                "updated_at",
            ],
        )

        response = self.change_status(
            ServiceRequest.STATUS_CANCELLED,
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.service_request.refresh_from_db()

        self.assertEqual(
            self.service_request.status,
            ServiceRequest.STATUS_COMPLETED,
        )

    def test_cancelled_to_new_is_forbidden(self):
        self.service_request.status = ServiceRequest.STATUS_CANCELLED

        self.service_request.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        response = self.change_status(
            ServiceRequest.STATUS_NEW,
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.service_request.refresh_from_db()

        self.assertEqual(
            self.service_request.status,
            ServiceRequest.STATUS_CANCELLED,
        )

    def test_cancelled_to_in_progress_is_forbidden(self):
        self.service_request.status = ServiceRequest.STATUS_CANCELLED

        self.service_request.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        response = self.change_status(
            ServiceRequest.STATUS_IN_PROGRESS,
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.service_request.refresh_from_db()

        self.assertEqual(
            self.service_request.status,
            ServiceRequest.STATUS_CANCELLED,
        )

    def test_completed_status_does_not_overwrite_completed_at(self):
        completed_at = timezone.now() - timedelta(hours=1)

        self.service_request.status = ServiceRequest.STATUS_COMPLETED

        self.service_request.completed_at = completed_at

        self.service_request.save(
            update_fields=[
                "status",
                "completed_at",
                "updated_at",
            ],
        )

        response = self.change_status(
            ServiceRequest.STATUS_COMPLETED,
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.service_request.refresh_from_db()

        self.assertEqual(
            self.service_request.completed_at,
            completed_at,
        )

    def test_invalid_status_returns_400(self):
        response = self.change_status(
            "invalid_status",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.service_request.refresh_from_db()

        self.assertEqual(
            self.service_request.status,
            ServiceRequest.STATUS_NEW,
        )

    def test_nonexistent_request_returns_404(self):
        url = "/api/service-requests/999999/status/"

        response = self.client.patch(
            url,
            {
                "status": ServiceRequest.STATUS_IN_PROGRESS,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            404,
        )


class ServiceRequestRatingAPITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = ServiceCategory.objects.create(
            name="Rating категория",
            slug="rating-category",
            is_active=True,
        )

        cls.service = Service.objects.create(
            category=cls.category,
            name="Rating услуга",
            slug="rating-service",
            is_active=True,
        )

    def setUp(self):
        self.client = APIClient()

    def create_request(
        self,
        status=ServiceRequest.STATUS_COMPLETED,
    ):
        service_request = ServiceRequest.objects.create(
            name="Иван Иванов",
            phone="+998901234567",
            address="Ташкент, улица Навои, 10",
            service=self.service,
            scheduled_at=timezone.now() + timedelta(days=1),
            status=status,
        )

        if status == ServiceRequest.STATUS_COMPLETED:
            service_request.completed_at = timezone.now()
            service_request.save(
                update_fields=[
                    "completed_at",
                    "updated_at",
                ],
            )

        return service_request

    def test_completed_request_can_be_rated(self):
        service_request = self.create_request()

        response = self.client.post(
            f"/api/service-requests/" f"{service_request.rating_token}/rate/",
            {"rating": 5},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        service_request.refresh_from_db()

        self.assertEqual(
            service_request.rating,
            5,
        )

    def test_completed_request_cannot_be_rated_twice(self):
        service_request = self.create_request()

        response = self.client.post(
            f"/api/service-requests/" f"{service_request.rating_token}/rate/",
            {"rating": 5},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        response = self.client.post(
            f"/api/service-requests/" f"{service_request.rating_token}/rate/",
            {"rating": 4},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        service_request.refresh_from_db()

        self.assertEqual(
            service_request.rating,
            5,
        )

    def test_new_request_cannot_be_rated(self):
        service_request = self.create_request(
            status=ServiceRequest.STATUS_NEW,
        )

        response = self.client.post(
            f"/api/service-requests/" f"{service_request.rating_token}/rate/",
            {"rating": 5},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        service_request.refresh_from_db()

        self.assertIsNone(
            service_request.rating,
        )

    def test_in_progress_request_cannot_be_rated(self):
        service_request = self.create_request(
            status=ServiceRequest.STATUS_IN_PROGRESS,
        )

        response = self.client.post(
            f"/api/service-requests/" f"{service_request.rating_token}/rate/",
            {"rating": 5},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        service_request.refresh_from_db()

        self.assertIsNone(
            service_request.rating,
        )

    def test_cancelled_request_cannot_be_rated(self):
        service_request = self.create_request(
            status=ServiceRequest.STATUS_CANCELLED,
        )

        response = self.client.post(
            f"/api/service-requests/" f"{service_request.rating_token}/rate/",
            {"rating": 5},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        service_request.refresh_from_db()

        self.assertIsNone(
            service_request.rating,
        )

    def test_rating_zero_is_invalid(self):
        service_request = self.create_request()

        response = self.client.post(
            f"/api/service-requests/" f"{service_request.rating_token}/rate/",
            {"rating": 0},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        service_request.refresh_from_db()

        self.assertIsNone(
            service_request.rating,
        )

    def test_rating_six_is_invalid(self):
        service_request = self.create_request()

        response = self.client.post(
            f"/api/service-requests/" f"{service_request.rating_token}/rate/",
            {"rating": 6},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        service_request.refresh_from_db()

        self.assertIsNone(
            service_request.rating,
        )

    def test_rating_missing_is_invalid(self):
        service_request = self.create_request()

        response = self.client.post(
            f"/api/service-requests/" f"{service_request.rating_token}/rate/",
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        service_request.refresh_from_db()

        self.assertIsNone(
            service_request.rating,
        )

    def test_invalid_rating_token_returns_404(self):
        response = self.client.post(
            f"/api/service-requests/" f"{uuid.uuid4()}/rate/",
            {"rating": 5},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_rating_is_public(self):
        service_request = self.create_request()

        self.client.force_authenticate(
            user=None,
        )

        response = self.client.post(
            f"/api/service-requests/" f"{service_request.rating_token}/rate/",
            {"rating": 4},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        service_request.refresh_from_db()

        self.assertEqual(
            service_request.rating,
            4,
        )


class ServiceRequestRateLimitTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = ServiceCategory.objects.create(
            name="Rate Limit категория",
            slug="rate-limit-category",
            is_active=True,
        )

        cls.service = Service.objects.create(
            category=cls.category,
            name="Rate Limit услуга",
            slug="rate-limit-service",
            is_active=True,
        )

    def setUp(self):
        cache.clear()

        self.client = APIClient()
        self.url = "/api/service-requests/"

        self.telegram_patcher = patch(
            "service_requests.views.notify_new_service_request"
        )

        self.mock_notify = self.telegram_patcher.start()

    def tearDown(self):
        self.telegram_patcher.stop()

        cache.clear()

        super().tearDown()

    def valid_payload(self, index):
        return {
            "name": f"Клиент {index}",
            "phone": f"+9989012345{index:02d}",
            "address": f"Ташкент, улица Навои, дом {index}",
            "service": self.service.id,
            "scheduled_at": (timezone.now() + timedelta(days=1)).isoformat(),
            "comment": "Тест rate limit",
        }

    def test_first_five_requests_are_allowed(self):
        for index in range(1, 6):
            response = self.client.post(
                self.url,
                self.valid_payload(index),
                format="json",
            )

            self.assertEqual(
                response.status_code,
                201,
                msg=(
                    f"Запрос #{index} неожиданно получил "
                    f"{response.status_code}: {response.data}"
                ),
            )

        self.assertEqual(
            ServiceRequest.objects.count(),
            5,
        )

        self.assertEqual(
            self.mock_notify.call_count,
            5,
        )

    def test_sixth_request_is_blocked(self):
        for index in range(1, 6):
            response = self.client.post(
                self.url,
                self.valid_payload(index),
                format="json",
            )

            self.assertEqual(
                response.status_code,
                201,
            )

        response = self.client.post(
            self.url,
            self.valid_payload(6),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            429,
        )

        self.assertEqual(
            ServiceRequest.objects.count(),
            5,
        )

        self.assertEqual(
            self.mock_notify.call_count,
            5,
        )

    def test_rate_limit_does_not_block_rating(self):
        for index in range(1, 6):
            response = self.client.post(
                self.url,
                self.valid_payload(index),
                format="json",
            )

            self.assertEqual(
                response.status_code,
                201,
            )

        sixth_response = self.client.post(
            self.url,
            self.valid_payload(6),
            format="json",
        )

        self.assertEqual(
            sixth_response.status_code,
            429,
        )

        service_request = ServiceRequest.objects.create(
            name="Клиент рейтинга",
            phone="+998901234567",
            address="Ташкент",
            service=self.service,
            scheduled_at=timezone.now() + timedelta(days=1),
            status=ServiceRequest.STATUS_COMPLETED,
            completed_at=timezone.now(),
        )

        response = self.client.post(
            f"/api/service-requests/" f"{service_request.rating_token}/rate/",
            {"rating": 5},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        service_request.refresh_from_db()

        self.assertEqual(
            service_request.rating,
            5,
        )


class JWTAuthenticationTests(TestCase):
    def setUp(self):
        cache.clear()

        self.client = APIClient()

        User = get_user_model()

        self.user = User.objects.create_user(
            username="jwt_test_user",
            password="StrongPassword123!",
            is_staff=True,
            is_superuser=True,
        )

        self.token_url = "/api/auth/token/"
        self.refresh_url = "/api/auth/token/refresh/"

    def tearDown(self):
        cache.clear()
        super().tearDown()

    def login(self, password="StrongPassword123!"):
        return self.client.post(
            self.token_url,
            {
                "username": "jwt_test_user",
                "password": password,
            },
            format="json",
        )

    def test_valid_login_returns_access_and_refresh(self):
        response = self.login()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "access",
            response.data,
        )

        self.assertIn(
            "refresh",
            response.data,
        )

        self.assertTrue(
            response.data["access"],
        )

        self.assertTrue(
            response.data["refresh"],
        )

    def test_invalid_login_returns_401(self):
        response = self.login(
            password="WrongPassword123!",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_refresh_returns_new_access_token(self):
        login_response = self.login()

        self.assertEqual(
            login_response.status_code,
            status.HTTP_200_OK,
        )

        refresh_response = self.client.post(
            self.refresh_url,
            {
                "refresh": login_response.data["refresh"],
            },
            format="json",
        )

        self.assertEqual(
            refresh_response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "access",
            refresh_response.data,
        )

        self.assertTrue(
            refresh_response.data["access"],
        )

    def test_invalid_refresh_token_returns_401(self):
        response = self.client.post(
            self.refresh_url,
            {
                "refresh": "invalid.refresh.token",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_first_five_invalid_logins_are_allowed(self):
        for index in range(1, 6):
            response = self.login(
                password=f"WrongPassword{index}!",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
                msg=(
                    f"Попытка #{index} неожиданно получила "
                    f"{response.status_code}: {response.data}"
                ),
            )

    def test_sixth_invalid_login_is_rate_limited(self):
        for index in range(1, 6):
            response = self.login(
                password=f"WrongPassword{index}!",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
            )

        response = self.login(
            password="WrongPassword6!",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS,
        )

    def test_refresh_is_not_blocked_by_login_rate_limit(self):
        for index in range(1, 6):
            response = self.login(
                password=f"WrongPassword{index}!",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
            )

        login_response = self.login()

        self.assertEqual(
            login_response.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS,
        )

        # Get a valid refresh token without going through the throttled
        # login endpoint by creating a token directly for the test user.
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh_token = str(
            RefreshToken.for_user(self.user),
        )

        refresh_response = self.client.post(
            self.refresh_url,
            {
                "refresh": refresh_token,
            },
            format="json",
        )

        self.assertEqual(
            refresh_response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "access",
            refresh_response.data,
        )
