from employees.models import Employee

from telegram_clients.models import TelegramClient

from telegram_structure.models import TelegramUser

from ..client_handlers import (

    send_client_menu as send_client_ui_menu,

)

from ..services import TelegramBotError

from .common import (

    get_telegram_display_name,

    get_telegram_user_language,

    normalize_language,

    sync_telegram_user,

)

from .employee import get_employee_group_keyboard

# ==========================================================

# МУЛЬТИЯЗЫЧНЫЕ ТЕКСТЫ

# ==========================================================

EMPLOYEE_GREETING_TEXT = {

    "ru": (

        "👋 Привет, \\<b>{name}\\</b>!\n\n"

        "Вы уже привязаны к системе "

        "«Изумруд Сервис» как сотрудник.\n\n"

        "🔔 Теперь бот будет присылать "

        "вам новые заявки."

    ),

    "uz": (

        "👋 Salom, \\<b>{name}\\</b>!\n\n"

        "Siz «Izumrud Service» tizimiga "

        "xodim sifatida biriktirilgansiz.\n\n"

        "🔔 Endi bot sizga yangi buyurtmalarni "

        "yuboradi."

    ),

    "en": (

        "👋 Hello, \\<b>{name}\\</b>!\n\n"

        "You are already linked to "

        "«Emerald Service» as an employee.\n\n"

        "🔔 The bot will now send you "

        "new service requests."

    ),

    "zh": (

        "👋 您好，\\<b>{name}\\</b>！\n\n"

        "您的 Telegram 已经与 "

        "「Izumrud Service」员工账户绑定。\n\n"

        "🔔 现在机器人将向您发送新的服务请求。"

    ),

}

EMPLOYEE_GROUP_TEXT = {

    "ru": "🚰 Рабочая группа сантехников:",

    "uz": "🚰 Santexniklar ishchi guruhi:",

    "en": "🚰 Plumbers' work group:",

    "zh": "🚰 水管工工作群组：",

}

INACTIVE_EMPLOYEE_TEXT = {

    "ru": (

        "⚠️ Этот Telegram уже привязан "

        "к профилю сотрудника.\n\n"

        "Профиль сотрудника сейчас неактивен "

        "или требует проверки администратора."

    ),

    "uz": (

        "⚠️ Ushbu Telegram xodim profiliga "

        "allaqachon biriktirilgan.\n\n"

        "Xodim profili hozir faol emas "

        "yoki administrator tekshiruvini talab qiladi."

    ),

    "en": (

        "⚠️ This Telegram account is already "

        "linked to an employee profile.\n\n"

        "The employee profile is currently inactive "

        "or requires administrator review."

    ),

    "zh": (

        "⚠️ 此 Telegram 已经绑定到员工账户。\n\n"

        "员工账户目前未启用，"

        "或者需要管理员检查。"

    ),

}

WELCOME_TEXT = {

    "ru": "Добро пожаловать в «Изумруд Сервис».",

    "uz": "«Izumrud Service»ga xush kelibsiz.",

    "en": "Welcome to «Emerald Service».",

    "zh": "欢迎来到「Izumrud Service」。",

}

NEW_CLIENT_TEXT = {

    "ru": "📱 Отправьте свой номер телефона, чтобы продолжить.",

    "uz": "📱 Davom etish uchun telefon raqamingizni yuboring.",

    "en": "📱 Please send your phone number to continue.",

    "zh": "📱 请发送您的电话号码以继续。",

}

CONTACT_BUTTON_TEXT = {

    "ru": "📱 Отправить номер телефона",

    "uz": "📱 Telefon raqamimni yuborish",

    "en": "📱 Send my phone number",

    "zh": "📱 发送我的电话号码",

}

LANGUAGE_SELECTION_TEXT = {

    "ru": (

        "🌐 \\<b>Выберите язык\\</b>\n\n"

        "Выберите язык, на котором бот будет "

        "общаться с вами:"

    ),

    "uz": (

        "🌐 \\<b>Tilni tanlang\\</b>\n\n"

        "Bot siz bilan qaysi tilda muloqot "

        "qilishini tanlang:"

    ),

    "en": (

        "🌐 \\<b>Choose your language\\</b>\n\n"

        "Choose the language you want the bot "

        "to use when communicating with you:"

    ),

    "zh": ("🌐 \\<b>选择语言\\</b>\n\n" "请选择机器人与您交流时使用的语言："),

}

LANGUAGE_BUTTONS = {

    "ru": "🇷🇺 Русский",

    "uz": "🇺🇿 O'zbekcha",

    "en": "🇬🇧 English",

    "zh": "🇨🇳 中文",

}

# ==========================================================

# ЯЗЫК

# ==========================================================

def get_language(language, default="ru"):

    """

    Возвращает поддерживаемый язык.

    """

    normalized_language = normalize_language(language)

    if normalized_language:

        return normalized_language

    return default

# ==========================================================

# КЛАВИАТУРА ВЫБОРА ЯЗЫКА

# ==========================================================

def get_language_keyboard():

    """

    Inline-клавиатура выбора языка.

    """

    return {

        "inline_keyboard": [

            [

                {

                    "text": LANGUAGE_BUTTONS["ru"],

                    "callback_data": "language:ru",

                },

                {

                    "text": LANGUAGE_BUTTONS["uz"],

                    "callback_data": "language:uz",

                },

            ],

            [

                {

                    "text": LANGUAGE_BUTTONS["en"],

                    "callback_data": "language:en",

                },

                {

                    "text": LANGUAGE_BUTTONS["zh"],

                    "callback_data": "language:zh",

                },

            ],

        ],

    }

def get_language_selection_keyboard():

    """

    Возвращает inline-клавиатуру выбора языка.

    """

    return get_language_keyboard()

# ==========================================================

# КЛАВИАТУРА ТЕЛЕФОНА

# ==========================================================

def get_contact_keyboard(language):

    """

    Возвращает reply-клавиатуру для отправки телефона.

    """

    language = get_language(language)

    return {

        "keyboard": [

            [

                {

                    "text": CONTACT_BUTTON_TEXT[language],

                    "request_contact": True,

                },

            ],

        ],

        "resize_keyboard": True,

        "one_time_keyboard": True,

    }

# ==========================================================

# ВЫБОР ЯЗЫКА

# ==========================================================

def send_language_selection(

    bot,

    telegram_id,

    language="ru",

):

    """

    Показывает пользователю выбор языка.

    Уже привязанному сотруднику общий выбор языка не показываем:

    его Telegram должен обслуживаться как сотрудник, а не как новый

    клиент.

    """

    linked_employee = Employee.objects.filter(

        telegram_id=telegram_id,

    ).first()

    if linked_employee is not None:

        employee_language = get_language(

            linked_employee.language,

            default="ru",

        )

        if linked_employee.is_active:

            employee_greeting = EMPLOYEE_GREETING_TEXT.get(

                employee_language,

                EMPLOYEE_GREETING_TEXT["ru"],

            ).format(

                name=linked_employee.name,

            )

            bot.send_message(

                telegram_id,

                employee_greeting,

            )

            group_keyboard = get_employee_group_keyboard()

            if group_keyboard:

                group_text = EMPLOYEE_GROUP_TEXT.get(

                    employee_language,

                    EMPLOYEE_GROUP_TEXT["ru"],

                )

                bot.send_message(

                    telegram_id,

                    group_text,

                    reply_markup=group_keyboard,

                )

        else:

            inactive_text = INACTIVE_EMPLOYEE_TEXT.get(

                employee_language,

                INACTIVE_EMPLOYEE_TEXT["ru"],

            )

            bot.send_message(

                telegram_id,

                inactive_text,

            )

        return

    language = get_language(language)

    bot.send_message(

        telegram_id,

        LANGUAGE_SELECTION_TEXT[language],

        reply_markup=get_language_selection_keyboard(),

    )

# ==========================================================

# ЗАПРОС ТЕЛЕФОНА

# ==========================================================

def send_client_phone_request(

    bot,

    telegram_id,

    language,

    display_name="",

):

    """

    Показывает пользователю запрос номера телефона

    на выбранном языке.

    """

    language = get_language(language)

    if language == "ru":

        greeting = f"👋 Привет" f"{', ' + display_name if display_name else ''}!"

    elif language == "uz":

        greeting = f"👋 Salom" f"{', ' + display_name if display_name else ''}!"

    elif language == "en":

        greeting = f"👋 Hello" f"{', ' + display_name if display_name else ''}!"

    else:

        greeting = f"👋 您好" f"{display_name if display_name else ''}！"

    bot.send_message(

        telegram_id,

        (

            f"{greeting}\n\n"

            f"{WELCOME_TEXT[language]}\n\n"

            f"{NEW_CLIENT_TEXT[language]}"

        ),

        reply_markup=get_contact_keyboard(language),

    )

# ==========================================================

# /start

# ==========================================================

def handle_start(

    bot,

    message,

):

    """

    Обрабатывает команду /start.

    Логика:

    1\\. Активный сотрудник -> меню сотрудника.

    2\\. Неактивный сотрудник -> предупреждение.

    3\\. Существующий TelegramClient -> клиентское меню.

    4\\. Новый пользователь без выбранного языка

       -> выбор языка.

    5\\. Новый пользователь с выбранным языком

       -> запрос телефона.

    Для нового пользователя:

        /start

            ↓

        выбор языка

            ↓

        TelegramUser.language

            ↓

        TelegramUser.language_selected = True

            ↓

        запрос телефона

            ↓

        TelegramClient.language

    """

    telegram_user = message.get(

        "from",

        {},

    )

    telegram_id = telegram_user.get(

        "id",

    )

    username = telegram_user.get(

        "username",

        "",

    )

    if not telegram_id:

        print("❌ handle_start(): " "отсутствует telegram_id")

        return

    # ======================================================

    # СОХРАНЯЕМ TELEGRAM USER

    # ======================================================

    telegram_user_obj = sync_telegram_user(

        telegram_user,

    )

    print(f"🚀 handle_start(): " f"Telegram ID={telegram_id}")

    # ======================================================

    # АКТИВНЫЙ СОТРУДНИК

    # ======================================================

    employee = Employee.objects.filter(

        telegram_id=telegram_id,

        is_active=True,

    ).first()

    if employee:

        print(f"👷 Найден сотрудник: " f"{employee.name}")

        new_username = username or ""

        if employee.telegram_username != new_username:

            employee.telegram_username = new_username

            employee.save(

                update_fields=[

                    "telegram_username",

                    "updated_at",

                ],

            )

        employee_language = get_language(

            employee.language,

            default="ru",

        )

        employee_greeting = EMPLOYEE_GREETING_TEXT.get(

            employee_language,

            EMPLOYEE_GREETING_TEXT["ru"],

        ).format(

            name=employee.name,

        )

        bot.send_message(

            telegram_id,

            employee_greeting,

        )

        group_keyboard = get_employee_group_keyboard()

        if group_keyboard:

            group_text = EMPLOYEE_GROUP_TEXT.get(

                employee_language,

                EMPLOYEE_GROUP_TEXT["ru"],

            )

            bot.send_message(

                telegram_id,

                group_text,

                reply_markup=group_keyboard,

            )

        return

    # ======================================================

    # НЕАКТИВНЫЙ СОТРУДНИК

    # ======================================================

    linked_employee = Employee.objects.filter(

        telegram_id=telegram_id,

    ).first()

    if linked_employee:

        print("⚠️ Найден неактивный сотрудник: " f"{linked_employee.name}")

        employee_language = get_language(

            linked_employee.language,

            default="ru",

        )

        inactive_text = INACTIVE_EMPLOYEE_TEXT.get(

            employee_language,

            INACTIVE_EMPLOYEE_TEXT["ru"],

        )

        bot.send_message(

            telegram_id,

            inactive_text,

        )

        return

    # ======================================================

    # TELEGRAM CLIENT

    # ======================================================

    client = TelegramClient.objects.filter(

        telegram_id=telegram_id,

    ).first()

    if client:

        print("👤 Найден TelegramClient: " f"{client.name} / {client.phone}")

        new_username = username or ""

        new_name = get_telegram_display_name(

            telegram_user,

        )

        update_fields = []

        if client.telegram_username != new_username:

            client.telegram_username = new_username

            update_fields.append(

                "telegram_username",

            )

        if new_name and client.name != new_name:

            client.name = new_name

            update_fields.append(

                "name",

            )

        if update_fields:

            update_fields.append(

                "updated_at",

            )

            client.save(

                update_fields=update_fields,

            )

        print("📋 Вызываю " "send_client_ui_menu()...")

        try:

            result = send_client_ui_menu(

                bot,

                telegram_id,

                client,

            )

            print("✅ send_client_ui_menu() " f"завершён: {result!r}")

            # ======================================================
            # УДАЛЯЕМ /start ПОСЛЕ УСПЕШНОГО ОТКРЫТИЯ МЕНЮ
            # ======================================================

            start_message_id = message.get("message_id")

            if start_message_id:
                try:
                    bot.delete_message(
                        chat_id=telegram_id,
                        message_id=start_message_id,
                    )

                    print(
                        "🗑️ Удалено сообщение /start: "
                        f"message_id={start_message_id}"
                    )

                except Exception as exc:
                    print(
                        "⚠️ Не удалось удалить сообщение /start: "
                        f"{exc}"
                    )

        except TelegramBotError as exc:

            print("❌ Ошибка " "send_client_ui_menu(): " f"{exc}")

            raise

        return

    # ======================================================

    # НОВЫЙ ПОЛЬЗОВАТЕЛЬ

    # ======================================================

    print("🆕 TelegramClient не найден.")

    # ======================================================

    # ПРОВЕРЯЕМ TELEGRAM USER

    # ======================================================

    if telegram_user_obj is None:

        print("❌ Не удалось получить " "TelegramUser.")

        return

    # ======================================================

    # ЯЗЫК ПОЛЬЗОВАТЕЛЯ

    # ======================================================

    language = get_telegram_user_language(

        telegram_id,

    )

    language = get_language(

        language,

        default="ru",

    )

    print("🌐 Язык Telegram-пользователя: " f"{language}")

    print("🌐 Язык выбран: " f"{telegram_user_obj.language_selected}")

    # ======================================================

    # НОВЫЙ ПОЛЬЗОВАТЕЛЬ БЕЗ ВЫБРАННОГО ЯЗЫКА

    # ======================================================

    if not telegram_user_obj.language_selected:

        print("🌐 Язык ещё не выбран. " "Показываем выбор языка.")

        send_language_selection(

            bot,

            telegram_id,

            language="ru",

        )

        return

    # ======================================================

    # ЯЗЫК УЖЕ ВЫБРАН

    # ======================================================

    display_name = get_telegram_display_name(

        telegram_user,

    )

    print("📱 Запрашиваем номер телефона " f"на языке {language}.")

    send_client_phone_request(

        bot,

        telegram_id,

        language,

        display_name=display_name,

    )
