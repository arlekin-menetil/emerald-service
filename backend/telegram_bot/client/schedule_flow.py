from datetime import date, datetime

from django.utils import timezone
from telegram_clients.models import TelegramClient

from .calendar import build_client_calendar_text, get_calendar_keyboard
from .common import (
    CLIENT_SELECTED_DATE_KEY,
    CLIENT_SELECTED_TIME_KEY,
    CLIENT_TIME_STORAGE_FORMAT,
    edit_client_screen,
    get_client_by_telegram_id,
)
from .keyboards import get_client_inline_menu_keyboard, get_skip_inline_keyboard
from .time_slots import build_client_time_text, get_time_keyboard, get_time_slots_for_date
from .translations import t


def parse_client_date(value):
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return None

def handle_client_date_selected(bot, telegram_id, date_value, client=None, message_id=None):
    if client is None:
        client = get_client_by_telegram_id(telegram_id)
    if client is None:
        return
    if client.flow_state != TelegramClient.FLOW_CHOOSING_DATE:
        return edit_client_screen(bot, telegram_id, t(client, 'date_selection_unavailable'), reply_markup=get_client_inline_menu_keyboard(client), client=client, message_id=message_id)
    selected_date = parse_client_date(date_value)
    if selected_date is None:
        return edit_client_screen(bot, telegram_id, t(client, 'invalid_date'), reply_markup=get_calendar_keyboard(client), client=client, message_id=message_id)
    today = timezone.localdate()
    if selected_date < today:
        return edit_client_screen(bot, telegram_id, t(client, 'date_already_passed'), reply_markup=get_calendar_keyboard(client), client=client, message_id=message_id)
    slots = get_time_slots_for_date(selected_date)
    if not slots:
        if selected_date == today:
            text = t(client, 'no_time_slots_today')
        else:
            text = t(client, 'no_time_slots_date')
        return edit_client_screen(bot, telegram_id, text, reply_markup=get_calendar_keyboard(client), client=client, message_id=message_id)
    client.set_draft_value(CLIENT_SELECTED_DATE_KEY, selected_date.isoformat())
    draft = dict(client.draft_data or {})
    draft.pop(CLIENT_SELECTED_TIME_KEY, None)
    draft.pop('scheduled_at', None)
    client.draft_data = draft
    client.save(update_fields=['draft_data', 'updated_at'])
    client.set_flow_state(TelegramClient.FLOW_CHOOSING_TIME)
    return edit_client_screen(bot, telegram_id, build_client_time_text(client, selected_date), reply_markup=get_time_keyboard(client, selected_date), client=client, message_id=message_id)

def parse_client_time(value):
    if not value:
        return None
    normalized_value = str(value).strip()
    if '-' in normalized_value:
        normalized_value = normalized_value.replace('-', ':', 1)
    try:
        return datetime.strptime(normalized_value, '%H:%M').time()
    except (TypeError, ValueError):
        return None

def combine_client_date_time(selected_date, selected_time):
    naive_datetime = datetime.combine(selected_date, selected_time)
    return timezone.make_aware(naive_datetime, timezone=timezone.get_current_timezone())

def handle_client_time_selected(bot, telegram_id, date_value, time_value, client=None, message_id=None):
    if client is None:
        client = get_client_by_telegram_id(telegram_id)
    if client is None:
        return
    if client.flow_state != TelegramClient.FLOW_CHOOSING_TIME:
        return edit_client_screen(bot, telegram_id, t(client, 'time_selection_unavailable'), reply_markup=get_client_inline_menu_keyboard(client), client=client, message_id=message_id)
    selected_date = parse_client_date(date_value)
    selected_time = parse_client_time(time_value)
    if selected_date is None or selected_time is None:
        return edit_client_screen(bot, telegram_id, t(client, 'invalid_date_or_time'), reply_markup=get_calendar_keyboard(client), client=client, message_id=message_id)
    today = timezone.localdate()
    if selected_date < today:
        client.set_flow_state(TelegramClient.FLOW_CHOOSING_DATE)
        return edit_client_screen(bot, telegram_id, t(client, 'date_already_passed'), reply_markup=get_calendar_keyboard(client), client=client, message_id=message_id)
    available_slots = get_time_slots_for_date(selected_date)
    if selected_time not in available_slots:
        return edit_client_screen(bot, telegram_id, t(client, 'time_unavailable'), reply_markup=get_time_keyboard(client, selected_date), client=client, message_id=message_id)
    scheduled_at = combine_client_date_time(selected_date, selected_time)
    if scheduled_at <= timezone.now():
        return edit_client_screen(bot, telegram_id, t(client, 'time_already_passed'), reply_markup=get_time_keyboard(client, selected_date), client=client, message_id=message_id)
    client.set_draft_value(CLIENT_SELECTED_DATE_KEY, selected_date.isoformat())
    client.set_draft_value(CLIENT_SELECTED_TIME_KEY, selected_time.strftime(CLIENT_TIME_STORAGE_FORMAT))
    client.set_draft_value('scheduled_at', scheduled_at.isoformat())
    client.set_flow_state(TelegramClient.FLOW_WAITING_COMMENT)
    return edit_client_screen(bot, telegram_id, t(client, 'comment_prompt'), reply_markup=get_skip_inline_keyboard(client), client=client, message_id=message_id)
