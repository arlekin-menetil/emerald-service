from html import escape

from services.models import Service
from telegram_clients.models import TelegramClient

from .common import (
    edit_client_screen,
    get_client_by_telegram_id,
    get_localized_category_field,
    get_localized_service_field,
    set_ui_message_id,
    start_client_draft,
)
from .formatters import format_price
from .keyboards import (
    get_back_to_client_menu_keyboard,
    get_client_inline_menu_keyboard,
    get_service_keyboard,
)
from .translations import t


def send_client_menu(bot, telegram_id, client=None, message_id=None):
    client = client or get_client_by_telegram_id(telegram_id)

    if client is None:
        bot.send_message(telegram_id, t('ru', 'client_not_registered'))
        return

    menu_text = t(
        client,
        'welcome',
        name=escape(str(client.name)),
    )
    keyboard = get_client_inline_menu_keyboard(client)

    if message_id is None:
        result = bot.send_message(
            telegram_id,
            menu_text,
            reply_markup=keyboard,
        )
        new_message_id = result.get('result', {}).get('message_id')

        if new_message_id:
            set_ui_message_id(client, new_message_id)

        return result

    return edit_client_screen(
        bot,
        telegram_id,
        menu_text,
        reply_markup=keyboard,
        client=client,
        message_id=message_id,
    )


def handle_client_start(bot, telegram_id):
    client = get_client_by_telegram_id(telegram_id)

    if client is None:
        bot.send_message(
            telegram_id,
            t('ru', 'client_not_found_start'),
        )
        return

    return send_client_menu(bot, telegram_id, client)


def build_services_text(client):
    services = (
        Service.objects
        .filter(is_active=True)
        .select_related('category')
        .order_by(
            'category__sort_order',
            'sort_order',
            'name',
        )
    )

    if not services.exists():
        return None

    lines = [t(client, 'services_title'), '']
    current_category = None

    for service in services:
        category_name = (
            get_localized_category_field(service.category, 'name', client)
            if service.category
            else t(client, 'services_category_other')
        )

        if category_name != current_category:
            if current_category is not None:
                lines.append('')

            lines.append(f'<b>{escape(str(category_name))}</b>')
            current_category = category_name

        if service.price_from is not None:
            price = format_price(service.price_from)
            price_unit = get_localized_service_field(
                service,
                'price_unit',
                client,
            )

            if price_unit:
                price_text = t(
                    client,
                    'services_price_from_unit',
                    price=price,
                    unit=escape(str(price_unit)),
                )
            else:
                price_text = t(
                    client,
                    'services_price_from',
                    price=price,
                )
        else:
            price_text = t(
                client,
                'services_price_to_be_confirmed',
            )

        service_name = get_localized_service_field(
            service,
            'name',
            client,
        )
        lines.append(
            f'• {escape(str(service_name))}{price_text}'
        )

    return '\n'.join(lines)


def handle_client_services(bot, telegram_id, client=None, message_id=None):
    client = client or get_client_by_telegram_id(telegram_id)

    if client is None:
        bot.send_message(
            telegram_id,
            t('ru', 'client_not_found_start'),
        )
        return

    text = build_services_text(client) or t(client, 'services_empty')

    return edit_client_screen(
        bot,
        telegram_id,
        text,
        reply_markup=get_back_to_client_menu_keyboard(client),
        client=client,
        message_id=message_id,
    )


def handle_client_create_request(bot, telegram_id, client=None, message_id=None):
    client = client or get_client_by_telegram_id(telegram_id)

    if client is None:
        bot.send_message(
            telegram_id,
            t('ru', 'client_not_found_start'),
        )
        return

    services = (
        Service.objects
        .filter(is_active=True)
        .select_related('category')
        .order_by(
            'category__sort_order',
            'sort_order',
            'name',
        )
    )

    if not services.exists():
        return edit_client_screen(
            bot,
            telegram_id,
            t(client, 'create_request_unavailable'),
            reply_markup=get_back_to_client_menu_keyboard(client),
            client=client,
            message_id=message_id,
        )

    start_client_draft(client)

    return edit_client_screen(
        bot,
        telegram_id,
        t(client, 'create_request_title'),
        reply_markup=get_service_keyboard(client),
        client=client,
        message_id=message_id,
    )
