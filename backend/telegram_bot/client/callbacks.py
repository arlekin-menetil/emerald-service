from service_requests.models import ServiceRequest
from services.models import Service
from telegram_clients.models import TelegramClient

from ..services import TelegramBotError
from .calendar import build_client_calendar_text, get_calendar_keyboard
from .common import (
    clear_client_draft,
    edit_client_screen,
    get_client_by_telegram_id,
    remember_callback_message,
    set_ui_message_id,
)
from .formatters import format_rating_stars
from .keyboards import get_remove_location_keyboard
from .requests import handle_client_confirm, handle_client_requests
from .rating import handle_client_rating
from .comment_flow import handle_client_comment
from .location_flow import handle_client_location_step
from .menu import (
    handle_client_create_request,
    handle_client_services,
    send_client_menu,
)
from .schedule_flow import (
    handle_client_date_selected,
    handle_client_time_selected,
    parse_client_time,
)
from .service_flow import handle_client_service_selected
from .translations import t


def _alert(bot, callback_id, client, key, **kwargs):
    bot.answer_callback_query(
        callback_id,
        text=t(client, key, **kwargs),
        show_alert=True,
    )


def _delete_client_message(
    bot,
    telegram_id,
    message_id,
    label="client UI",
):
    """
    Удаляет старое сообщение клиента перед переходом
    на новый экран.
    """
    if not message_id:
        return False

    try:
        bot.delete_message(
            telegram_id,
            message_id,
        )

        print(
            f"🗑️ Удалено {label}: message_id={message_id}"
        )

        return True

    except TelegramBotError as exc:
        print(
            f"⚠️ Не удалось удалить {label} "
            f"message_id={message_id}: {exc}"
        )

    except Exception as exc:
        print(
            f"⚠️ Ошибка удаления {label} "
            f"message_id={message_id}: {exc}"
        )

    return False


def _parse_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _valid_parts(
    bot,
    callback_id,
    client,
    parts,
    size,
    key,
):
    if len(parts) != size:
        _alert(
            bot,
            callback_id,
            client,
            key,
        )
        return False

    return True


def handle_client_callback(bot, callback_query):
    callback_id = callback_query.get("id")
    data = callback_query.get("data", "")
    telegram_id = callback_query.get("from", {}).get("id")

    if not callback_id or not telegram_id:
        return

    if not data.startswith("client:"):
        bot.answer_callback_query(
            callback_id,
            text=t("ru", "callback_unknown"),
            show_alert=True,
        )
        return

    print(
        f"👤 handle_client_callback(): "
        f"telegram_id={telegram_id}, data={data!r}"
    )

    client = get_client_by_telegram_id(telegram_id)

    if client is None:
        bot.answer_callback_query(
            callback_id,
            text=t("ru", "callback_client_not_found"),
            show_alert=True,
        )
        return

    _, message_id = remember_callback_message(
        client,
        callback_query,
    )

    parts = data.split(":")
    action = parts[1] if len(parts) > 1 else ""

    simple_actions = {
        "create": handle_client_create_request,
        "requests": handle_client_requests,
        "services": handle_client_services,
    }

    if action in simple_actions:
        bot.answer_callback_query(callback_id)

        simple_actions[action](
            bot,
            telegram_id,
            client=client,
            message_id=message_id,
        )
        return

    if action == "menu":
        bot.answer_callback_query(callback_id)

        clear_client_draft(client)

        if message_id:
            set_ui_message_id(
                client,
                message_id,
            )

        send_client_menu(
            bot,
            telegram_id,
            client=client,
            message_id=message_id,
        )
        return

    if action == "calendar_noop":
        bot.answer_callback_query(callback_id)
        return

    if action == "choose_date":
        if client.flow_state not in {
            TelegramClient.FLOW_CHOOSING_DATE,
            TelegramClient.FLOW_CHOOSING_TIME,
        }:
            _alert(
                bot,
                callback_id,
                client,
                "callback_calendar_unavailable",
            )
            return

        bot.answer_callback_query(callback_id)

        client.set_flow_state(
            TelegramClient.FLOW_CHOOSING_DATE
        )

        edit_client_screen(
            bot,
            telegram_id,
            build_client_calendar_text(client),
            reply_markup=get_calendar_keyboard(client),
            client=client,
            message_id=message_id,
        )
        return

    if action == "date":
        if not _valid_parts(
            bot,
            callback_id,
            client,
            parts,
            3,
            "callback_bad_date",
        ):
            return

        bot.answer_callback_query(callback_id)

        handle_client_date_selected(
            bot,
            telegram_id,
            parts[2],
            client=client,
            message_id=message_id,
        )
        return

    if action == "time":
        if not _valid_parts(
            bot,
            callback_id,
            client,
            parts,
            4,
            "callback_bad_time",
        ):
            return

        time_value = parts[3]

        if not parse_client_time(time_value):
            _alert(
                bot,
                callback_id,
                client,
                "callback_bad_time",
            )
            return

        bot.answer_callback_query(callback_id)

        handle_client_time_selected(
            bot,
            telegram_id,
            parts[2],
            time_value,
            client=client,
            message_id=message_id,
        )
        return

    if action == "rate":
        if not _valid_parts(
            bot,
            callback_id,
            client,
            parts,
            4,
            "callback_bad_rating",
        ):
            return

        request_id = _parse_int(parts[2])
        rating = _parse_int(parts[3])

        if request_id is None or rating is None:
            _alert(
                bot,
                callback_id,
                client,
                "callback_bad_rating",
            )
            return

        if not 1 <= rating <= 5:
            _alert(
                bot,
                callback_id,
                client,
                "callback_rating_range",
            )
            return

        service_request = (
            ServiceRequest.objects
            .filter(
                id=request_id,
                telegram_client=client,
            )
            .select_related("service")
            .first()
        )

        if service_request is None:
            _alert(
                bot,
                callback_id,
                client,
                "callback_request_not_found",
            )
            return

        if (
            service_request.status
            != ServiceRequest.STATUS_COMPLETED
        ):
            _alert(
                bot,
                callback_id,
                client,
                "callback_cannot_rate",
            )
            return

        if service_request.rating is not None:
            _alert(
                bot,
                callback_id,
                client,
                "callback_already_rated",
                stars=format_rating_stars(
                    service_request.rating
                ),
            )
            return

        success = handle_client_rating(
            bot,
            telegram_id,
            request_id,
            rating,
            client=client,
            message_id=message_id,
        )

        if success:
            bot.answer_callback_query(
                callback_id,
                text=t(
                    client,
                    "callback_rating_success",
                ),
                show_alert=False,
            )
        else:
            _alert(
                bot,
                callback_id,
                client,
                "callback_rating_save_failed",
            )

        return

    if action in {"service", "address"}:
        if not _valid_parts(
            bot,
            callback_id,
            client,
            parts,
            3,
            "callback_bad_service",
        ):
            return

        service_id = _parse_int(parts[2])

        if service_id is None:
            _alert(
                bot,
                callback_id,
                client,
                "callback_bad_service",
            )
            return

        if action == "service":
            bot.answer_callback_query(callback_id)

            handle_client_service_selected(
                bot,
                telegram_id,
                service_id,
                client=client,
                message_id=message_id,
            )
            return

        draft_service_id = _parse_int(
            client.get_draft_value("service_id")
        )

        if draft_service_id != service_id:
            _alert(
                bot,
                callback_id,
                client,
                "callback_session_stale",
            )

            handle_client_create_request(
                bot,
                telegram_id,
                client=client,
                message_id=message_id,
            )
            return

        # Онлайн-консультация не должна запускать обычный сценарий
        # с адресом -> датой -> временем.
        #
        # Мы оставляем callback "client:address:<service_id>"
        # совместимым со старой клавиатурой, но передаём
        # консультацию в отдельную ветку.
        service = (
            Service.objects
            .filter(
                id=service_id,
                is_active=True,
            )
            .first()
        )

        if service is None:
            _alert(
                bot,
                callback_id,
                client,
                "callback_bad_service",
            )
            return

        if service.slug == "onlayn-konsultatsiya":
            bot.answer_callback_query(callback_id)

            print(
                "💬 Callback client:address -> "
                f"online consultation для услуги {service_id}"
            )

            client.set_draft_value(
                "request_type",
                ServiceRequest.REQUEST_TYPE_CONSULTATION,
            )
            client.set_draft_value(
                "service_id",
                service.id,
            )
            client.set_draft_value(
                "address",
                None,
            )
            client.set_draft_value(
                "latitude",
                None,
            )
            client.set_draft_value(
                "longitude",
                None,
            )
            client.set_draft_value(
                "scheduled_at",
                None,
            )
            client.set_draft_value(
                "estimated_price",
                0,
            )
            client.set_draft_value(
                "comment",
                "",
            )

            # Для консультации используется тот же
            # текстовый канал ввода, но text_flow должен
            # отличать его по draft["request_type"].
            client.set_flow_state(
                TelegramClient.FLOW_WAITING_COMMENT
            )

            edit_client_screen(
                bot,
                telegram_id,
                t(
                    client,
                    "consultation_question_prompt",
                ),
                client=client,
                message_id=message_id,
            )
            return

        bot.answer_callback_query(callback_id)

        print(
            f"📍 Callback client:address "
            f"для услуги {service_id}"
        )

        # ==========================================================
        # OPEN LOCATION FLOW
        # ==========================================================
        #
        # Старый экран выбора услуги НЕ удаляем и НЕ очищаем
        # его ui_message_id.
        #
        # handle_client_location_step() отправит отдельное сообщение
        # с инструкцией по геолокации, а сохранённый ui_message_id
        # позволит после получения геолокации переиспользовать
        # старый экран для календаря.
        # ==========================================================

        handle_client_location_step(
            bot,
            telegram_id,
            client=client,
            message_id=None,
        )

        return

    if action == "skip_comment":
        if (
            client.flow_state
            != TelegramClient.FLOW_WAITING_COMMENT
        ):
            _alert(
                bot,
                callback_id,
                client,
                "callback_step_unavailable",
            )
            return

        bot.answer_callback_query(callback_id)

        handle_client_comment(
            bot,
            telegram_id,
            t(client, "skip"),
            client=client,
            message_id=message_id,
        )
        return

    if action == "confirm":
        bot.answer_callback_query(
            callback_id,
            text=t(
                client,
                "callback_confirm",
            ),
            show_alert=False,
        )

        handle_client_confirm(
            bot,
            telegram_id,
            client=client,
            message_id=message_id,
        )
        return

    if action == "edit":
        bot.answer_callback_query(callback_id)

        handle_client_create_request(
            bot,
            telegram_id,
            client=client,
            message_id=message_id,
        )
        return

    if action == "cancel":
        bot.answer_callback_query(
            callback_id,
            text=t(
                client,
                "callback_cancel",
            ),
            show_alert=False,
        )

        clear_client_draft(client)

        if message_id:
            set_ui_message_id(
                client,
                message_id,
            )

        try:
            cancel_result = bot.send_message(
                telegram_id,
                t(
                    client,
                    "request_cancelled",
                ),
                reply_markup=get_remove_location_keyboard(),
            )

            cancel_message_id = (
                cancel_result.get("result", {}).get("message_id")
            )

            if cancel_message_id:
                _delete_client_message(
                    bot,
                    telegram_id,
                    cancel_message_id,
                    label="сообщение отмены",
                )

        except TelegramBotError as exc:
            print(
                "⚠️ Не удалось убрать "
                f"Reply Keyboard: {exc}"
            )

        send_client_menu(
            bot,
            telegram_id,
            client=client,
            message_id=message_id,
        )
        return

    _alert(
        bot,
        callback_id,
        client,
        "callback_unknown",
    )