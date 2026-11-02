from calendar import monthrange
from datetime import date

from django.utils import timezone

from .translations import get_month_name, get_weekday_name, t


def get_calendar_month_name(client, month):
    return get_month_name(client, month)


def get_calendar_weekday_headers(client):
    return [[
        {
            "text": get_weekday_name(client, weekday),
            "callback_data": "client:calendar_noop",
        }
        for weekday in range(7)
    ]]


def get_calendar_keyboard(client):
    today = timezone.localdate()
    year, month = today.year, today.month
    days_in_month = monthrange(year, month)[1]
    first_weekday = date(year, month, 1).weekday()

    keyboard = [[{
        "text": f"📅 {get_calendar_month_name(client, month)} {year}",
        "callback_data": "client:calendar_noop",
    }]]

    keyboard.extend(get_calendar_weekday_headers(client))

    week = [
        {
            "text": " ",
            "callback_data": "client:calendar_noop",
        }
        for _ in range(first_weekday)
    ]

    for day_number in range(1, days_in_month + 1):
        current_date = date(year, month, day_number)

        if current_date < today:
            button = {
                "text": f"▫️ {day_number}",
                "callback_data": "client:calendar_noop",
            }
        elif current_date == today:
            button = {
                "text": f"🟢 {day_number}",
                "callback_data": f"client:date:{current_date.isoformat()}",
            }
        else:
            button = {
                "text": str(day_number),
                "callback_data": f"client:date:{current_date.isoformat()}",
            }

        week.append(button)

        if len(week) == 7:
            keyboard.append(week)
            week = []

    if week:
        week.extend(
            {
                "text": " ",
                "callback_data": "client:calendar_noop",
            }
            for _ in range(7 - len(week))
        )
        keyboard.append(week)

    keyboard.append([{
        "text": t(client, "cancel"),
        "callback_data": "client:cancel",
    }])

    return {"inline_keyboard": keyboard}


def build_client_calendar_text(client):
    today = timezone.localdate()

    return (
        t(client, "calendar_choose_date")
        + t(
            client,
            "calendar_today",
            date=today.strftime("%d.%m.%Y"),
        )
        + t(client, "calendar_past_day")
        + t(client, "calendar_today_legend")
        + t(client, "calendar_choose_convenient_date")
    )