import logging

from telegram_bot.client.translations_online import translate_online

logger = logging.getLogger(__name__)


TARGET_LANGUAGES = {
    "uz": "name_uz",
    "en": "name_en",
    "zh": "name_zh",
}


def translate_employee_name(name: str) -> dict:
    """
    Переводит имя сотрудника с русского на поддерживаемые языки.

    Возвращает словарь:
        {
            "name_uz": "...",
            "name_en": "...",
            "name_zh": "...",
        }

    Если перевод невозможен, translate_online()
    возвращает исходный текст.
    """

    name = str(name or "").strip()

    if not name:
        return {
            field: ""
            for field in TARGET_LANGUAGES.values()
        }

    result = {}

    for language, field_name in TARGET_LANGUAGES.items():
        try:
            result[field_name] = translate_online(
                name,
                target_language=language,
                source_language="ru",
            )
        except Exception:
            logger.exception(
                "Не удалось перевести имя сотрудника: %r -> %s",
                name,
                language,
            )
            result[field_name] = name

    return result


WEBSITE_NAME_TARGET_LANGUAGES = {
    "uz": "website_name_uz",
    "en": "website_name_en",
    "zh": "website_name_zh",
}


def translate_employee_website_name(website_name: str) -> dict:
    """
    Переводит отображаемое имя сотрудника для сайта.
    """
    website_name = str(website_name or "").strip()

    if not website_name:
        return {
            field: ""
            for field in WEBSITE_NAME_TARGET_LANGUAGES.values()
        }

    result = {}

    for language, field_name in WEBSITE_NAME_TARGET_LANGUAGES.items():
        try:
            result[field_name] = translate_online(
                website_name,
                target_language=language,
                source_language="ru",
            )
        except Exception:
            logger.exception(
                "Не удалось перевести website_name сотрудника: %r -> %s",
                website_name,
                language,
            )
            result[field_name] = website_name

    return result
