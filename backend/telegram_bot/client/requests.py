from datetime import datetime
from html import escape

from django.db import transaction
from django.utils import timezone

from services.models import Service
from service_requests.models import ServiceRequest
from telegram_clients.models import TelegramClient

from .common import (
    CLIENT_LATITUDE_KEY,
    CLIENT_LONGITUDE_KEY,
    clear_client_draft,
    edit_client_screen,
    get_client_by_telegram_id,
    get_localized_service_field,
    get_ui_message_id,
    set_ui_message_id,
)
from .formatters import (
    format_price,
    format_rating_stars,
    format_scheduled_at,
    get_request_status_emoji,
    get_request_status_name,
)
from .keyboards import (
    get_back_to_client_menu_keyboard,
    get_client_inline_menu_keyboard,
    get_request_confirm_keyboard,
)
from .location import (
    format_location_coordinates,
    get_google_maps_url,
    is_valid_location,
    normalize_coordinate,
)
from .translations import t


REQUEST_ERROR_CLIENT_NOT_FOUND = "request_error_client_not_found"
REQUEST_ERROR_SERVICE_UNAVAILABLE = "request_error_service_unavailable"
REQUEST_ERROR_LOCATION_NOT_FOUND = "request_error_location_not_found"
REQUEST_ERROR_DATETIME_INVALID = "request_error_datetime_invalid"
REQUEST_ERROR_DATETIME_PASSED = "request_error_datetime_passed"


# ==========================================================
# DRAFT DATA
# ==========================================================

def get_client_draft_service(client):
    if client is None:
        return None

    service_id = client.get_draft_value("service_id")
    if not service_id:
        return None

    return (
        Service.objects
        .filter(id=service_id, is_active=True)
        .select_related("category")
        .first()
    )


def get_client_draft_datetime(client):
    if client is None:
        return None

    value = client.get_draft_value("scheduled_at")
    if not value:
        return None

    try:
        parsed = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None

    if timezone.is_naive(parsed):
        parsed = timezone.make_aware(
            parsed,
            timezone=timezone.get_current_timezone(),
        )

    return parsed


def get_client_draft_location(client):
    if client is None:
        return None, None

    latitude = client.get_draft_value(CLIENT_LATITUDE_KEY)
    longitude = client.get_draft_value(CLIENT_LONGITUDE_KEY)

    if not is_valid_location(latitude, longitude):
        return None, None

    return (
        normalize_coordinate(latitude),
        normalize_coordinate(longitude),
    )


# ==========================================================
# SMALL HELPERS
# ==========================================================

def _delete_telegram_message(bot, telegram_id, message_id, label):
    """
    Безопасно удаляет временное сообщение из клиентского чата.
    Ошибка удаления не должна ломать создание заявки.
    """
    if not message_id:
        return False

    try:
        bot.delete_message(
            telegram_id,
            int(message_id),
        )
        print(
            f"🗑️ Удалено временное сообщение клиента: "
            f"{label}, message_id={message_id}"
        )
        return True
    except Exception as exc:
        print(
            f"⚠️ Не удалось удалить временное сообщение "
            f"{label}, message_id={message_id}: {exc}"
        )
        return False


def _delete_client_intermediate_messages(bot, telegram_id, client):
    """
    Удаляет промежуточные сообщения после успешного создания заявки.

    Важно:
    - данные заявки уже сохранены в ServiceRequest;
    - удаляются только Telegram-сообщения;
    - если конкретный ID ещё не записан текущим flow-handler'ом,
      функция просто пропускает его.
    """
    if client is None:
        return

    cleanup_keys = (
        ("location_received_message_id", "Location received"),
        ("comment_message_id", "client comment"),
    )

    for key, label in cleanup_keys:
        message_id = client.get_draft_value(key)
        if not message_id:
            continue

        deleted = _delete_telegram_message(
            bot,
            telegram_id,
            message_id,
            label,
        )

        # После успешного удаления старый ID больше не нужен.
        if deleted:
            try:
                client.set_draft_value(key, None)
            except Exception:
                pass



def _get_service_name(service, client):
    return get_localized_service_field(
        service,
        "name",
        client,
    )


def _get_price_text(service, client, unknown_key):
    if service is None or service.price_from is None:
        return t(client, unknown_key)

    price = format_price(service.price_from)
    price_unit = get_localized_service_field(
        service,
        "price_unit",
        client,
    )

    if price_unit:
        return t(
            client,
            "estimated_price_with_unit",
            price=price,
            unit=escape(str(price_unit)),
        )

    return t(
        client,
        "estimated_price",
        price=price,
    )


# ==========================================================
# REQUEST PREVIEW
# ==========================================================

def build_client_request_preview(client):
    if client is None:
        return None

    service = get_client_draft_service(client)
    if service is None:
        return None

    latitude, longitude = get_client_draft_location(client)
    if latitude is None or longitude is None:
        return None

    scheduled_at = get_client_draft_datetime(client)
    if scheduled_at is None:
        return None

    comment = (
        client.get_draft_value("comment", "") or ""
    ).strip()

    price_line = _get_price_text(
        service,
        client,
        "request_price_to_be_confirmed",
    )

    coordinates = format_location_coordinates(
        latitude,
        longitude,
    )
    google_maps_url = get_google_maps_url(
        latitude,
        longitude,
    )

    service_name = _get_service_name(
        service,
        client,
    )

    lines = [
        t(client, "request_preview_title"),
        "",
        t(client, "request_service"),
        escape(str(service_name)),
        "",
        price_line,
        "",
        t(client, "request_location"),
        t(client, "request_location_received"),
        f"<code>{coordinates}</code>",
    ]

    if google_maps_url:
        lines.append(
            f'<a href="{google_maps_url}">'
            f'{t(client, "open_map")}'
            "</a>"
        )

    lines.extend(
        [
            "",
            t(client, "request_date"),
            scheduled_at.strftime("%d.%m.%Y"),
            t(client, "request_time"),
            scheduled_at.strftime("%H:%M"),
        ]
    )

    if comment:
        lines.extend(
            [
                "",
                t(client, "request_comment"),
                escape(str(comment)),
            ]
        )

    lines.extend(
        [
            "",
            t(client, "request_price_warning"),
            t(client, "request_price_inspection"),
            "",
            t(client, "request_confirm_prompt"),
        ]
    )

    return "\n".join(lines)


def send_client_request_preview(
    bot,
    telegram_id,
    client=None,
    message_id=None,
):
    client = client or get_client_by_telegram_id(telegram_id)

    if client is None:
        return

    preview = build_client_request_preview(client)

    if preview is None:
        current_message_id = (
            message_id
            or get_ui_message_id(client)
        )

        clear_client_draft(client)

        if current_message_id:
            set_ui_message_id(
                client,
                current_message_id,
            )

        return edit_client_screen(
            bot,
            telegram_id,
            t(client, "request_invalid_draft"),
            reply_markup=get_client_inline_menu_keyboard(client),
            client=client,
            message_id=current_message_id,
        )

    return edit_client_screen(
        bot,
        telegram_id,
        preview,
        reply_markup=get_request_confirm_keyboard(client),
        client=client,
        message_id=message_id,
    )


# ==========================================================
# CREATE SERVICE REQUEST
# ==========================================================

def create_service_request_from_client(client):
    if client is None:
        raise ValueError(REQUEST_ERROR_CLIENT_NOT_FOUND)

    service = get_client_draft_service(client)
    if service is None:
        raise ValueError(REQUEST_ERROR_SERVICE_UNAVAILABLE)

    latitude, longitude = get_client_draft_location(client)
    if latitude is None or longitude is None:
        raise ValueError(REQUEST_ERROR_LOCATION_NOT_FOUND)

    scheduled_at = get_client_draft_datetime(client)
    if scheduled_at is None:
        raise ValueError(REQUEST_ERROR_DATETIME_INVALID)

    if scheduled_at <= timezone.now():
        raise ValueError(REQUEST_ERROR_DATETIME_PASSED)

    comment = (
        client.get_draft_value("comment", "") or ""
    ).strip()

    with transaction.atomic():
        service_request = ServiceRequest.objects.create(
            name=client.name,
            phone=client.phone,
            address=t(client, "location_address"),
            latitude=latitude,
            longitude=longitude,
            scheduled_at=scheduled_at,
            service=service,
            comment=comment,
            request_type=ServiceRequest.REQUEST_TYPE_SERVICE,
            status=ServiceRequest.STATUS_NEW,
            telegram_client=client,
            language=client.language,
        )

    return service_request


# ==========================================================
# CREATE ONLINE CONSULTATION
# ==========================================================

def handle_client_consultation_question(
    bot,
    telegram_id,
    text,
    client=None,
    message_id=None,
):
    """
    Создаёт онлайн-консультацию сразу после получения вопроса клиента.

    В отличие от обычной заявки:
    - не требует адрес;
    - не требует координаты;
    - не требует даты/времени;
    - не требует подтверждения через FLOW_CONFIRMING;
    - сохраняет исходный текст клиента без автоматического перевода;
    - сразу отправляет заявку сотрудникам.
    """
    client = client or get_client_by_telegram_id(telegram_id)

    if client is None:
        return

    question = (text or "").strip()

    if not question:
        return edit_client_screen(
            bot,
            telegram_id,
            t(client, "consultation_question_required"),
            client=client,
            message_id=message_id,
        )

    if len(question) > 5000:
        return edit_client_screen(
            bot,
            telegram_id,
            t(client, "consultation_question_too_long"),
            client=client,
            message_id=message_id,
        )

    service = get_client_draft_service(client)

    if service is None:
        clear_client_draft(client)

        return edit_client_screen(
            bot,
            telegram_id,
            t(
                client,
                "request_creation_failed",
                error=t(client, "callback_bad_service"),
            ),
            reply_markup=get_client_inline_menu_keyboard(client),
            client=client,
            message_id=message_id,
        )

    if service.slug != "onlayn-konsultatsiya":
        clear_client_draft(client)

        return edit_client_screen(
            bot,
            telegram_id,
            t(
                client,
                "request_creation_failed",
                error=t(client, "callback_bad_service"),
            ),
            reply_markup=get_client_inline_menu_keyboard(client),
            client=client,
            message_id=message_id,
        )

    with transaction.atomic():
        service_request = ServiceRequest.objects.create(
            name=client.name,
            phone=client.phone,
            address="",
            latitude=None,
            longitude=None,
            scheduled_at=None,
            service=service,
            comment=question,
            request_type=ServiceRequest.REQUEST_TYPE_CONSULTATION,
            status=ServiceRequest.STATUS_NEW,
            telegram_client=client,
            language=client.language,
        )

    current_message_id = (
        message_id
        or get_ui_message_id(client)
    )

    clear_client_draft(client)

    if current_message_id:
        set_ui_message_id(
            client,
            current_message_id,
        )

    service_name = _get_service_name(
        service,
        client,
    )

    success_lines = [
        t(client, "consultation_request_created"),
        "",
        t(
            client,
            "request_number",
            request_id=service_request.id,
        ),
        f"💬 {escape(str(service_name))}",
        "",
        t(client, "consultation_question_label"),
        escape(question),
        "",
        t(client, "consultation_request_sent"),
    ]

    success_text = "\n".join(success_lines)

    edit_client_screen(
        bot,
        telegram_id,
        success_text,
        reply_markup=get_client_inline_menu_keyboard(client),
        client=client,
        message_id=current_message_id,
    )

    # Store the Telegram message ID of the "request created" screen
    # directly on the ServiceRequest. This message is removed later
    # when an employee accepts the request.
    if current_message_id:
        service_request.client_request_message_id = current_message_id
        service_request.save(
            update_fields=["client_request_message_id"]
        )

    try:
        from telegram_bot.notifications import notify_new_service_request

        notify_new_service_request(service_request)

    except Exception as exc:
        print(
            "⚠️ Не удалось отправить уведомление "
            f"о новой онлайн-консультации: {exc}"
        )

    return service_request


# ==========================================================
# ERROR TRANSLATION
# ==========================================================

def _get_request_error_text(client, error_key):
    error_keys = {
        REQUEST_ERROR_CLIENT_NOT_FOUND: "callback_client_not_found",
        REQUEST_ERROR_SERVICE_UNAVAILABLE: "callback_bad_service",
        REQUEST_ERROR_LOCATION_NOT_FOUND: "location_required",
        REQUEST_ERROR_DATETIME_INVALID: "invalid_date_or_time",
        REQUEST_ERROR_DATETIME_PASSED: "date_already_passed",
    }

    translation_key = error_keys.get(error_key)

    if translation_key is None:
        return error_key

    return t(client, translation_key)


# ==========================================================
# CONFIRM REQUEST
# ==========================================================

def handle_client_confirm(
    bot,
    telegram_id,
    client=None,
    message_id=None,
):
    client = client or get_client_by_telegram_id(telegram_id)

    if client is None:
        return

    if client.flow_state != TelegramClient.FLOW_CONFIRMING:
        return edit_client_screen(
            bot,
            telegram_id,
            t(client, "request_confirmation_unavailable"),
            reply_markup=get_client_inline_menu_keyboard(client),
            client=client,
            message_id=message_id,
        )

    try:
        service_request = create_service_request_from_client(client)

    except ValueError as exc:
        current_message_id = (
            message_id
            or get_ui_message_id(client)
        )

        clear_client_draft(client)

        if current_message_id:
            set_ui_message_id(
                client,
                current_message_id,
            )

        error_text = _get_request_error_text(
            client,
            str(exc),
        )

        return edit_client_screen(
            bot,
            telegram_id,
            t(
                client,
                "request_creation_failed",
                error=escape(error_text),
            ),
            reply_markup=get_client_inline_menu_keyboard(client),
            client=client,
            message_id=current_message_id,
        )

    current_message_id = (
        message_id
        or get_ui_message_id(client)
    )

    # Удаляем промежуточные сообщения ДО очистки draft_data.
    # Эти ID должны быть записаны flow-handler'ами:
    #   location_received_message_id
    #   comment_message_id
    print(
        "🧹 Очистка промежуточных сообщений перед созданием "
        f"заявки #{service_request.id}: "
        f"location_received_message_id="
        f"{client.get_draft_value('location_received_message_id')!r}, "
        f"comment_message_id="
        f"{client.get_draft_value('comment_message_id')!r}"
    )

    _delete_client_intermediate_messages(
        bot,
        telegram_id,
        client,
    )

    clear_client_draft(client)

    if current_message_id:
        set_ui_message_id(
            client,
            current_message_id,
        )

    if service_request.service:
        service_name = _get_service_name(
            service_request.service,
            client,
        )
    else:
        service_name = t(
            client,
            "request_service_not_specified",
        )

    price_text = _get_price_text(
        service_request.service,
        client,
        "request_price_specialist_short",
    )

    coordinates = format_location_coordinates(
        service_request.latitude,
        service_request.longitude,
    )

    google_maps_url = get_google_maps_url(
        service_request.latitude,
        service_request.longitude,
    )

    success_lines = [
        t(client, "request_created"),
        "",
        t(
            client,
            "request_number",
            request_id=service_request.id,
        ),
        f"🔧 {escape(str(service_name))}",
        t(client, "request_location_success"),
        f"<code>{coordinates}</code>",
        f"📅 {format_scheduled_at(service_request.scheduled_at, client)}",
        price_text,
    ]

    if google_maps_url:
        success_lines.append(
            f'<a href="{google_maps_url}">'
            f'{t(client, "open_map")}'
            "</a>"
        )

    success_lines.extend(
        [
            "",
            t(client, "request_sent_to_specialists"),
            t(client, "request_employee_notification"),
        ]
    )

    success_text = "\n".join(success_lines)

    edit_client_screen(
        bot,
        telegram_id,
        success_text,
        reply_markup=get_client_inline_menu_keyboard(client),
        client=client,
        message_id=current_message_id,
    )

    # Сохраняем ID обычного экрана «Request created successfully!».
    # callbacks.py использует его позже, когда сантехник принимает заявку.
    if current_message_id:
        service_request.client_request_message_id = current_message_id
        service_request.save(
            update_fields=["client_request_message_id"]
        )

    try:
        from telegram_bot.notifications import (
            notify_new_service_request,
        )

        notify_new_service_request(service_request)

    except Exception as exc:
        print(
            "⚠️ Не удалось отправить "
            f"уведомление о новой заявке: {exc}"
        )

    return service_request


# ==========================================================
# CLIENT REQUESTS LIST
# ==========================================================

def build_client_requests_text(client):
    if client is None:
        return t(
            None,
            "my_requests_client_not_found",
        )

    requests = (
        ServiceRequest.objects
        .filter(telegram_client=client)
        .select_related("service")
        .order_by("-created_at")[:20]
    )

    if not requests:
        return t(client, "my_requests_empty")

    lines = [
        t(client, "my_requests_title"),
        "",
    ]

    for service_request in requests:
        emoji = get_request_status_emoji(
            service_request.status,
        )

        if service_request.service:
            service_name = _get_service_name(
                service_request.service,
                client,
            )
        else:
            service_name = t(
                client,
                "request_service_not_specified",
            )

        created_at = timezone.localtime(
            service_request.created_at,
        )

        status_name = get_request_status_name(
            service_request,
            client,
        )

        lines.extend(
            [
                f"\\<b>"
                f"{t(client, 'request_number', request_id=service_request.id)}"
                f"\\</b>",
                f"{emoji} {escape(str(status_name))}",
                f"🔧 {escape(str(service_name))}",
                t(
                    client,
                    "request_created_at",
                    date=created_at.strftime(
                        "%d.%m.%Y %H:%M"
                    ),
                ),
            ]
        )

        if service_request.scheduled_at:
            lines.append(
                t(
                    client,
                    "request_scheduled_at",
                    datetime=format_scheduled_at(
                        service_request.scheduled_at,
                        client,
                    ),
                )
            )

        if (
            service_request.latitude is not None
            and service_request.longitude is not None
        ):
            lines.append(
                f"📍 {t(client, 'request_location_received')}"
            )

            google_maps_url = get_google_maps_url(
                service_request.latitude,
                service_request.longitude,
            )

            if google_maps_url:
                lines.append(
                    f'\\<a href="{google_maps_url}">'
                    f'{t(client, "open_map")}'
                    "</a>"
                )

        if (
            service_request.request_type != ServiceRequest.REQUEST_TYPE_CONSULTATION
            and service_request.service
            and service_request.service.price_from is not None
        ):
            lines.append(
                t(
                    client,
                    "request_price_list",
                    price=format_price(
                        service_request.service.price_from,
                    ),
                )
            )

        if service_request.rating is not None:
            lines.append(
                t(
                    client,
                    "request_rating",
                    stars=format_rating_stars(
                        service_request.rating,
                    ),
                )
            )

        elif service_request.status == ServiceRequest.STATUS_COMPLETED:
            lines.append(
                t(
                    client,
                    "request_not_rated",
                )
            )

        lines.append("")

    return "\n".join(lines)


def handle_client_requests(
    bot,
    telegram_id,
    client=None,
    message_id=None,
):
    client = client or get_client_by_telegram_id(telegram_id)

    if client is None:
        bot.send_message(
            telegram_id,
            t(None, "client_not_found_start"),
        )
        return

    text = build_client_requests_text(client)

    return edit_client_screen(
        bot,
        telegram_id,
        text,
        reply_markup=get_back_to_client_menu_keyboard(client),
        client=client,
        message_id=message_id,
    )