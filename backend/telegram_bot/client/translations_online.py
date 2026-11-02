import logging

import requests
from django.conf import settings


logger = logging.getLogger(__name__)

YANDEX_TRANSLATE_URL = (
    "https://translate.api.cloud.yandex.net/translate/v2/translate"
)


def translate_online(
    text: str,
    target_language: str,
    source_language: str = "ru",
) -> str:
    """
    Перевод текста через Yandex Cloud Translate.

    Если перевод невозможен по какой-либо причине,
    возвращает исходный текст, чтобы бот продолжал работать.
    """

    text = str(text or "").strip()

    if not text:
        return text

    target_language = str(target_language or "").strip().lower()
    source_language = str(source_language or "").strip().lower()

    # Переводить русский -> русский нет смысла.
    if not target_language or target_language == source_language:
        return text

    api_key = getattr(settings, "YANDEX_TRANSLATE_API_KEY", "")
    folder_id = getattr(settings, "YANDEX_CLOUD_FOLDER_ID", "")

    if not api_key:
        logger.warning("YANDEX_TRANSLATE_API_KEY не задан.")
        return text

    if not folder_id:
        logger.warning("YANDEX_CLOUD_FOLDER_ID не задан.")
        return text

    payload = {
        "folderId": folder_id,
        "texts": [text],
        "targetLanguageCode": target_language,
        "sourceLanguageCode": source_language,
    }

    headers = {
        "Authorization": f"Api-Key {api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            YANDEX_TRANSLATE_URL,
            headers=headers,
            json=payload,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        translations = data.get("translations") or []

        if not translations:
            logger.warning(
                "Yandex Translate вернул ответ без translations: %s",
                data,
            )
            return text

        translated_text = translations[0].get("text")

        if not translated_text:
            logger.warning(
                "Yandex Translate вернул пустой перевод: %s",
                data,
            )
            return text

        return translated_text.strip()

    except requests.RequestException as exc:
        logger.exception(
            "Ошибка запроса к Yandex Translate: %s",
            exc,
        )
        return text

    except (ValueError, KeyError, TypeError) as exc:
        logger.exception(
            "Ошибка обработки ответа Yandex Translate: %s",
            exc,
        )
        return text