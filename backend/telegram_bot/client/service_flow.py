from html import escape

from services.models import Service
from telegram_clients.models import TelegramClient

from .common import (
    edit_client_screen,
    get_client_by_telegram_id,
    get_localized_service_field,
)
from .formatters import format_price
from .keyboards import get_service_continue_keyboard, get_service_keyboard
from .translations import format_price_unit, t


def handle_client_service_selected(
    bot,
    telegram_id,
    service_id,
    client=None,
    message_id=None,
):
    client = client or get_client_by_telegram_id(telegram_id)
    if client is None:
        return

    service = (
        Service.objects
        .filter(id=service_id, is_active=True)
        .select_related('category')
        .first()
    )

    if service is None:
        return edit_client_screen(
            bot,
            telegram_id,
            t(client, 'service_unavailable'),
            reply_markup=get_service_keyboard(client),
            client=client,
            message_id=message_id,
        )

    client.set_draft_value('service_id', service.id)

    if service.price_from is not None:
        client.set_draft_value(
            'estimated_price',
            int(service.price_from),
        )
    else:
        client.set_draft_value('estimated_price', None)

    client.set_flow_state(TelegramClient.FLOW_WAITING_ADDRESS)

    if service.price_from is not None:
        price = format_price(service.price_from)
        price_text = t(
            client,
            'selected_service_price',
            price=price,
        )

        price_unit = get_localized_service_field(
            service,
            'price_unit',
            client,
        )

        if price_unit:
            price_text += ' ' + escape(
                str(format_price_unit(client, price_unit))
            )
    else:
        price_text = t(
            client,
            'selected_service_price_unknown',
        )

    service_name = get_localized_service_field(
        service,
        'name',
        client,
    )

    selected_service_text = t(
        client,
        'selected_service',
        name=escape(str(service_name)),
        price_text=price_text,
    )

    return edit_client_screen(
        bot,
        telegram_id,
        selected_service_text,
        reply_markup=get_service_continue_keyboard(
            client,
            service.id,
        ),
        client=client,
        message_id=message_id,
    )