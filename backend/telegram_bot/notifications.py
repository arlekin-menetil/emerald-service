from html import escape


from django.utils import timezone


from employees.models import Employee


from service_requests.models import (
    ServiceRequest,
    ServiceRequestEmployeeResponse,
)


from .services import TelegramBot


from .client.translations import t, translate_online

# ==========================================================


# ГЕОЛОКАЦИЯ


# ==========================================================


def get_request_coordinates(service_request):
    """



    Получает координаты заявки.



    Координаты не отображаются текстом.



    Они используются только для формирования



    ссылок Google Maps и Яндекс Карт.



    """

    latitude = service_request.latitude

    longitude = service_request.longitude

    if latitude is None or longitude is None:

        return None, None

    try:

        latitude = float(latitude)

        longitude = float(longitude)

    except (TypeError, ValueError):

        return None, None

    if not (-90 <= latitude <= 90):

        return None, None

    if not (-180 <= longitude <= 180):

        return None, None

    return latitude, longitude


def get_google_maps_url(service_request):
    """



    Формирует ссылку Google Maps.



    """

    latitude, longitude = get_request_coordinates(
        service_request,
    )

    if latitude is None or longitude is None:

        return None

    return f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"


def get_yandex_maps_url(service_request):
    """



    Формирует ссылку Яндекс Карт.



    """

    latitude, longitude = get_request_coordinates(
        service_request,
    )

    if latitude is None or longitude is None:

        return None

    return f"https://yandex.ru/maps/?pt={longitude},{latitude}&z=17&l=map"


def get_location_keyboard(service_request):
    """



    Формирует только кнопки карт.



    Координаты не выводятся текстом.



    """

    keyboard = []

    google_url = get_google_maps_url(
        service_request,
    )

    yandex_url = get_yandex_maps_url(
        service_request,
    )

    if google_url:

        keyboard.append(
            [
                {
                    "text": t(get_worker_group_language(), "worker_open_google_maps"),
                    "url": google_url,
                }
            ]
        )

    if yandex_url:

        keyboard.append(
            [
                {
                    "text": t(get_worker_group_language(), "worker_open_yandex_maps"),
                    "url": yandex_url,
                }
            ]
        )

    return keyboard


# ==========================================================


# SERVICE LOCALIZATION


# ==========================================================


def _get_localized_service_field(service, field_name, language, default=""):
    """



    Возвращает локализованное поле услуги.



    Если перевод отсутствует, используется русский вариант.



    """

    if service is None:

        return default

    language = language or "ru"

    if language not in {"ru", "uz", "en", "zh"}:

        language = "ru"

    if language == "ru":

        value = getattr(service, field_name, None)

    else:

        value = getattr(service, f"{field_name}_{language}", None)

        if not value:

            value = getattr(service, field_name, None)

    return value if value not in (None, "") else default


# CLIENT LANGUAGE


# ==========================================================


CLIENT_LANGUAGE_LABELS = {
    "ru": "🇷🇺 Русский",
    "uz": "🇺🇿 O'zbekcha",
    "en": "🇬🇧 English",
    "zh": "🇨🇳 中文",
}



def get_client_language_text(service_request):
    """
    Возвращает отображаемый язык клиента
    на языке рабочей Telegram-группы.
    """
    group_language = get_worker_group_language()

    language = (
        getattr(service_request, "language", None)
        or "ru"
    )

    language = str(language).strip().lower()

    if language not in {"ru", "uz", "en", "zh"}:
        language = "ru"

    labels = {
        "ru": t(group_language, "worker_language_ru"),
        "uz": t(group_language, "worker_language_uz"),
        "en": t(group_language, "worker_language_en"),
        "zh": t(group_language, "worker_language_zh"),
    }

    return labels.get(
        language,
        language,
    )


# ==========================================================


# EMPLOYEES


# ==========================================================


def get_active_employees():
    """



    Возвращает активных сантехников,



    у которых привязан Telegram.



    """

    return Employee.objects.filter(
        is_active=True,
        telegram_id__isnull=False,
    ).order_by("name")


# ==========================================================


# EMPLOYEE RESPONSE


# ==========================================================


def get_employee_response(
    service_request,
    employee,
):
    """



    Возвращает ответ конкретного сантехника



    по заявке.



    Если ответа ещё нет —



    создаётся запись со статусом pending.



    """

    response, _ = ServiceRequestEmployeeResponse.objects.get_or_create(
        service_request=service_request,
        employee=employee,
        defaults={
            "status": ServiceRequestEmployeeResponse.STATUS_PENDING,
        },
    )

    return response


def get_employee_status_text(
    service_request,
    employee,
):
    """
    Возвращает отображаемый статус конкретного сантехника
    на языке рабочей Telegram-группы.
    """
    language = get_worker_group_language()

    response = ServiceRequestEmployeeResponse.objects.filter(
        service_request=service_request,
        employee=employee,
    ).first()

    if response is None:
        return t(language, "worker_status_waiting")

    if response.status == ServiceRequestEmployeeResponse.STATUS_ACCEPTED:
        if is_online_consultation(service_request):
            return _worker_consultation_text(language, "status")

        return t(language, "worker_status_going")

    if response.status == ServiceRequestEmployeeResponse.STATUS_DECLINED:
        return t(language, "worker_status_cannot")

    if response.status == ServiceRequestEmployeeResponse.STATUS_COMPLETED:
        return t(language, "worker_status_completed")

    return t(language, "worker_status_waiting")


# ==========================================================


# REQUEST STATUS


# ==========================================================


def get_request_status_text(service_request):
    """
    Формирует общий статус заявки на языке рабочей Telegram-группы.
    """
    language = get_worker_group_language()

    if service_request.status == ServiceRequest.STATUS_COMPLETED:
        return f"✅ <b>{t(language, 'worker_status_completed_request')}</b>"

    if service_request.status == ServiceRequest.STATUS_CANCELLED:
        return f"❌ <b>{t(language, 'worker_status_cancelled')}</b>"

    assigned_employees = service_request.employees.filter(
        is_active=True,
    ).order_by("name")

    assigned_count = assigned_employees.count()

    if assigned_count == 0:
        if service_request.status == ServiceRequest.STATUS_IN_PROGRESS:
            return f"🔧 <b>{t(language, 'worker_status_in_progress')}</b>"

        waiting_status = ("Ожидаем ответа сантехника" if language == "ru" else "Santexnik javobini kutmoqdamiz")
        return f"⏳ <b>{waiting_status}</b>"

    completed_count = ServiceRequestEmployeeResponse.objects.filter(
        service_request=service_request,
        employee__in=assigned_employees,
        status=ServiceRequestEmployeeResponse.STATUS_COMPLETED,
    ).count()

    if completed_count == assigned_count:
        return f"✅ <b>{t(language, 'worker_status_all_completed')}</b>"

    if assigned_count == 1:
        employee = assigned_employees.first()

        if is_online_consultation(service_request):
            return (
                f"💬 <b>{_worker_consultation_text(language, 'status')}</b>\n"
                f"👷 <b>{escape(employee.name)}</b>"
            )

        return (
            f"🚰 <b>{t(language, 'worker_status_assigned_one')}</b>\n"
            f"👷 Едет: <b>{escape(employee.name)}</b>"
        )

    # В штатном сценарии одновременно назначается только один сантехник.
    # Даже если в старых данных осталось несколько назначенных сотрудников,
    # в уведомлении не перечисляем всех — показываем текущего первого.
    employee = assigned_employees.first()

    if is_online_consultation(service_request):
        return (
            f"💬 <b>{_worker_consultation_text(language, 'status')}</b>\n"
            f"👷 <b>{escape(employee.name)}</b>"
        )

    return (
        f"🚰 <b>{t(language, 'worker_status_assigned_one')}</b>\n"
        f"👷 Едет: <b>{escape(employee.name)}</b>"
    )


# ==========================================================


# EMPLOYEE STATUS LIST


# ==========================================================


def format_employee_responses(service_request):
    """



    Формирует список ответов всех активных



    сантехников с привязанным Telegram.



    """

    employees = get_active_employees()

    if not employees.exists():

        return t(get_worker_group_language(), "worker_no_plumbers")

    lines = []

    for employee in employees:

        status_text = get_employee_status_text(
            service_request,
            employee,
        )

        lines.append(f"👷 {escape(employee.name)} — {status_text}")

    return "\n".join(lines)


# ==========================================================


# SCHEDULED ARRIVAL


# ==========================================================


def format_scheduled_at(service_request):
    """
    Формирует отображение желаемого времени приезда
    на языке рабочей Telegram-группы.
    """
    language = get_worker_group_language()
    scheduled_at = service_request.scheduled_at

    if scheduled_at is None:
        return f"<b>{t(language, 'worker_arrival_unknown')}</b>"

    if timezone.is_aware(scheduled_at):
        scheduled_at = timezone.localtime(scheduled_at)

    date_text = scheduled_at.strftime("%d.%m.%Y")
    time_text = scheduled_at.strftime("%H:%M")

    if language == "uz":
        return f"📅 <b>Kelish:</b> {date_text} soat {time_text}"

    return f"📅 <b>Приезд:</b> {date_text} в {time_text}"


# ==========================================================


# EMPLOYEE KEYBOARD


# ==========================================================



# ==========================================================
# ONLINE CONSULTATION HELPERS
# ==========================================================

def is_online_consultation(service_request):
    """Проверяет, является ли заявка онлайн-консультацией."""
    return (
        service_request is not None
        and service_request.request_type
        == ServiceRequest.REQUEST_TYPE_CONSULTATION
    )


_WORKER_CONSULTATION_TRANSLATIONS = {
    "ru": {
        "accept": "💬 Принять консультацию",
        "status": "💬 Консультация принята",
        "complete": "✅ Завершить консультацию",
        "question": "💬 Вопрос клиента",
        "telegram": "💬 Написать сотруднику в Telegram",
        "telegram_account": "📱 Telegram сотрудника: @{username}",
    },
    "uz": {
        "accept": "💬 Maslahatni qabul qilish",
        "status": "💬 Maslahat qabul qilindi",
        "complete": "✅ Maslahatni yakunlash",
        "question": "💬 Mijoz savoli",
        "telegram": "💬 Xodimga Telegram orqali yozish",
        "telegram_account": "📱 Xodim Telegrami: @{username}",
    },
}


def _worker_consultation_text(language, key, **kwargs):
    language = language if language in {"ru", "uz"} else "ru"
    value = _WORKER_CONSULTATION_TRANSLATIONS[language].get(key, key)
    try:
        return value.format(**kwargs)
    except (KeyError, IndexError, ValueError):
        return value


def get_employee_telegram_url(employee):
    """Возвращает прямую ссылку на Telegram сотрудника по username."""
    if employee is None:
        return None
    username = (getattr(employee, "telegram_username", None) or "").strip()
    if username.startswith("@"):
        username = username[1:]
    if not username:
        return None
    return f"https://t.me/{username}"


def get_consultation_employee_keyboard(employee, language="ru"):
    """Кнопка прямого перехода к Telegram сотрудника."""
    url = get_employee_telegram_url(employee)
    if not url:
        return {"inline_keyboard": []}

    return {
        "inline_keyboard": [
            [
                {
                    "text": _worker_consultation_text(language, "telegram"),
                    "url": url,
                }
            ]
        ]
    }


def get_employee_keyboard(service_request):
    """Формирует клавиатуру действий сотрудников."""
    if service_request.status in {
        ServiceRequest.STATUS_COMPLETED,
        ServiceRequest.STATUS_CANCELLED,
    }:
        return {"inline_keyboard": []}

    employees = list(get_active_employees())
    if not employees:
        return {"inline_keyboard": []}

    has_pending = False
    has_accepted = False
    has_changeable = False

    for employee in employees:
        response = ServiceRequestEmployeeResponse.objects.filter(
            service_request=service_request,
            employee=employee,
        ).first()

        if response is None:
            has_pending = True
        elif response.status == ServiceRequestEmployeeResponse.STATUS_PENDING:
            has_pending = True
        elif response.status == ServiceRequestEmployeeResponse.STATUS_ACCEPTED:
            has_accepted = True
            has_changeable = True
        elif response.status == ServiceRequestEmployeeResponse.STATUS_DECLINED:
            has_changeable = True

    language = get_worker_group_language()
    keyboard = []

    if has_pending:
        accept_text = (
            _worker_consultation_text(language, "accept")
            if is_online_consultation(service_request)
            else t(language, "worker_go")
        )
        keyboard.append(
            [
                {
                    "text": accept_text,
                    "callback_data": f"request_response:{service_request.id}:accepted",
                },
                {
                    "text": t(language, "worker_cannot"),
                    "callback_data": f"request_response:{service_request.id}:declined",
                },
            ]
        )

    if has_changeable:
        keyboard.append(
            [
                {
                    "text": t(language, "worker_change_answer"),
                    "callback_data": f"request_response:{service_request.id}:change",
                },
            ]
        )

    if has_accepted:
        if is_online_consultation(service_request):
            complete_text = _worker_consultation_text(
                language,
                "complete",
            )
        else:
            complete_text = t(language, "worker_completed")

        keyboard.append(
            [
                {
                    "text": complete_text,
                    "callback_data": f"request_response:{service_request.id}:completed",
                },
            ]
        )

    return {"inline_keyboard": keyboard}


# ==========================================================


# SERVICE REQUEST MESSAGE


# ==========================================================


# ==========================================================


# GROUP EMPLOYEE LANGUAGE / ADDRESS


# ==========================================================


GROUP_ADDRESS_TRANSLATIONS = {
    "ru": "Геолокация клиента",
    "uz": "Mijoz joylashuvi",
}


def _normalize_group_address(address):
    """
    Нормализует системные значения адреса/геолокации,
    которые могли быть сохранены на языке клиента.

    Реальный адрес клиента не переводится автоматически.
    Переводятся только известные системные варианты.
    """
    if not address:
        return None

    value = str(address).strip()

    if not value:
        return None

    normalized = " ".join(value.lower().split())

    known_values = {
        "геолокация клиента": "location",
        "mijoz joylashuvi": "location",
        "client location": "location",
        "地址": "location",
        "location": "location",
    }

    return known_values.get(normalized, value)


def get_group_employee_languages():
    """
    Возвращает языки активных сотрудников с Telegram.

    Сотрудники используют только:
    - ru — русский
    - uz — узбекский
    """
    languages = set()

    for employee in get_active_employees():
        language = getattr(employee, "language", None) or "ru"

        if language not in {"ru", "uz"}:
            language = "ru"

        languages.add(language)

    return languages


def get_worker_group_language():
    """
    Возвращает язык сообщений рабочей группы.

    Рабочая группа поддерживает только русский и узбекский.
    Если все активные сотрудники используют узбекский — используется uz.
    Во всех остальных случаях используется русский как язык группы
    по умолчанию. Это гарантирует, что одно общее сообщение группы
    всегда имеет один язык.
    """
    languages = get_group_employee_languages()

    if languages == {"uz"}:
        return "uz"

    return "ru"


def get_group_address(service_request):
    """
    Формирует адрес для общего сообщения рабочей Telegram-группы.

    Реальный адрес клиента не переводится автоматически.
    Системный placeholder показывается на языке группы.
    """
    address = _normalize_group_address(
        service_request.address,
    )

    if address is None:
        address = "location"

    if address != "location":
        return address

    language = get_worker_group_language()
    return GROUP_ADDRESS_TRANSLATIONS.get(
        language,
        GROUP_ADDRESS_TRANSLATIONS["ru"],
    )


# ==========================================================


# SERVICE REQUEST MESSAGE


# ==========================================================


def format_comment_translations(service_request):
    """
    Формирует комментарий клиента для общей рабочей RU/UZ-группы.

    Сотрудники группы используют только русский и узбекский языки, поэтому
    перевод показывается только тем сотрудникам, которым он действительно
    нужен:

    - клиент RU -> оригинал + перевод UZ + предупреждение для UZ;
    - клиент UZ -> оригинал + перевод RU + предупреждение для RU;
    - клиент EN/ZH -> оригинал + перевод RU и UZ с соответствующими
      предупреждениями;
    - сотруднику, говорящему на языке клиента, перевод не нужен.
    """
    comment = str(service_request.comment or "").strip()
    if not comment:
        return ""

    source_language = (
        getattr(service_request, "language", None)
        or "ru"
    )

    source_language = str(source_language).strip().lower()

    if source_language not in {"ru", "uz", "en", "zh"}:
        source_language = "ru"

    language_labels = {
        "ru": "🇷🇺 Русский",
        "uz": "🇺🇿 O'zbekcha",
        "en": "🇬🇧 English",
        "zh": "🇨🇳 中文",
    }

    # Для каждого языка клиента определяем, кому из двух типов сотрудников
    # нужен перевод. Сотрудник с тем же языком клиента перевод не получает.
    target_languages = {
        "ru": ["uz"],
        "uz": ["ru"],
        "en": ["ru", "uz"],
        "zh": ["ru", "uz"],
    }[source_language]

    lines = [
        f"🌐 <b>Оригинал ({language_labels[source_language]}):</b>",
        escape(comment),
    ]

    warning_text = {
        "ru": (
            "⚠️ <b>ВАЖНО:</b> Клиент общается на "
            f"{language_labels[source_language]}.\n"
            "При общении с клиентом используйте переводчик."
        ),
        "uz": (
            "⚠️ <b>MUHIM:</b> Mijoz "
            f"{language_labels[source_language]} tilida muloqot qiladi.\n"
            "Mijoz bilan muloqotda tarjimondan foydalaning."
        ),
    }

    for target_language in target_languages:
        try:
            translated = translate_online(
                comment,
                target_language=target_language,
                source_language=source_language,
            )
        except Exception as exc:
            print(
                "⚠️ Не удалось перевести комментарий заявки "
                f"#{service_request.id} "
                f"{source_language}->{target_language}: {exc}"
            )
            continue

        translated = str(translated or "").strip()
        if not translated or translated == comment:
            continue

        if target_language == "ru":
            translation_title = "🇷🇺 <b>Перевод для русскоязычного сотрудника:</b>"
        else:
            translation_title = "🇺🇿 <b>O‘zbek tilidagi tarjima:</b>"

        lines.extend(
            [
                "",
                translation_title,
                escape(translated),
                "",
                warning_text[target_language],
            ]
        )

    return "\n".join(lines)

# Сохраняем старое имя функции для совместимости.
def format_consultation_question_translations(service_request):
    return format_comment_translations(service_request)


def format_service_request_message(
    service_request,
):
    """
    Формирует сообщение о заявке для рабочей Telegram-группы.

    Для онлайн-консультации адрес и время приезда не показываются.
    Комментарий/вопрос клиента автоматически переводится
    на нужные языки для рабочей группы.
    """
    language = get_worker_group_language()

    service_name = (
        _get_localized_service_field(
            service_request.service,
            "name",
            language,
            default=t(language, "service_unknown"),
        )
        if service_request.service
        else t(language, "service_unknown")
    )

    comment = str(service_request.comment or "").strip()
    comment_fallback = "Izoh yo‘q" if language == "uz" else "Нет"

    request_status = get_request_status_text(service_request)
    client_language = get_client_language_text(service_request)

    lines = [
        t(language, "worker_new_request"),
        "",
        f"{t(language, 'worker_request_number')} <b>#{service_request.id}</b>",
        f"{t(language, 'worker_client')} <b>{escape(service_request.name)}</b>",
        f"{t(language, 'worker_phone')} <b>{escape(service_request.phone)}</b>",
        f"{t(language, 'worker_client_language')} <b>{escape(client_language)}</b>",
    ]

    if is_online_consultation(service_request):
        consultation_title = (
            "💬 <b>Онлайн-консультация</b>"
            if language == "ru"
            else "💬 <b>Onlayn maslahat</b>"
        )
        question_translation_block = format_comment_translations(
            service_request
        )
        if not question_translation_block:
            question_translation_block = escape(comment_fallback)
        lines.extend(
            [
                consultation_title,
                f"{t(language, 'worker_service')} <b>{escape(service_name)}</b>",
                "",
                question_translation_block,
            ]
        )
    else:
        address = get_group_address(service_request)
        scheduled_at = format_scheduled_at(service_request)
        lines.extend(
            [
                f"{t(language, 'worker_address')} <b>{escape(address)}</b>",
                f"{t(language, 'worker_service')} <b>{escape(service_name)}</b>",
                scheduled_at,
                (
                    f"{t(language, 'worker_comment')}:\n"
                    f"{format_comment_translations(service_request)}"
                    if comment
                    else f"{t(language, 'worker_comment')} {escape(comment_fallback)}"
                ),
            ]
        )

    lines.extend(
        [
            "",
            request_status,
        ]
    )

    message = "\n".join(lines)
    employee_keyboard = get_employee_keyboard(service_request)

    if employee_keyboard.get("inline_keyboard"):
        message += "\n\n" f"<b>{t(language, 'worker_action')}</b>"

    if service_request.status == ServiceRequest.STATUS_COMPLETED:
        message += f"\n\n<b>{t(language, 'worker_request_completed')}</b>"
    elif service_request.status == ServiceRequest.STATUS_CANCELLED:
        message += f"\n\n<b>{t(language, 'worker_request_closed')}</b>"

    return message


# ==========================================================


# GROUP KEYBOARD


# ==========================================================


def get_group_keyboard(service_request):
    """



    Формирует клавиатуру заявки



    для рабочей Telegram-группы.



    В группе используется одна общая



    inline-клавиатура.



    Кнопки карт доступны всем.



    Действия сотрудников проверяются



    дополнительно в callbacks.py.



    """

    # ======================================================

    # CLOSED REQUEST

    # ======================================================

    if service_request.status in {
        ServiceRequest.STATUS_COMPLETED,
        ServiceRequest.STATUS_CANCELLED,
    }:

        return {
            "inline_keyboard": [],
        }

    # ======================================================

    # EMPLOYEE ACTIONS

    # ======================================================

    employee_keyboard = get_employee_keyboard(
        service_request,
    )

    keyboard = employee_keyboard.get(
        "inline_keyboard",
        [],
    )

    # ======================================================

    # LOCATION

    # ======================================================

    location_keyboard = get_location_keyboard(
        service_request,
    )

    # ======================================================

    # FINAL KEYBOARD

    # ======================================================

    # Карты всегда идут первыми.

    keyboard = location_keyboard + keyboard

    return {
        "inline_keyboard": keyboard,
    }


# ==========================================================


# NEW SERVICE REQUEST NOTIFICATION


# ==========================================================


def notify_new_service_request(
    service_request,
):
    """



    Отправляет новую заявку



    в рабочую Telegram-группу.



    Координаты текстом не отправляются.



    Если координаты есть —



    добавляются две кнопки карт.



    """

    bot = TelegramBot()

    message = format_service_request_message(
        service_request,
    )

    keyboard = get_group_keyboard(
        service_request,
    )

    return bot.send_to_group(
        text=message,
        reply_markup=keyboard,
    )




def format_vacancy_application_message(application):
    """
    Формирует сообщение о новой заявке на вакансию
    для рабочей Telegram-группы.
    """
    language = get_worker_group_language()

    title = (
        "🟢 <b>Новая заявка на вакансию</b>"
        if language == "ru"
        else "🟢 <b>Yangi ishga ariza</b>"
    )

    language_names = {
        "ru": "Русский",
        "uz": "O‘zbekcha",
        "en": "English",
        "zh": "中文",
    }

    application_language = language_names.get(
        application.language,
        application.language,
    )

    lines = [
        title,
        "",
        f"📋 <b>Номер заявки:</b> #{application.id}",
        f"👤 <b>Имя:</b> {escape(application.name)}",
        f"📞 <b>Телефон:</b> {escape(application.phone)}",
        f"🔧 <b>Специализация:</b> {escape(application.specialization)}",
        f"💼 <b>Опыт:</b> {escape(application.experience)}",
        f"🌐 <b>Язык:</b> {escape(application_language)}",
        "",
        "📝 <b>О себе:</b>",
        escape(application.about),
    ]

    return "\n".join(lines)


def notify_new_vacancy_application(application):
    """
    Отправляет новую заявку на вакансию
    в рабочую Telegram-группу.
    """
    bot = TelegramBot()

    message = format_vacancy_application_message(
        application,
    )

    return bot.send_to_group(
        text=message,
    )

# ==========================================================


# CLIENT NOTIFICATION


# ==========================================================


# ==========================================================

# CLIENT NOTIFICATION TRANSLATIONS

# ==========================================================


# These are fallbacks for client-assignment messages.

# The main translation source remains translations.py via t().

# They prevent raw translation keys from reaching Telegram when a

# newly added key has not yet been added to translations.py.


_CLIENT_ASSIGNMENT_TRANSLATIONS = {
    "ru": {
        "employee_assigned_title": "🔧 <b>Ваша заявка принята!</b>",
        "request_number": "📋 Номер заявки: <b>№{request_id}</b>",
        "assigned_service": "🔧 <b>Услуга:</b> {service}",
        "assigned_plumber_title": "👨‍🔧 <b>Сантехник:</b>",
        "assigned_phone": "📞 <b>Телефон:</b> {phone}",
        "assigned_address": "📍 <b>Адрес:</b> {address}",
        "assigned_arrival": "🕐 <b>Время приезда:</b> {date} в {time}",
        "assigned_arrival_not_specified": "🕐 <b>Время приезда:</b> Не указано",
        "employee_assigned_success": "✅ Специалист назначен на вашу заявку.",
    },
    "uz": {
        "employee_assigned_title": "🔧 <b>Buyurtmangiz qabul qilindi!</b>",
        "request_number": "📋 Buyurtma raqami: <b>№{request_id}</b>",
        "assigned_service": "🔧 <b>Xizmat:</b> {service}",
        "assigned_plumber_title": "👨‍🔧 <b>Santexnik:</b>",
        "assigned_phone": "📞 <b>Telefon:</b> {phone}",
        "assigned_address": "📍 <b>Manzil:</b> {address}",
        "assigned_arrival": "🕐 <b>Kelish vaqti:</b> {date} soat {time}",
        "assigned_arrival_not_specified": "🕐 <b>Kelish vaqti:</b> Ko‘rsatilmagan",
        "employee_assigned_success": "✅ Buyurtmangizga mutaxassis biriktirildi.",
    },
    "en": {
        "employee_assigned_title": "🔧 <b>Your request has been accepted!</b>",
        "request_number": "📋 Request number: <b>№{request_id}</b>",
        "assigned_service": "🔧 <b>Service:</b> {service}",
        "assigned_plumber_title": "👨‍🔧 <b>Plumber:</b>",
        "assigned_phone": "📞 <b>Phone:</b> {phone}",
        "assigned_address": "📍 <b>Address:</b> {address}",
        "assigned_arrival": "🕐 <b>Arrival time:</b> {date} at {time}",
        "assigned_arrival_not_specified": "🕐 <b>Arrival time:</b> Not specified",
        "employee_assigned_success": "✅ A specialist has been assigned to your request.",
    },
    "zh": {
        "employee_assigned_title": "🔧 <b>您的订单已被接受！</b>",
        "request_number": "📋 订单编号：<b>№{request_id}</b>",
        "assigned_service": "🔧 <b>服务：</b>{service}",
        "assigned_plumber_title": "👨‍🔧 <b>水管工：</b>",
        "assigned_phone": "📞 <b>电话：</b>{phone}",
        "assigned_address": "📍 <b>地址：</b>{address}",
        "assigned_arrival": "🕐 <b>到访时间：</b>{date} {time}",
        "assigned_arrival_not_specified": "🕐 <b>到访时间：</b>未指定",
        "employee_assigned_success": "✅ 已为您的订单分配专业人员。",
    },
}


def _client_assignment_t(language, key, **kwargs):
    """

    Returns a client-assignment translation.



    First uses translations.py through t().

    If the key is not present there, or t() returns the raw key,

    the local fallback above is used.

    """

    language = language if language in _CLIENT_ASSIGNMENT_TRANSLATIONS else "ru"

    translated = t(
        language,
        key,
        **kwargs,
    )

    # Missing translation key.

    if translated == key:

        translated = _CLIENT_ASSIGNMENT_TRANSLATIONS[language].get(
            key,
            _CLIENT_ASSIGNMENT_TRANSLATIONS["ru"].get(key, key),
        )

    # t() may return an unformatted string when a placeholder name

    # does not match the kwargs passed to it.

    if "{" in translated and "}" in translated:

        fallback = _CLIENT_ASSIGNMENT_TRANSLATIONS[language].get(
            key,
            _CLIENT_ASSIGNMENT_TRANSLATIONS["ru"].get(key),
        )

        if fallback:

            try:

                translated = fallback.format(**kwargs)

            except (KeyError, IndexError, ValueError):

                pass

    return translated


# ==========================================================

# CLIENT NOTIFICATION

# ==========================================================


def format_client_employee_assigned_message(
    service_request,
    employee,
):
    """
    Формирует сообщение клиенту после назначения сотрудника.

    Для онлайн-консультации адрес и время приезда не показываются.
    Telegram сотрудника добавляется отдельной inline-кнопкой.
    """
    telegram_client = service_request.telegram_client
    language = (
        telegram_client.language
        if telegram_client is not None
        else "ru"
    ) or "ru"

    service_name = (
        _get_localized_service_field(
            service_request.service,
            "name",
            language,
            default=t(language, "service_unknown"),
        )
        if service_request.service
        else t(language, "service_unknown")
    )

    employee_name = (
        employee.name
        if employee and employee.name
        else t(language, "plumber")
    )
    employee_phone = (
        employee.phone
        if employee and employee.phone
        else ""
    )

    lines = [
        _client_assignment_t(language, "employee_assigned_title"),
        "",
        _client_assignment_t(
            language,
            "request_number",
            request_id=service_request.id,
        ),
        _client_assignment_t(
            language,
            "assigned_service",
            service=escape(service_name),
        ),
        "",
        _client_assignment_t(language, "assigned_plumber_title"),
        f"<b>{escape(employee_name)}</b>",
    ]

    if employee_phone:
        lines.append(
            _client_assignment_t(
                language,
                "assigned_phone",
                phone=escape(employee_phone),
            )
        )

    if is_online_consultation(service_request):
        username = (
            getattr(employee, "telegram_username", None) or ""
        ).strip()
        if username.startswith("@"):
            username = username[1:]

        if username:
            lines.extend(
                [
                    "",
                    _worker_consultation_text(
                        language,
                        "telegram_account",
                        username=escape(username),
                    ),
                ]
            )

        return "\n".join(lines)

    address = (
        service_request.address
        if service_request.address
        else t(language, "address_not_specified")
    )

    lines.extend(
        [
            "",
            _client_assignment_t(
                language,
                "assigned_address",
                address=escape(address),
            ),
            format_scheduled_at_localized(service_request, language),
            "",
            _client_assignment_t(
                language,
                "employee_assigned_success",
            ),
        ]
    )

    return "\n".join(lines)


def format_scheduled_at_localized(
    service_request,
    language,
):
    """



    Формирует локализованное время приезда



    для сообщения клиенту.



    """

    scheduled_at = service_request.scheduled_at

    if scheduled_at is None:

        return _client_assignment_t(
            language,
            "assigned_arrival_not_specified",
        )

    if timezone.is_aware(scheduled_at):

        scheduled_at = timezone.localtime(
            scheduled_at,
        )

    return _client_assignment_t(
        language,
        "assigned_arrival",
        date=scheduled_at.strftime("%d.%m.%Y"),
        time=scheduled_at.strftime("%H:%M"),
    )


def notify_client_employee_assigned(
    service_request,
    employee,
):
    """



    Отправляет клиенту уведомление



    о назначении сантехника.



    Язык уведомления определяется



    через TelegramClient.language.



    Если у заявки нет Telegram-клиента



    или Telegram ID —



    уведомление не отправляется.



    Координаты клиента никогда



    не отправляются.



    """

    telegram_client = service_request.telegram_client

    if telegram_client is None:

        print(
            "⚠️ notify_client_employee_assigned(): "
            f"у заявки №{service_request.id} "
            "нет Telegram-клиента."
        )

        return None

    telegram_id = telegram_client.telegram_id

    if not telegram_id:

        print(
            "⚠️ notify_client_employee_assigned(): "
            f"у клиента заявки №{service_request.id} "
            "нет Telegram ID."
        )

        return None

    bot = TelegramBot()

    message = format_client_employee_assigned_message(
        service_request,
        employee,
    )

    reply_markup = None

    if is_online_consultation(service_request):
        language = (
            telegram_client.language
            if telegram_client is not None
            else "ru"
        )
        reply_markup = get_consultation_employee_keyboard(
            employee,
            language=language,
        )

    return bot.send_message(
        chat_id=telegram_id,
        text=message,
        reply_markup=reply_markup,
    )
