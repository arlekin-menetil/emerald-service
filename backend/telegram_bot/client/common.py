from telegram_clients.models import TelegramClient

from ..services import TelegramBotError


CLIENT_UI_MESSAGE_ID_KEY = "ui_message_id"
CLIENT_LOCATION_MESSAGE_ID_KEY = "location_message_id"
CLIENT_LATITUDE_KEY = "latitude"
CLIENT_LONGITUDE_KEY = "longitude"
CLIENT_LOCATION_RECEIVED_KEY = "location_received"
CLIENT_SELECTED_DATE_KEY = "selected_date"
CLIENT_SELECTED_TIME_KEY = "selected_time"

CLIENT_DATETIME_FORMAT = "%d.%m.%Y %H:%M"
CLIENT_DATE_STORAGE_FORMAT = "%Y-%m-%d"
CLIENT_TIME_STORAGE_FORMAT = "%H:%M"

SUPPORTED_CLIENT_LANGUAGES = {"ru", "uz", "en", "zh"}


def _get_localized_field(obj, field_name, client, default=""):
    if obj is None:
        return default

    language = getattr(client, "language", "ru") or "ru"
    if language not in SUPPORTED_CLIENT_LANGUAGES:
        language = "ru"

    localized_field = (
        field_name
        if language == "ru"
        else f"{field_name}_{language}"
    )

    value = getattr(obj, localized_field, None)

    if not value and language != "ru":
        value = getattr(obj, field_name, None)

    return value if value not in (None, "") else default


def get_localized_service_field(service, field_name, client, default=""):
    return _get_localized_field(
        service,
        field_name,
        client,
        default,
    )


def get_localized_category_field(category, field_name, client, default=""):
    return _get_localized_field(
        category,
        field_name,
        client,
        default,
    )


def get_client_by_telegram_id(telegram_id):
    if not telegram_id:
        return None

    return TelegramClient.objects.filter(
        telegram_id=telegram_id,
    ).first()


def get_ui_message_id(client):
    if client is None:
        return None

    value = client.get_draft_value(CLIENT_UI_MESSAGE_ID_KEY)

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def set_ui_message_id(client, message_id):
    if client is None or not message_id:
        return

    client.set_draft_value(
        CLIENT_UI_MESSAGE_ID_KEY,
        int(message_id),
    )


def clear_ui_message_id(client):
    if client is None:
        return

    draft = dict(client.draft_data or {})

    if CLIENT_UI_MESSAGE_ID_KEY not in draft:
        return

    del draft[CLIENT_UI_MESSAGE_ID_KEY]
    client.draft_data = draft
    client.save(update_fields=["draft_data", "updated_at"])


def get_location_message_id(client):
    if client is None:
        return None

    value = client.get_draft_value(CLIENT_LOCATION_MESSAGE_ID_KEY)

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def set_location_message_id(client, message_id):
    if client is None or not message_id:
        return

    client.set_draft_value(
        CLIENT_LOCATION_MESSAGE_ID_KEY,
        int(message_id),
    )


def clear_location_message_id(client):
    if client is None:
        return

    draft = dict(client.draft_data or {})

    if CLIENT_LOCATION_MESSAGE_ID_KEY not in draft:
        return

    del draft[CLIENT_LOCATION_MESSAGE_ID_KEY]
    client.draft_data = draft
    client.save(update_fields=["draft_data", "updated_at"])


def get_callback_message(callback_query):
    message = callback_query.get("message")

    if not message:
        return None, None

    chat = message.get("chat", {})
    return chat.get("id"), message.get("message_id")


def remember_callback_message(client, callback_query):
    chat_id, message_id = get_callback_message(callback_query)

    if message_id:
        set_ui_message_id(client, message_id)

    return chat_id, message_id


def edit_client_screen(
    bot,
    telegram_id,
    text,
    reply_markup=None,
    client=None,
    message_id=None,
):
    client = client or get_client_by_telegram_id(telegram_id)

    if client is None:
        print("❌ edit_client_screen(): клиент не найден.")
        return None

    message_id = message_id or get_ui_message_id(client)

    if message_id:
        try:
            return bot.edit_message_text(
                chat_id=telegram_id,
                message_id=message_id,
                text=text,
                reply_markup=reply_markup,
            )
        except TelegramBotError as exc:
            if "message is not modified" in str(exc).lower():
                return None

            clear_ui_message_id(client)

    result = bot.send_message(
        telegram_id,
        text,
        reply_markup=reply_markup,
    )

    new_message_id = result.get("result", {}).get("message_id")

    if new_message_id:
        set_ui_message_id(client, new_message_id)

    return result


def clear_client_draft(client):
    if client is not None:
        client.clear_draft()


def start_client_draft(client):
    old_ui_message_id = get_ui_message_id(client)

    client.start_draft()

    if old_ui_message_id:
        set_ui_message_id(client, old_ui_message_id)