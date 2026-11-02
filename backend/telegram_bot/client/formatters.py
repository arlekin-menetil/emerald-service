from html import escape

from django.utils import timezone
from service_requests.models import ServiceRequest

from .translations import t


CLIENT_DATETIME_FORMAT = "%d.%m.%Y %H:%M"


def format_price(price):
    if price is None:
        return None

    try:
        value = int(price)
    except (TypeError, ValueError):
        return None

    return f"{value:,}".replace(",", " ") + " сум"


def format_service_price(service, client):
    if service.price_from is None:
        return t(client, "price_to_be_confirmed_short")

    price = format_price(service.price_from)

    if service.price_unit:
        return t(
            client,
            "price_from",
            price=price,
            unit=escape(str(service.price_unit)),
        )

    return t(
        client,
        "price_from_without_unit",
        price=price,
    )


def format_scheduled_at(scheduled_at, client):
    if scheduled_at is None:
        return t(client, "coordinates_not_specified")

    return timezone.localtime(scheduled_at).strftime(
        CLIENT_DATETIME_FORMAT
    )


def get_request_status_emoji(status):
    return {
        ServiceRequest.STATUS_NEW: "🆕",
        ServiceRequest.STATUS_IN_PROGRESS: "🔧",
        ServiceRequest.STATUS_COMPLETED: "✅",
        ServiceRequest.STATUS_CANCELLED: "❌",
    }.get(status, "📋")


def get_request_status_name(service_request, client):
    key = {
        ServiceRequest.STATUS_NEW: "status_new",
        ServiceRequest.STATUS_IN_PROGRESS: "status_in_progress",
        ServiceRequest.STATUS_COMPLETED: "status_completed",
        ServiceRequest.STATUS_CANCELLED: "status_cancelled",
    }.get(service_request.status, "status_unknown")

    return t(client, key)


def format_rating_stars(rating):
    try:
        rating = int(rating)
    except (TypeError, ValueError):
        return ""

    if not 1 <= rating <= 5:
        return ""

    return "⭐" * rating