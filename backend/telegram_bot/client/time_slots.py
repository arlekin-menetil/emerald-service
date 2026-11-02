from datetime import date, datetime, time, timedelta

from django.utils import timezone

from .translations import t


CLIENT_WORK_START_HOUR = 9
CLIENT_WORK_START_MINUTE = 0

CLIENT_WORK_END_HOUR = 18
CLIENT_WORK_END_MINUTE = 0

CLIENT_TIME_SLOT_MINUTES = 30


def get_time_slots_for_date(selected_date):
    """Возвращает доступные интервалы времени для выбранной даты."""
    if not isinstance(selected_date, date):
        return []

    today = timezone.localdate()
    now = timezone.localtime()

    start = time(
        CLIENT_WORK_START_HOUR,
        CLIENT_WORK_START_MINUTE,
    )
    end = time(
        CLIENT_WORK_END_HOUR,
        CLIENT_WORK_END_MINUTE,
    )

    current_datetime = datetime.combine(
        selected_date,
        start,
    )
    end_datetime = datetime.combine(
        selected_date,
        end,
    )

    slots = []

    while current_datetime <= end_datetime:
        slot_time = current_datetime.time()

        if selected_date == today:
            current_slot_time = time(
                now.hour,
                now.minute,
            )

            if slot_time <= current_slot_time:
                current_datetime += timedelta(
                    minutes=CLIENT_TIME_SLOT_MINUTES,
                )
                continue

        slots.append(slot_time)

        current_datetime += timedelta(
            minutes=CLIENT_TIME_SLOT_MINUTES,
        )

    return slots


def get_time_keyboard(client, selected_date):
    """Формирует inline-клавиатуру выбора времени."""
    slots = get_time_slots_for_date(selected_date)

    keyboard = []
    row = []

    for slot in slots:
        time_text = slot.strftime("%H:%M")
        callback_time = slot.strftime("%H-%M")
        date_value = selected_date.isoformat()

        row.append({
            "text": time_text,
            "callback_data": (
                f"client:time:{date_value}:{callback_time}"
            ),
        })

        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    if not slots:
        keyboard.append([
            {
                "text": t(client, "time_unavailable"),
                "callback_data": "client:calendar_noop",
            }
        ])

    keyboard.append([
        {
            "text": t(client, "choose_another_date"),
            "callback_data": "client:choose_date",
        }
    ])

    keyboard.append([
        {
            "text": t(client, "cancel"),
            "callback_data": "client:cancel",
        }
    ])

    return {
        "inline_keyboard": keyboard,
    }


def build_client_time_text(client, selected_date):
    """Формирует текст перед выбором времени."""
    return t(
        client,
        "time_choose",
        date=selected_date.strftime("%d.%m.%Y"),
    )