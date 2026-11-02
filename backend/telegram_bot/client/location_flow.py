from telegram_clients.models import TelegramClient

from ..services import TelegramBotError

from .calendar import build_client_calendar_text, get_calendar_keyboard

from .common import (
    CLIENT_LATITUDE_KEY,
    CLIENT_LOCATION_MESSAGE_ID_KEY,
    CLIENT_LOCATION_RECEIVED_KEY,
    CLIENT_LONGITUDE_KEY,
    clear_location_message_id,
    edit_client_screen,
    get_client_by_telegram_id,
    get_location_message_id,
    get_ui_message_id,
    set_location_message_id,
)

from .keyboards import (
    get_location_keyboard,
    get_remove_location_keyboard,
)

from .location import is_valid_location, normalize_coordinate

from .menu import handle_client_create_request

from .translations import t


def _delete_location_prompt_message(bot, chat_id, message_id):
    """Удаляет старое сообщение бота с инструкцией по отправке геолокации."""

    if not message_id:
        return

    try:
        bot.delete_message(
            chat_id,
            message_id,
        )

        print(
            "🗑️ Удалено сообщение с инструкцией геолокации: "
            f"message_id={message_id}"
        )

    except TelegramBotError as exc:
        # Сообщение могло быть уже удалено пользователем/Telegram.
        print(
            "⚠️ Не удалось удалить сообщение с инструкцией геолокации: "
            f"{exc}"
        )

    except Exception as exc:
        print(
            "⚠️ Неожиданная ошибка при удалении сообщения "
            f"с инструкцией геолокации: {exc}"
        )


def _delete_client_location_message(
    bot,
    chat_id,
    message_id,
):
    """
    Удаляет входящее сообщение клиента с отправленной геолокацией.

    Координаты уже сохранены в draft_data, поэтому удаляется
    только сообщение Telegram.
    """

    if not message_id:
        return

    try:
        bot.delete_message(
            chat_id,
            message_id,
        )

        print(
            "🗑️ Удалено сообщение клиента с геолокацией: "
            f"message_id={message_id}"
        )

    except TelegramBotError as exc:
        print(
            "⚠️ Не удалось удалить сообщение клиента с геолокацией: "
            f"{exc}"
        )

    except Exception as exc:
        print(
            "⚠️ Ошибка удаления сообщения клиента с геолокацией: "
            f"{exc}"
        )


def handle_client_location_step(
    bot,
    telegram_id,
    client=None,
    message_id=None,
):
    if client is None:
        client = get_client_by_telegram_id(
            telegram_id
        )

    if client is None:
        print(
            "❌ handle_client_location_step(): "
            "клиент не найден."
        )
        return

    if not client.get_draft_value("service_id"):
        print(
            "⚠️ handle_client_location_step(): "
            "service_id отсутствует."
        )

        return handle_client_create_request(
            bot,
            telegram_id,
            client=client,
            message_id=message_id,
        )

    client.set_flow_state(
        TelegramClient.FLOW_WAITING_ADDRESS
    )

    draft = dict(
        client.draft_data or {}
    )

    for key in (
        CLIENT_LATITUDE_KEY,
        CLIENT_LONGITUDE_KEY,
        CLIENT_LOCATION_RECEIVED_KEY,
        CLIENT_LOCATION_MESSAGE_ID_KEY,
    ):
        draft.pop(
            key,
            None,
        )

    client.draft_data = draft

    client.save(
        update_fields=[
            "draft_data",
            "updated_at",
        ]
    )

    # Отправляем сразу сообщение с настоящей Telegram-кнопкой
    # request_location=True.
    #
    # Раньше здесь сначала отправлялось отдельное сообщение
    # "📍" с remove_keyboard=True, а затем уже сообщение
    # с кнопкой геолокации. Этот промежуточный шаг убран,
    # чтобы не было лишнего сообщения и конфликта с Reply Keyboard.
    try:
        result = bot.send_message(
            telegram_id,
            t(
                client,
                "location_prompt",
            ),
            reply_markup=get_location_keyboard(
                client
            ),
        )

    except TelegramBotError as exc:
        print(
            "❌ Ошибка отправки клавиатуры геолокации: "
            f"{exc}"
        )
        raise

    new_message_id = (
        result.get(
            "result",
            {},
        ).get(
            "message_id"
        )
    )

    print(
        f"📍 Новый location message_id: "
        f"{new_message_id}"
    )

    if new_message_id:
        set_location_message_id(
            client,
            new_message_id,
        )

    return result


def handle_client_location(
    bot,
    telegram_id,
    latitude,
    longitude,
    client=None,
    message_id=None,
):
    print(
        "📍 handle_client_location(): "
        f"telegram_id={telegram_id}, "
        f"latitude={latitude}, "
        f"longitude={longitude}"
    )

    if client is None:
        client = get_client_by_telegram_id(
            telegram_id
        )

    if client is None:
        print(
            "❌ Клиент для геолокации не найден."
        )
        return

    if (
        client.flow_state
        != TelegramClient.FLOW_WAITING_ADDRESS
    ):
        print(
            "⚠️ Геолокация получена вне "
            "FLOW_WAITING_ADDRESS."
        )

        bot.send_message(
            telegram_id,
            t(
                client,
                "location_not_expected",
            ),
        )

        return

    latitude = normalize_coordinate(
        latitude
    )

    longitude = normalize_coordinate(
        longitude
    )

    if not is_valid_location(
        latitude,
        longitude,
    ):
        print(
            "❌ Получены некорректные координаты."
        )

        bot.send_message(
            telegram_id,
            t(
                client,
                "location_invalid",
            ),
            reply_markup=get_location_keyboard(
                client
            ),
        )

        return

    # ==========================================================
    # SAVE LOCATION
    # ==========================================================

    client.set_draft_value(
        CLIENT_LATITUDE_KEY,
        str(latitude),
    )

    client.set_draft_value(
        CLIENT_LONGITUDE_KEY,
        str(longitude),
    )

    client.set_draft_value(
        CLIENT_LOCATION_RECEIVED_KEY,
        True,
    )

    client.set_draft_value(
        "address",
        t(
            client,
            "location_address",
        ),
    )

    client.set_flow_state(
        TelegramClient.FLOW_CHOOSING_DATE
    )

    # ==========================================================
    # CLEANUP LOCATION MESSAGES
    # ==========================================================

    # Сохраняем ID сообщения бота с инструкцией ДО очистки поля.
    # После clear_location_message_id() получить этот ID уже нельзя.
    location_message_id = get_location_message_id(
        client
    )

    # Удаляем входящее сообщение клиента с геолокацией только один раз.
    _delete_client_location_message(
        bot,
        telegram_id,
        message_id,
    )

    # Удаляем сообщение бота с инструкцией:
    # "📍 Work location / Press «Share location» below..."
    _delete_location_prompt_message(
        bot,
        telegram_id,
        location_message_id,
    )

    # Теперь ID инструкции больше не нужен.
    clear_location_message_id(
        client
    )

    # ==========================================================
    # OPEN CALENDAR
    # ==========================================================

    # Основной UI message_id хранится отдельно от сообщений геолокации.
    # Превращаем этот экран в календарь.
    stored_ui_message_id = get_ui_message_id(
        client
    )

    current_ui_message_id = stored_ui_message_id

    calendar_result = edit_client_screen(
        bot,
        telegram_id,
        build_client_calendar_text(
            client
        ),
        reply_markup=get_calendar_keyboard(
            client
        ),
        client=client,
        message_id=current_ui_message_id,
    )

    # ==========================================================
    # REPLY KEYBOARD
    # ==========================================================
    #
    # Раньше здесь отправлялось отдельное сообщение:
    # "✅ Location received."
    #
    # Затем была попытка отправить техническое сообщение
    # с текстом " " для снятия Reply Keyboard.
    #
    # Telegram отклоняет такое сообщение с ошибкой:
    #
    # Bad Request: text must be non-empty
    #
    # Кроме того, само сообщение с инструкцией геолокации
    # уже удалено выше.
    #
    # Поэтому дополнительное техническое сообщение здесь
    # больше не отправляем.

    return calendar_result


def handle_client_location_message(
    bot,
    message,
):
    """
    Обработчик Telegram-сообщения с геолокацией.

    run_telegram_bot.py передаёт сюда:

        handle_client_location_message(
            bot,
            message,
        )

    Из сообщения Telegram извлекаются:

        - chat.id
        - location.latitude
        - location.longitude
        - message_id

    После этого управление передаётся
    существующей handle_client_location().
    """

    if not isinstance(
        message,
        dict,
    ):
        print(
            "⚠️ handle_client_location_message(): "
            "message имеет некорректный тип."
        )
        return

    chat = message.get(
        "chat"
    ) or {}

    location = message.get(
        "location"
    ) or {}

    telegram_id = chat.get(
        "id"
    )

    latitude = location.get(
        "latitude"
    )

    longitude = location.get(
        "longitude"
    )

    message_id = message.get(
        "message_id"
    )

    if telegram_id is None:
        print(
            "⚠️ handle_client_location_message(): "
            "telegram_id отсутствует."
        )
        return

    if (
        latitude is None
        or longitude is None
    ):
        print(
            "⚠️ handle_client_location_message(): "
            "координаты отсутствуют."
        )
        return

    return handle_client_location(
        bot,
        telegram_id,
        latitude,
        longitude,
        message_id=message_id,
    )


def handle_client_address_step(
    bot,
    telegram_id,
    client=None,
    message_id=None,
):
    return handle_client_location_step(
        bot,
        telegram_id,
        client=client,
        message_id=message_id,
    )


def handle_client_address(
    bot,
    telegram_id,
    text,
    client=None,
    message_id=None,
):
    if client is None:
        client = get_client_by_telegram_id(
            telegram_id
        )

    if client is None:
        return

    return bot.send_message(
        telegram_id,
        t(
            client,
            "location_required",
        ),
        reply_markup=get_location_keyboard(
            client
        ),
    )