from telegram_clients.models import TelegramClient

from ..services import TelegramBotError
from .calendar import build_client_calendar_text, get_calendar_keyboard
from .common import (
    CLIENT_SELECTED_DATE_KEY,
    clear_client_draft,
    edit_client_screen,
    get_client_by_telegram_id,
    get_ui_message_id,
)
from .comment_flow import handle_client_comment
from .keyboards import (
    get_client_inline_menu_keyboard,
    get_location_keyboard,
    get_remove_location_keyboard,
    get_request_confirm_keyboard,
)
from .menu import (
    handle_client_create_request,
    handle_client_services,
    send_client_menu,
)
from .requests import handle_client_requests
from .schedule_flow import (
    build_client_time_text,
    parse_client_date,
)
from .time_slots import get_time_keyboard
from .translations import t


def _edit(
    bot,
    telegram_id,
    text,
    reply_markup,
    client,
    message_id,
):
    edit_client_screen(
        bot,
        telegram_id,
        text,
        reply_markup=reply_markup,
        client=client,
        message_id=message_id,
    )


def _menu_action(
    handler,
    bot,
    telegram_id,
    client,
    message_id,
):
    handler(
        bot,
        telegram_id,
        client=client,
        message_id=message_id,
    )


def handle_client_text(
    bot,
    message,
):
    telegram_id = message.get("from", {}).get("id")
    text = (message.get("text") or "").strip()

    if not telegram_id or not text:
        return

    client = get_client_by_telegram_id(
        telegram_id
    )

    if client is None:
        return

    # ID сообщения, которое НАПИСАЛ САМ КЛИЕНТ.
    # Нельзя использовать get_ui_message_id(client) здесь:
    # это ID сообщения БОТА (календарь/экран заявки), а не сообщения
    # пользователя с комментарием.
    incoming_message_id = message.get("message_id")

    # Отдельно сохраняем ID активного UI-сообщения бота для экранов,
    # которые нужно редактировать.
    ui_message_id = get_ui_message_id(client)

    print(
        "💬 handle_client_text(): "
        f"telegram_id={telegram_id}, "
        f"text={text!r}, "
        f"flow_state={client.flow_state}, "
        f"incoming_message_id={incoming_message_id}, "
        f"ui_message_id={ui_message_id}"
    )

    # ==========================================================
    # CANCEL
    # ==========================================================

    if text == t(client, "cancel"):
        clear_client_draft(client)

        try:
            bot.send_message(
                telegram_id,
                t(client, "request_cancelled"),
                reply_markup=get_remove_location_keyboard(),
            )
        except TelegramBotError as exc:
            print(
                "⚠️ Не удалось убрать Reply Keyboard: "
                f"{exc}"
            )

        send_client_menu(
            bot,
            telegram_id,
            client=client,
            message_id=ui_message_id,
        )

        return

    # ==========================================================
    # WAITING FOR LOCATION
    # ==========================================================

    if client.flow_state == TelegramClient.FLOW_WAITING_ADDRESS:
        bot.send_message(
            telegram_id,
            t(client, "location_text_required"),
            reply_markup=get_location_keyboard(client),
        )

        return

    # ==========================================================
    # CHOOSING DATE
    # ==========================================================

    if client.flow_state == TelegramClient.FLOW_CHOOSING_DATE:
        _edit(
            bot,
            telegram_id,
            build_client_calendar_text(client),
            get_calendar_keyboard(client),
            client,
            message_id,
        )

        return

    # ==========================================================
    # CHOOSING TIME
    # ==========================================================

    if client.flow_state == TelegramClient.FLOW_CHOOSING_TIME:
        selected_date = parse_client_date(
            client.get_draft_value(
                CLIENT_SELECTED_DATE_KEY
            )
        )

        if selected_date is None:
            client.set_flow_state(
                TelegramClient.FLOW_CHOOSING_DATE
            )

            _edit(
                bot,
                telegram_id,
                build_client_calendar_text(client),
                get_calendar_keyboard(client),
                client,
                message_id,
            )

            return

        _edit(
            bot,
            telegram_id,
            build_client_time_text(
                client,
                selected_date,
            ),
            get_time_keyboard(
                client,
                selected_date,
            ),
            client,
            message_id,
        )

        return

    # ==========================================================
    # ONLINE CONSULTATION QUESTION
    # ==========================================================
    #
    # Для онлайн-консультации адрес, дата и время не нужны.
    # callbacks.py выставляет request_type=consultation и оставляет
    # клиента в FLOW_WAITING_COMMENT. Поэтому здесь важно отличить
    # консультацию от обычного комментария к заявке.
    #
    # Автоматический перевод текста клиента НЕ выполняется.
    # Вопрос сохраняется в исходном языке клиента и передаётся
    # сотруднику как есть.

    if client.flow_state == TelegramClient.FLOW_WAITING_COMMENT:
        request_type = client.get_draft_value("request_type")

        if request_type == "consultation":
            from .requests import handle_client_consultation_question

            handle_client_consultation_question(
                bot,
                telegram_id,
                text,
                client=client,
                message_id=incoming_message_id,
            )
            return

        handle_client_comment(
            bot,
            telegram_id,
            text,
            client=client,
            message_id=incoming_message_id,
        )

        return

    # ==========================================================
    # CONFIRMING REQUEST
    # ==========================================================

    if client.flow_state == TelegramClient.FLOW_CONFIRMING:
        _edit(
            bot,
            telegram_id,
            t(client, "request_already_ready"),
            get_request_confirm_keyboard(client),
            client,
            message_id,
        )

        return

    # ==========================================================
    # MAIN MENU ACTIONS
    # ==========================================================

    actions = {
        "menu_create": handle_client_create_request,
        "menu_requests": handle_client_requests,
        "menu_services": handle_client_services,
    }

    for key, handler in actions.items():
        if text == t(client, key):
            _menu_action(
                handler,
                bot,
                telegram_id,
                client,
                message_id,
            )

            return

    # ==========================================================
    # UNKNOWN TEXT
    # ==========================================================

    _edit(
        bot,
        telegram_id,
        t(client, "unknown_command"),
        get_client_inline_menu_keyboard(client),
        client,
        message_id,
    )
