from services.models import Service

from .translations import get_language, t


def get_client_inline_menu_keyboard(client):
    return {
        "inline_keyboard": [
            [{"text": t(client, "menu_create"), "callback_data": "client:create"}],
            [{"text": t(client, "menu_requests"), "callback_data": "client:requests"}],
            [{"text": t(client, "menu_services"), "callback_data": "client:services"}],
        ],
    }


def get_back_to_client_menu_keyboard(client):
    return {
        "inline_keyboard": [[
            {
                "text": t(client, "back_to_menu"),
                "callback_data": "client:menu",
            }
        ]],
    }


def get_cancel_inline_keyboard(client):
    return {
        "inline_keyboard": [[
            {
                "text": t(client, "cancel"),
                "callback_data": "client:cancel",
            }
        ]],
    }


def get_location_keyboard(client):
    return {
        "keyboard": [
            [
                {
                    "text": t(client, "share_location"),
                    "request_location": True,
                }
            ],
            [{"text": t(client, "cancel")}],
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True,
        "is_persistent": False,
        "selective": False,
    }


def get_remove_location_keyboard():
    return {"remove_keyboard": True}


def get_skip_inline_keyboard(client):
    return {
        "inline_keyboard": [
            [{
                "text": t(client, "skip"),
                "callback_data": "client:skip_comment",
            }],
            [{
                "text": t(client, "cancel"),
                "callback_data": "client:cancel",
            }],
        ],
    }


def get_localized_service_name(service, client):
    field_name = {
        "ru": "name",
        "uz": "name_uz",
        "en": "name_en",
        "zh": "name_zh",
    }.get(get_language(client), "name")

    return getattr(service, field_name, None) or service.name


def get_service_keyboard(client):
    services = (
        Service.objects
        .filter(is_active=True)
        .select_related("category")
        .order_by(
            "category__sort_order",
            "sort_order",
            "name",
        )
    )

    keyboard = [
        [{
            "text": get_localized_service_name(service, client),
            "callback_data": f"client:service:{service.id}",
        }]
        for service in services
    ]

    keyboard.append([{
        "text": t(client, "back_to_menu"),
        "callback_data": "client:menu",
    }])

    return {"inline_keyboard": keyboard}


def get_service_continue_keyboard(client, service_id):
    return {
        "inline_keyboard": [
            [{
                "text": t(client, "continue"),
                "callback_data": f"client:address:{service_id}",
            }],
            [{
                "text": t(client, "choose_another"),
                "callback_data": "client:create",
            }],
            [{
                "text": t(client, "cancel"),
                "callback_data": "client:cancel",
            }],
        ],
    }


def get_request_confirm_keyboard(client):
    return {
        "inline_keyboard": [
            [{
                "text": t(client, "confirm_request"),
                "callback_data": "client:confirm",
            }],
            [
                {
                    "text": t(client, "edit_request"),
                    "callback_data": "client:edit",
                },
                {
                    "text": t(client, "cancel"),
                    "callback_data": "client:cancel",
                },
            ],
        ],
    }
