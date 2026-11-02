from telegram_clients.models import TelegramClient

from ..services import TelegramBotError
from .common import (
    edit_client_screen,
    get_client_by_telegram_id,
    get_ui_message_id,
)
from .keyboards import get_skip_inline_keyboard
from .requests import send_client_request_preview
from .translations import t


def _delete_comment_prompt_message(bot, telegram_id, client):
    """Удаляет старый экран бота «Request comment» с кнопками Skip/Cancel."""
    prompt_message_id = get_ui_message_id(client)

    if not prompt_message_id:
        return

    try:
        bot.delete_message(
            telegram_id,
            int(prompt_message_id),
        )

        print(
            "🗑️ Удалён экран комментария с кнопками: "
            f"message_id={prompt_message_id}"
        )

    except TelegramBotError as exc:
        print(
            "⚠️ Не удалось удалить экран комментария: "
            f"message_id={prompt_message_id}, error={exc}"
        )

    except Exception as exc:
        print(
            "⚠️ Ошибка удаления экрана комментария: "
            f"message_id={prompt_message_id}, error={exc}"
        )


def _delete_location_received_message(bot, telegram_id, client):
    """
    Удаляет сообщение бота «📍 Location received.»,
    которое было отправлено после получения геолокации.
    """

    try:
        location_received_message_id = client.get_draft_value(
            "location_received_message_id"
        )

    except Exception as exc:
        print(
            "⚠️ Не удалось получить location_received_message_id: "
            f"{exc}"
        )
        return

    if not location_received_message_id:
        print(
            "ℹ️ location_received_message_id отсутствует — "
            "удалять нечего."
        )
        return

    try:
        bot.delete_message(
            telegram_id,
            int(location_received_message_id),
        )

        print(
            "🗑️ Удалено сообщение 'Location received.': "
            f"message_id={location_received_message_id}"
        )

    except TelegramBotError as exc:
        print(
            "⚠️ Не удалось удалить сообщение 'Location received.': "
            f"message_id={location_received_message_id}, error={exc}"
        )

    except Exception as exc:
        print(
            "⚠️ Ошибка удаления сообщения 'Location received.': "
            f"message_id={location_received_message_id}, error={exc}"
        )

    finally:
        try:
            client.set_draft_value(
                "location_received_message_id",
                None,
            )
        except Exception:
            pass


def _clear_ui_message_reference(client):
    """Очищает ссылку на удалённый Telegram UI message."""

    try:
        client.set_draft_value(
            "ui_message_id",
            None,
        )

    except Exception:
        pass


def handle_client_comment(
    bot,
    telegram_id,
    text,
    client=None,
    message_id=None,
):
    client = client or get_client_by_telegram_id(
        telegram_id
    )

    if client is None:
        return

    comment = (text or "").strip()

    # ==========================================================
    # SKIP
    # ==========================================================
    #
    # ВАЖНО:
    # При Skip НЕ удаляем экран комментария.
    #
    # message_id здесь — это message_id сообщения БОТА
    # с кнопками Skip/Cancel.
    #
    # Мы превращаем именно этот экран в Preview.
    #
    # Это позволяет избежать delete_message(), который
    # в данном сценарии провоцирует появление /start.
    #
    # ==========================================================

    if comment == t(client, "skip"):
        comment = ""

        # Сохраняем пустой комментарий.
        client.set_draft_value(
            "comment",
            comment,
        )

        # При Skip сообщения клиента с комментарием нет.
        # Поэтому старый comment_message_id не должен попасть
        # в подтверждение следующей заявки.
        client.set_draft_value(
            "comment_message_id",
            None,
        )

        # Переходим в состояние подтверждения.
        client.set_flow_state(
            TelegramClient.FLOW_CONFIRMING
        )

        # Используем именно message_id экрана комментария.
        prompt_message_id = (
            message_id
            or get_ui_message_id(client)
        )

        print(
            "⏭️ Клиент нажал Skip. "
            "Не удаляем экран комментария. "
            f"Редактируем message_id={prompt_message_id}"
        )

        # Превращаем существующий экран комментария
        # непосредственно в Preview.
        preview_result = send_client_request_preview(
            bot,
            telegram_id,
            client=client,
            message_id=prompt_message_id,
        )

        # Preview уже заменил экран комментария.
        # Не выполняем дополнительный deleteMessage здесь:
        # это лишний сетевой запрос и ранее удаления сообщений
        # были связаны с появлением неожиданных /start.
        return preview_result

    # ==========================================================
    # ОБЫЧНЫЙ КОММЕНТАРИЙ
    # ==========================================================

    # Проверяем максимальную длину комментария.
    if len(comment) > 5000:
        return edit_client_screen(
            bot,
            telegram_id,
            t(
                client,
                "comment_too_long",
            ),
            reply_markup=get_skip_inline_keyboard(
                client
            ),
            client=client,
            message_id=message_id,
        )

    # Сохраняем комментарий.
    client.set_draft_value(
        "comment",
        comment,
    )

    # ==========================================================
    # ВАЖНО:
    # НЕ УДАЛЯЕМ сообщение клиента с комментарием ЗДЕСЬ.
    #
    # message_id здесь — именно ID сообщения,
    # которое написал клиент.
    #
    # Сохраняем его в draft_data.
    #
    # После успешного нажатия «Подтвердить заявку»
    # requests.py удалит это сообщение вместе с остальными
    # промежуточными сообщениями.
    # ==========================================================

    if message_id:
        client.set_draft_value(
            "comment_message_id",
            message_id,
        )

        print(
            "📝 Сохранён message_id комментария клиента "
            "для удаления после подтверждения: "
            f"message_id={message_id}"
        )
    else:
        client.set_draft_value(
            "comment_message_id",
            None,
        )

        print(
            "ℹ️ message_id комментария клиента отсутствует — "
            "удалять нечего."
        )

    # ----------------------------------------------------------
    # УДАЛЯЕМ ЭКРАН КОММЕНТАРИЯ
    # ----------------------------------------------------------

    _delete_comment_prompt_message(
        bot,
        telegram_id,
        client,
    )

    # ----------------------------------------------------------
    # УДАЛЯЕМ "📍 Location received."
    # ----------------------------------------------------------

    _delete_location_received_message(
        bot,
        telegram_id,
        client,
    )

    # После удаления старого UI
    # очищаем его message_id.
    _clear_ui_message_reference(
        client
    )

    # Переходим к подтверждению заявки.
    client.set_flow_state(
        TelegramClient.FLOW_CONFIRMING
    )

    # Для обычного комментария Preview создаётся
    # новым сообщением бота.
    #
    # Сообщение клиента с комментарием НЕ удаляется здесь.
    # Оно будет удалено только после успешного подтверждения
    # заявки в requests.py.
    return send_client_request_preview(
        bot,
        telegram_id,
        client=client,
        message_id=None,
    )