from employees.models import Employee

from telegram_structure.models import (
    TelegramChat,
    TelegramChatMember,
    TelegramUser,
)

# ==========================================================
# TELEGRAM CHAT MEMBER SYNC
# ==========================================================


def sync_telegram_chat_member(message):
    """
    Синхронизирует Telegram-пользователя и его
    принадлежность к Telegram-чату.

    Employee автоматически НЕ создаётся.

    Обрабатывает только сообщения, в которых Telegram
    передал chat и from.
    """

    if not isinstance(message, dict):
        return None

    chat = message.get("chat")
    telegram_user = message.get("from")

    if not isinstance(chat, dict):
        return None

    if not isinstance(telegram_user, dict):
        return None

    chat_id = chat.get("id")
    telegram_id = telegram_user.get("id")

    if chat_id is None or telegram_id is None:
        return None

    # ======================================================
    # CHAT
    # ======================================================

    chat_type = chat.get("type")

    allowed_chat_types = {
        TelegramChat.CHAT_TYPE_PRIVATE,
        TelegramChat.CHAT_TYPE_GROUP,
        TelegramChat.CHAT_TYPE_SUPERGROUP,
        TelegramChat.CHAT_TYPE_CHANNEL,
    }

    if chat_type not in allowed_chat_types:
        return None

    title = (
        chat.get(
            "title",
            "",
        )
        or ""
    )

    username = (
        chat.get(
            "username",
            "",
        )
        or ""
    )

    telegram_chat, chat_created = TelegramChat.objects.update_or_create(
        chat_id=chat_id,
        defaults={
            "title": title,
            "username": username,
            "chat_type": chat_type,
            "is_active": True,
        },
    )

    if chat_created:
        print(
            "💬 Новый Telegram-чат сохранён: "
            f"id={chat_id}, "
            f"title={title or 'без названия'}, "
            f"type={chat_type}"
        )

    # ======================================================
    # USER
    # ======================================================

    username = (
        telegram_user.get(
            "username",
            "",
        )
        or ""
    )

    first_name = (
        telegram_user.get(
            "first_name",
            "",
        )
        or ""
    )

    last_name = (
        telegram_user.get(
            "last_name",
            "",
        )
        or ""
    )

    telegram_user_obj, user_created = TelegramUser.objects.update_or_create(
        telegram_id=telegram_id,
        defaults={
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "is_active": True,
        },
    )

    if user_created:
        print(
            "👤 Новый Telegram-пользователь сохранён: "
            f"id={telegram_id}, "
            f"username=@{username if username else 'нет'}"
        )

    # ======================================================
    # CHAT MEMBER
    # ======================================================

    membership, membership_created = TelegramChatMember.objects.update_or_create(
        chat=telegram_chat,
        user=telegram_user_obj,
        defaults={
            "is_active": True,
        },
    )

    if membership_created:
        print(
            "👥 Новый участник Telegram-чата сохранён: "
            f"user_id={telegram_id}, "
            f"chat_id={chat_id}"
        )

    # ======================================================
    # RETURN
    # ======================================================

    return {
        "chat": telegram_chat,
        "user": telegram_user_obj,
        "membership": membership,
    }


# ==========================================================
# REGISTER TELEGRAM EMPLOYEE
# ==========================================================


def register_telegram_employee(message):
    """
    Регистрирует Telegram-пользователя как сотрудника.

    Employee создаётся только после команды /register.
    """

    if not isinstance(message, dict):
        return None

    chat = message.get("chat")
    telegram_user = message.get("from")

    if not isinstance(chat, dict):
        return None

    if not isinstance(telegram_user, dict):
        return None

    chat_id = chat.get("id")
    telegram_id = telegram_user.get("id")

    if chat_id is None or telegram_id is None:
        return None

    # ======================================================
    # ПРОВЕРЯЕМ ТИП ЧАТА
    # ======================================================

    chat_type = chat.get("type")

    if chat_type not in {
        TelegramChat.CHAT_TYPE_GROUP,
        TelegramChat.CHAT_TYPE_SUPERGROUP,
    }:
        return {
            "success": False,
            "reason": "group_only",
        }

    # ======================================================
    # СИНХРОНИЗИРУЕМ TELEGRAM STRUCTURE
    # ======================================================

    synced = sync_telegram_chat_member(message)

    if synced is None:
        return None

    telegram_user_obj = synced["user"]

    # ======================================================
    # ДАННЫЕ TELEGRAM-ПОЛЬЗОВАТЕЛЯ
    # ======================================================

    username = (
        telegram_user.get(
            "username",
            "",
        )
        or ""
    )

    first_name = (
        telegram_user.get(
            "first_name",
            "",
        )
        or ""
    )

    last_name = (
        telegram_user.get(
            "last_name",
            "",
        )
        or ""
    )

    # ======================================================
    # ИМЯ СОТРУДНИКА
    # ======================================================

    employee_name = " ".join(
        part
        for part in [
            first_name,
            last_name,
        ]
        if part
    ).strip()

    if not employee_name:
        employee_name = username or f"Telegram {telegram_id}"

    # ======================================================
    # ПРОВЕРЯЕМ СУЩЕСТВУЮЩЕГО СОТРУДНИКА
    # ======================================================

    employee = Employee.objects.filter(
        telegram_id=telegram_id,
    ).first()

    if employee:
        employee.name = employee_name
        employee.telegram_username = username
        employee.is_active = True

        employee.save(
            update_fields=[
                "name",
                "telegram_username",
                "is_active",
                "updated_at",
            ]
        )

        print(
            "🔄 Сотрудник уже существует, "
            "данные обновлены: "
            f"{employee.name} "
            f"(telegram_id={telegram_id})"
        )

        return {
            "success": True,
            "created": False,
            "employee": employee,
            "telegram_user": telegram_user_obj,
        }

    # ======================================================
    # СОЗДАЁМ НОВОГО СОТРУДНИКА
    # ======================================================

    employee = Employee.objects.create(
        name=employee_name,
        position="Сантехник",
        experience=0,
        telegram_id=telegram_id,
        telegram_username=username,
        is_active=True,
    )

    print(
        "👷 Новый сотрудник зарегистрирован: "
        f"{employee.name} "
        f"(telegram_id={telegram_id})"
    )

    return {
        "success": True,
        "created": True,
        "employee": employee,
        "telegram_user": telegram_user_obj,
    }


# ==========================================================
# SAVED GROUP MEMBERS
# ==========================================================


def get_saved_group_members(chat_id):
    """
    Возвращает сохранённых активных участников
    Telegram-чата.

    Важно:
    функция работает только с теми пользователями,
    которые уже были обнаружены ботом и сохранены
    в TelegramChatMember.
    """

    if chat_id is None:
        return []

    memberships = (
        TelegramChatMember.objects.select_related(
            "chat",
            "user",
        )
        .filter(
            chat__chat_id=chat_id,
            chat__is_active=True,
            is_active=True,
            user__is_active=True,
        )
        .order_by(
            "user__first_name",
            "user__last_name",
            "user__telegram_id",
        )
    )

    return list(memberships)
