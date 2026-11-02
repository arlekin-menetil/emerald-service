from html import escape

from django.db import transaction
from service_requests.models import ServiceRequest
from telegram_clients.models import TelegramClient

from .common import (
    edit_client_screen,
    get_client_by_telegram_id,
    get_localized_service_field,
    get_ui_message_id,
)
from .formatters import format_rating_stars
from .keyboards import get_client_inline_menu_keyboard
from .translations import t


def get_client_rating_keyboard(service_request, client):
    request_id = service_request.id
    return {
        'inline_keyboard': [
            [
                {
                    'text': t(client, 'rating_star', rating=1),
                    'callback_data': f'client:rate:{request_id}:1',
                },
                {
                    'text': t(client, 'rating_star', rating=2),
                    'callback_data': f'client:rate:{request_id}:2',
                },
                {
                    'text': t(client, 'rating_star', rating=3),
                    'callback_data': f'client:rate:{request_id}:3',
                },
            ],
            [
                {
                    'text': t(client, 'rating_star', rating=4),
                    'callback_data': f'client:rate:{request_id}:4',
                },
                {
                    'text': t(client, 'rating_star', rating=5),
                    'callback_data': f'client:rate:{request_id}:5',
                },
            ],
        ]
    }


def _get_rating_service_name(service_request, client):
    if service_request.service:
        return get_localized_service_field(
            service_request.service,
            'name',
            client,
        )
    return t(client, 'rating_service_fallback')


def build_client_rating_text(service_request, client):
    service_name = _get_rating_service_name(service_request, client)

    return (
        f"{t(client, 'rating_completed')}\n\n"
        f"{t(client, 'rating_request_number', request_id=service_request.id)}\n"
        f"{t(client, 'rating_service_label')}{escape(str(service_name))}\n\n"
        f"{t(client, 'rating_thanks')}\n\n"
        f"{t(client, 'rating_prompt')}\n\n"
        f"{t(client, 'rating_help')}"
    )


def build_client_rating_success_text(service_request, rating, client):
    service_name = _get_rating_service_name(service_request, client)
    stars = format_rating_stars(rating)

    return (
        f"{t(client, 'rating_success')}\n\n"
        f"{t(client, 'rating_request_number', request_id=service_request.id)}\n"
        f"{t(client, 'rating_service_label')}{escape(str(service_name))}\n\n"
        f"{t(client, 'rating_your_rating')}\n"
        f"{stars}\n\n"
        f"{t(client, 'rating_service_better')}"
    )


def handle_client_rating(
    bot,
    telegram_id,
    request_id,
    rating,
    client=None,
    message_id=None,
):
    client = client or get_client_by_telegram_id(telegram_id)
    if client is None:
        return False

    try:
        request_id = int(request_id)
        rating = int(rating)
    except (TypeError, ValueError):
        return False

    if not 1 <= rating <= 5:
        return False

    with transaction.atomic():
        service_request = (
            ServiceRequest.objects
            .select_for_update()
            .filter(
                id=request_id,
                telegram_client_id=client.id,
            )
            .first()
        )

        if service_request is None:
            return False

        if service_request.status != ServiceRequest.STATUS_COMPLETED:
            return False

        if service_request.rating is not None:
            return False

        service_request.rating = rating
        service_request.save(update_fields=['rating', 'updated_at'])

    current_message_id = message_id or get_ui_message_id(client)

    edit_client_screen(
        bot,
        telegram_id,
        build_client_rating_success_text(service_request, rating, client),
        reply_markup=get_client_inline_menu_keyboard(client),
        client=client,
        message_id=current_message_id,
    )

    return True