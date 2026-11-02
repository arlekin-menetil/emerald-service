from employees.models import Employee
from telegram_clients.models import TelegramClient
from telegram_structure.models import TelegramUser

# ==========================================================
# LANGUAGES
# ==========================================================

SUPPORTED_LANGUAGES = {
    "ru": "Русский",
    "uz": "O'zbekcha",
    "en": "English",
    "zh": "中文",
}


def normalize_language(language):
    """
    Возвращает поддерживаемый язык.

    Поддерживаем:
        ru — Русский
        uz — O'zbekcha
        en — English
        zh — 中文

    Если язык неизвестен или не указан,
    используется русский.
    """

    language = (language or "").lower().strip()

    if language in SUPPORTED_LANGUAGES:
        return language

    return "ru"


def get_language_name(language):
    """
    Возвращает название языка.
    """

    language = normalize_language(
        language,
    )

    return SUPPORTED_LANGUAGES[language]


# ==========================================================
# PHONE
# ==========================================================


def normalize_phone(phone):
    """
    Оставляет в номере только цифры.
    """

    return "".join(character for character in (phone or "") if character.isdigit())


# ==========================================================
# TELEGRAM DISPLAY NAME
# ==========================================================


def get_telegram_display_name(telegram_user):
    """
    Возвращает отображаемое имя пользователя Telegram.
    """

    first_name = telegram_user.get(
        "first_name",
        "",
    )

    last_name = telegram_user.get(
        "last_name",
        "",
    )

    display_name = " ".join(
        part
        for part in [
            first_name,
            last_name,
        ]
        if part
    )

    return display_name.strip()


# ==========================================================
# TELEGRAM USER
# ==========================================================


def sync_telegram_user(telegram_user):
    """
    Создаёт или обновляет TelegramUser.

    Сохраняет:
        - Telegram ID;
        - username;
        - first_name;
        - last_name.

    ВАЖНО:
    Существующие language и language_selected
    не перезаписываются.

    Это необходимо, чтобы выбранный пользователем
    язык сохранялся между взаимодействиями.
    """

    if not isinstance(
        telegram_user,
        dict,
    ):
        return None

    telegram_id = telegram_user.get(
        "id",
    )

    if telegram_id is None:
        return None

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

    telegram_user_obj, created = TelegramUser.objects.update_or_create(
        telegram_id=telegram_id,
        defaults={
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "is_active": True,
        },
    )

    if created:

        print(
            "👤 Новый Telegram-пользователь сохранён: "
            f"id={telegram_id}, "
            f"username=@"
            f"{username if username else 'нет'}, "
            f"language={telegram_user_obj.language}, "
            f"language_selected="
            f"{telegram_user_obj.language_selected}"
        )

    else:

        print(
            "🔄 Telegram-пользователь обновлён: "
            f"id={telegram_id}, "
            f"username=@"
            f"{username if username else 'нет'}, "
            f"language={telegram_user_obj.language}, "
            f"language_selected="
            f"{telegram_user_obj.language_selected}"
        )

    return telegram_user_obj


def get_telegram_user_language(
    telegram_user_id,
):
    """
    Возвращает язык TelegramUser.

    Если пользователь не найден,
    используется русский язык.
    """

    if not telegram_user_id:
        return "ru"

    telegram_user = TelegramUser.objects.filter(
        telegram_id=telegram_user_id,
    ).first()

    if telegram_user is None:
        return "ru"

    return normalize_language(
        telegram_user.language,
    )


def set_telegram_user_language(
    telegram_user_id,
    language,
):
    """
    Сохраняет выбранный язык TelegramUser.

    После выбора языка:
        language = выбранный язык
        language_selected = True
    """

    if not telegram_user_id:
        return False

    language = normalize_language(
        language,
    )

    telegram_user = TelegramUser.objects.filter(
        telegram_id=telegram_user_id,
    ).first()

    if telegram_user is None:

        print("⚠️ Telegram-пользователь не найден: " f"id={telegram_user_id}")

        return False

    language_changed = telegram_user.language != language

    selection_changed = telegram_user.language_selected is not True

    telegram_user.language = language
    telegram_user.language_selected = True

    telegram_user.save(
        update_fields=[
            "language",
            "language_selected",
            "updated_at",
        ],
    )

    if language_changed:

        print(
            "🌐 Язык Telegram-пользователя изменён: "
            f"id={telegram_user_id}, "
            f"language={language}"
        )

    elif selection_changed:

        print(
            "🌐 Язык Telegram-пользователя подтверждён: "
            f"id={telegram_user_id}, "
            f"language={language}"
        )

    else:

        print(
            "ℹ️ Язык Telegram-пользователя "
            "уже выбран: "
            f"id={telegram_user_id}, "
            f"language={language}"
        )

    return True


# ==========================================================
# EMPLOYEE
# ==========================================================


def find_employee_by_phone(phone):
    """
    Ищет активного сотрудника по номеру телефона.
    """

    normalized_phone = normalize_phone(
        phone,
    )

    if not normalized_phone:
        return None

    employees = Employee.objects.filter(
        is_active=True,
    )

    for employee in employees:

        employee_phone = normalize_phone(
            employee.phone,
        )

        if employee_phone == normalized_phone:
            return employee

    return None


# ==========================================================
# CLIENT
# ==========================================================


def find_client_by_phone(phone):
    """
    Ищет Telegram-клиента по номеру телефона.
    """

    normalized_phone = normalize_phone(
        phone,
    )

    if not normalized_phone:
        return None

    clients = TelegramClient.objects.all()

    for client in clients:

        client_phone = normalize_phone(
            client.phone,
        )

        if client_phone == normalized_phone:
            return client

    return None


# ==========================================================
# SERVICE REQUEST LOCATION
# ==========================================================


def clear_service_request_location(
    service_request,
):
    """
    Полностью удаляет координаты клиента из заявки.

    Используется после полного завершения работы.

    Координаты:
        - latitude -> None
        - longitude -> None

    ВАЖНО:
    Адрес заявки НЕ удаляется.

    Также не изменяются:
        - имя клиента;
        - телефон;
        - услуга;
        - время приезда;
        - комментарий;
        - статус;
        - completed_at.
    """

    if service_request.latitude is None and service_request.longitude is None:
        return False

    service_request.latitude = None
    service_request.longitude = None

    service_request.save(
        update_fields=[
            "latitude",
            "longitude",
            "updated_at",
        ],
    )

    print(
        f"🔒 Координаты заявки " f"#{service_request.id} " "удалены после завершения."
    )

    return True
