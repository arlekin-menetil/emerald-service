from django.conf import settings

# ==========================================================
# EMPLOYEE GROUP
# ==========================================================


def get_employee_group_keyboard():
    """
    Возвращает кнопку перехода сотрудника
    в рабочую Telegram-группу.
    """

    group_url = getattr(
        settings,
        "TELEGRAM_GROUP_URL",
        "",
    )

    if not group_url:
        return None

    return {
        "inline_keyboard": [
            [
                {
                    "text": "🔗 Открыть рабочую группу",
                    "url": group_url,
                },
            ],
        ],
    }


def send_employee_menu(
    bot,
    telegram_id,
    employee,
):
    """
    Показывает сотруднику сообщение после привязки.
    """

    group_keyboard = get_employee_group_keyboard()

    bot.send_message(
        telegram_id,
        "✅ <b>Telegram успешно привязан!</b>\n\n"
        f"👤 Сотрудник: <b>{employee.name}</b>\n"
        f"🔧 Должность: {employee.position}\n"
        f"📱 Телефон: {employee.phone}\n\n"
        "Теперь вы будете получать уведомления "
        "о новых заявках.",
        reply_markup=group_keyboard,
    )
