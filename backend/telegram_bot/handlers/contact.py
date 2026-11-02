from employees.models import Employee
from telegram_clients.models import TelegramClient

from ..client_handlers import (
    send_client_menu as send_client_ui_menu,
)

from .common import (
    find_client_by_phone,
    find_employee_by_phone,
    get_telegram_display_name,
    get_telegram_user_language,
    sync_telegram_user,
)

from .employee import get_employee_group_keyboard

# ==========================================================
# МУЛЬТИЯЗЫЧНЫЕ ТЕКСТЫ
# ==========================================================

TEXTS = {
    "ru": {
        "own_contact": (
            "⚠️ Необходимо отправить именно "
            "свой номер телефона.\n\n"
            "Нажмите кнопку "
            "«📱 Отправить номер телефона» "
            "и выберите свой контакт."
        ),
        "phone_error": (
            "❌ Не удалось получить номер телефона.\n\n"
            "Попробуйте отправить его ещё раз."
        ),
        "employee_already_active": (
            "👋 Этот Telegram уже привязан " "к сотруднику <b>{name}</b>."
        ),
        "employee_already_inactive": (
            "⚠️ Этот Telegram привязан "
            "к неактивному профилю сотрудника.\n\n"
            "Обратитесь к администратору."
        ),
        "employee_other_telegram": (
            "⚠️ Этот сотрудник уже привязан "
            "к другому Telegram-аккаунту.\n\n"
            "Обратитесь к администратору."
        ),
        "employee_linked": (
            "✅ <b>Telegram успешно привязан!</b>\n\n"
            "👤 Сотрудник: <b>{name}</b>\n"
            "🔧 Должность: {position}\n"
            "📱 Телефон: {phone}\n\n"
            "Теперь вы будете получать уведомления "
            "о новых заявках."
        ),
        "employee_group": (
            "🚰 <b>Рабочая группа сантехников</b>\n\n"
            "Нажмите кнопку ниже, чтобы перейти "
            "в рабочую группу."
        ),
        "phone_confirmed": ("✅ <b>Телефон подтверждён!</b>"),
        "phone_already_other_telegram": (
            "⚠️ Этот номер телефона уже связан "
            "с другим Telegram-аккаунтом.\n\n"
            "Если это ваш номер — обратитесь "
            "к администратору."
        ),
    },
    "uz": {
        "own_contact": (
            "⚠️ Aynan o‘z telefon raqamingizni "
            "yuborishingiz kerak.\n\n"
            "«📱 Telefon raqamimni yuborish» "
            "tugmasini bosing va o‘z kontaktingizni tanlang."
        ),
        "phone_error": (
            "❌ Telefon raqamini olishning iloji bo‘lmadi.\n\n"
            "Iltimos, yana bir bor yuboring."
        ),
        "employee_already_active": (
            "👋 Ushbu Telegram allaqachon " "<b>{name}</b> xodimiga biriktirilgan."
        ),
        "employee_already_inactive": (
            "⚠️ Ushbu Telegram faol bo‘lmagan "
            "xodim profiliga biriktirilgan.\n\n"
            "Administratorga murojaat qiling."
        ),
        "employee_other_telegram": (
            "⚠️ Ushbu xodim allaqachon "
            "boshqa Telegram akkauntiga biriktirilgan.\n\n"
            "Administratorga murojaat qiling."
        ),
        "employee_linked": (
            "✅ <b>Telegram muvaffaqiyatli biriktirildi!</b>\n\n"
            "👤 Xodim: <b>{name}</b>\n"
            "🔧 Lavozimi: {position}\n"
            "📱 Telefon: {phone}\n\n"
            "Endi siz yangi buyurtmalar haqida "
            "bildirishnomalar olasiz."
        ),
        "employee_group": (
            "🚰 <b>Santexniklar ishchi guruhi</b>\n\n"
            "Ishchi guruhga o‘tish uchun quyidagi "
            "tugmani bosing."
        ),
        "phone_confirmed": ("✅ <b>Telefon raqami tasdiqlandi!</b>"),
        "phone_already_other_telegram": (
            "⚠️ Ushbu telefon raqami allaqachon "
            "boshqa Telegram akkauntiga ulangan.\n\n"
            "Agar bu sizning raqamingiz bo‘lsa — "
            "administratorga murojaat qiling."
        ),
    },
    "en": {
        "own_contact": (
            "⚠️ You need to send your own phone number.\n\n"
            "Press the "
            "«📱 Send my phone number» "
            "button and select your own contact."
        ),
        "phone_error": (
            "❌ We couldn't get your phone number.\n\n" "Please try sending it again."
        ),
        "employee_already_active": (
            "👋 This Telegram account is already linked " "to employee <b>{name}</b>."
        ),
        "employee_already_inactive": (
            "⚠️ This Telegram account is linked "
            "to an inactive employee profile.\n\n"
            "Please contact the administrator."
        ),
        "employee_other_telegram": (
            "⚠️ This employee is already linked "
            "to another Telegram account.\n\n"
            "Please contact the administrator."
        ),
        "employee_linked": (
            "✅ <b>Telegram successfully linked!</b>\n\n"
            "👤 Employee: <b>{name}</b>\n"
            "🔧 Position: {position}\n"
            "📱 Phone: {phone}\n\n"
            "You will now receive notifications "
            "about new requests."
        ),
        "employee_group": (
            "🚰 <b>Plumbers' work group</b>\n\n"
            "Press the button below to open "
            "the work group."
        ),
        "phone_confirmed": ("✅ <b>Phone number confirmed!</b>"),
        "phone_already_other_telegram": (
            "⚠️ This phone number is already linked "
            "to another Telegram account.\n\n"
            "If this is your number, please contact "
            "the administrator."
        ),
    },
    "zh": {
        "own_contact": (
            "⚠️ 您必须发送您自己的电话号码。\n\n"
            "请点击"
            "「📱 发送我的电话号码」"
            "按钮并选择您自己的联系人。"
        ),
        "phone_error": ("❌ 无法获取您的电话号码。\n\n" "请重新发送。"),
        "employee_already_active": (
            "👋 此 Telegram 账号已经绑定到员工 " "<b>{name}</b>。"
        ),
        "employee_already_inactive": (
            "⚠️ 此 Telegram 账号已绑定到 " "未启用的员工账户。\n\n" "请联系管理员。"
        ),
        "employee_other_telegram": (
            "⚠️ 此员工已经绑定到其他 Telegram 账号。\n\n" "请联系管理员。"
        ),
        "employee_linked": (
            "✅ <b>Telegram 绑定成功！</b>\n\n"
            "👤 员工：<b>{name}</b>\n"
            "🔧 职位：{position}\n"
            "📱 电话：{phone}\n\n"
            "现在您将收到新的服务请求通知。"
        ),
        "employee_group": (
            "🚰 <b>水管工工作群组</b>\n\n" "点击下面的按钮进入工作群组。"
        ),
        "phone_confirmed": ("✅ <b>电话号码已确认！</b>"),
        "phone_already_other_telegram": (
            "⚠️ 此电话号码已经绑定到其他 Telegram 账号。\n\n"
            "如果这是您的号码，请联系管理员。"
        ),
    },
}


# ==========================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==========================================================


def get_language(language):
    """
    Возвращает поддерживаемый язык.
    """

    language = (language or "").lower()

    if language in {
        "ru",
        "uz",
        "en",
        "zh",
    }:
        return language

    return "ru"


def get_text(language, key, **kwargs):
    """
    Получает локализованный текст.
    """

    language = get_language(language)

    text = TEXTS.get(
        language,
        TEXTS["ru"],
    ).get(
        key,
        TEXTS["ru"].get(key, ""),
    )

    if kwargs:
        return text.format(**kwargs)

    return text


# ==========================================================
# CONTACT
# ==========================================================


def handle_contact(
    bot,
    message,
):
    """
    Обрабатывает отправку номера телефона.

    Язык клиента сохраняется в TelegramClient.language.

    Если клиент уже существует — используется его текущий язык.

    Если клиент новый — используется язык, выбранный пользователем
    ранее в TelegramUser.language.
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

    contact = message.get(
        "contact",
    )

    if not telegram_id or not contact:
        return

    # ======================================================
    # СОХРАНЯЕМ TELEGRAM USER
    # ======================================================

    sync_telegram_user(
        telegram_user,
    )

    # ======================================================
    # ОПРЕДЕЛЯЕМ ЯЗЫК
    # ======================================================

    client = TelegramClient.objects.filter(
        telegram_id=telegram_id,
    ).first()

    if client:
        # Для уже существующего клиента сохраняем
        # его язык из TelegramClient.
        language = get_language(
            client.language,
        )
    else:
        # Для нового клиента берем язык, который
        # пользователь выбрал на этапе /start.
        language = get_language(
            get_telegram_user_language(
                telegram_id,
            ),
        )

    # ======================================================
    # ПРОВЕРЯЕМ СОБСТВЕННЫЙ КОНТАКТ
    # ======================================================

    contact_user_id = contact.get(
        "user_id",
    )

    if contact_user_id is not None and contact_user_id != telegram_id:
        bot.send_message(
            telegram_id,
            get_text(
                language,
                "own_contact",
            ),
        )

        return

    phone = contact.get(
        "phone_number",
        "",
    )

    if not phone:
        bot.send_message(
            telegram_id,
            get_text(
                language,
                "phone_error",
            ),
        )

        return

    # ======================================================
    # TELEGRAM УЖЕ ПРИВЯЗАН К СОТРУДНИКУ
    # ======================================================

    existing_employee = Employee.objects.filter(
        telegram_id=telegram_id,
    ).first()

    if existing_employee:

        employee_language = get_language(
            existing_employee.language,
        )

        if existing_employee.is_active:
            bot.send_message(
                telegram_id,
                get_text(
                    employee_language,
                    "employee_already_active",
                    name=existing_employee.name,
                ),
            )
        else:
            bot.send_message(
                telegram_id,
                get_text(
                    employee_language,
                    "employee_already_inactive",
                ),
            )

        return

    # ======================================================
    # ИЩЕМ СОТРУДНИКА
    # ======================================================

    employee = find_employee_by_phone(
        phone,
    )

    if employee is not None:

        if employee.telegram_id is not None and employee.telegram_id != telegram_id:
            employee_language = get_language(
                employee.language,
            )

            bot.send_message(
                telegram_id,
                get_text(
                    employee_language,
                    "employee_other_telegram",
                ),
            )

            return

        employee.telegram_id = telegram_id
        employee.telegram_username = username or ""

        employee.save(
            update_fields=[
                "telegram_id",
                "telegram_username",
                "updated_at",
            ],
        )

        employee_language = get_language(
            employee.language,
        )

        remove_keyboard = {
            "remove_keyboard": True,
        }

        bot.send_message(
            telegram_id,
            get_text(
                employee_language,
                "employee_linked",
                name=employee.name,
                position=employee.position,
                phone=employee.phone,
            ),
            reply_markup=remove_keyboard,
        )

        group_keyboard = get_employee_group_keyboard()

        if group_keyboard:
            bot.send_message(
                telegram_id,
                get_text(
                    employee_language,
                    "employee_group",
                ),
                reply_markup=group_keyboard,
            )

        return

    # ======================================================
    # КЛИЕНТ
    # ======================================================

    display_name = get_telegram_display_name(
        telegram_user,
    )

    if not display_name:
        display_name = "Клиент"

    client = TelegramClient.objects.filter(
        telegram_id=telegram_id,
    ).first()

    # ======================================================
    # КЛИЕНТ УЖЕ СУЩЕСТВУЕТ ПО TELEGRAM ID
    # ======================================================

    if client:

        # Сохраняем язык, который уже записан у клиента.
        language = get_language(
            client.language,
        )

        update_fields = []

        if client.phone != phone:
            client.phone = phone

            update_fields.append(
                "phone",
            )

        if client.telegram_username != (username or ""):
            client.telegram_username = username or ""

            update_fields.append(
                "telegram_username",
            )

        if display_name and client.name != display_name:
            client.name = display_name

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

    else:

        # ==================================================
        # ИЩЕМ КЛИЕНТА ПО НОМЕРУ ТЕЛЕФОНА
        # ==================================================

        client = find_client_by_phone(
            phone,
        )

        if client:

            if client.telegram_id is not None and client.telegram_id != telegram_id:
                client_language = get_language(
                    client.language,
                )

                bot.send_message(
                    telegram_id,
                    get_text(
                        client_language,
                        "phone_already_other_telegram",
                    ),
                )

                return

            client.telegram_id = telegram_id
            client.telegram_username = username or ""

            if display_name:
                client.name = display_name

            client.save(
                update_fields=[
                    "telegram_id",
                    "telegram_username",
                    "name",
                    "updated_at",
                ],
            )

            # Если клиент уже существовал в базе,
            # сохраняем его существующий язык.
            language = get_language(
                client.language,
            )

        else:

            # ==================================================
            # СОЗДАЕМ НОВОГО КЛИЕНТА
            # ==================================================

            # ВАЖНО:
            # здесь НЕ ставим language="ru".
            #
            # Используем язык, который пользователь
            # выбрал на предыдущем шаге.
            language = get_language(
                get_telegram_user_language(
                    telegram_id,
                ),
            )

            client = TelegramClient.objects.create(
                telegram_id=telegram_id,
                telegram_username=username or "",
                name=display_name,
                phone=phone,
                language=language,
            )

    # ======================================================
    # УБИРАЕМ REPLY KEYBOARD
    # ======================================================

    remove_keyboard = {
        "remove_keyboard": True,
    }

    bot.send_message(
        telegram_id,
        get_text(
            language,
            "phone_confirmed",
        ),
        reply_markup=remove_keyboard,
    )

    # ======================================================
    # INLINE MENU
    # ======================================================

    print("📋 После контакта вызываю " "send_client_ui_menu()...")

    send_client_ui_menu(
        bot,
        telegram_id,
        client,
    )
