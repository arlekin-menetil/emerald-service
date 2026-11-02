import time

import requests

from django.conf import settings


class TelegramBotError(Exception):
    """Ошибка взаимодействия с Telegram Bot API."""


class TelegramBot:
    BASE_URL = "https://api.telegram.org/bot{token}"

    # ==========================================================
    # TIMEOUTS
    # ==========================================================

    # Обычные запросы Telegram.
    DEFAULT_CONNECT_TIMEOUT = 5
    DEFAULT_READ_TIMEOUT = 10

    # Long polling getUpdates.
    GET_UPDATES_CONNECT_TIMEOUT = 5
    GET_UPDATES_READ_TIMEOUT_EXTRA = 5

    # ==========================================================
    # RETRIES
    # ==========================================================

    # Для обычных запросов допускаем максимум 2 повтора.
    MAX_RETRIES = 2

    # Небольшая пауза между повторными попытками.
    RETRY_DELAY = 0.5

    # Long polling retry/backoff при временных сетевых ошибках.
    GET_UPDATES_MAX_RETRIES = 4
    GET_UPDATES_RETRY_DELAYS = (1, 2, 4, 8)

    # ==========================================================
    # INIT
    # ==========================================================

    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN

        if not self.token:
            raise TelegramBotError("TELEGRAM_BOT_TOKEN не настроен.")

        self.base_url = self.BASE_URL.format(token=self.token)

        # Session позволяет переиспользовать
        # HTTP-соединения с Telegram.
        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": ("EmeraldServiceTelegramBot/1.0"),
                "Accept": "application/json",
            }
        )

    # ==========================================================
    # INTERNAL REQUEST
    # ==========================================================

    def _request(
        self,
        method,
        data=None,
        timeout=None,
        retries=None,
    ):
        """
        Универсальный запрос к Telegram Bot API.

        timeout:
            - одно число;
            - или tuple(connect_timeout, read_timeout).

        retries:
            количество повторных попыток
            при временных сетевых ошибках.
        """

        url = f"{self.base_url}/{method}"

        if timeout is None:
            timeout = (
                self.DEFAULT_CONNECT_TIMEOUT,
                self.DEFAULT_READ_TIMEOUT,
            )

        if retries is None:
            retries = self.MAX_RETRIES

        last_exception = None

        for attempt in range(retries + 1):

            started_at = time.perf_counter()

            try:
                response = self.session.post(
                    url,
                    json=data or {},
                    timeout=timeout,
                )

                elapsed = time.perf_counter() - started_at

                # --------------------------------------------------
                # JSON
                # --------------------------------------------------

                try:
                    result = response.json()

                except ValueError as exc:
                    print(
                        f"❌ Telegram API: {method} | "
                        f"Некорректный JSON | "
                        f"{elapsed:.3f}s"
                    )

                    raise TelegramBotError(
                        "Telegram вернул некорректный JSON."
                    ) from exc

                # --------------------------------------------------
                # PERFORMANCE DIAGNOSTIC
                # --------------------------------------------------

                if method != "getUpdates" or not response.ok:
                    print(
                        f"📡 Telegram API: "
                        f"{method} | "
                        f"{elapsed:.3f}s | "
                        f"HTTP {response.status_code}"
                    )

                # --------------------------------------------------
                # TELEGRAM API ERROR
                # --------------------------------------------------

                if not response.ok or not result.get("ok"):

                    description = result.get(
                        "description",
                        "Неизвестная ошибка Telegram.",
                    )

                    error_code = result.get("error_code")

                    if error_code:
                        raise TelegramBotError(
                            f"Telegram API error "
                            f"{error_code}: {description}"
                        )

                    raise TelegramBotError(
                        f"Telegram API error: {description}"
                    )

                return result

            # ======================================================
            # READ TIMEOUT
            # ======================================================

            except requests.exceptions.ReadTimeout as exc:

                elapsed = time.perf_counter() - started_at
                last_exception = exc

                print(
                    f"⏱️ Telegram ReadTimeout: "
                    f"{method} | "
                    f"{elapsed:.3f}s"
                )

                # Для getUpdates timeout — нормальная
                # ситуация long polling.
                if method == "getUpdates":
                    raise TelegramBotError(
                        "Telegram не вернул getUpdates "
                        "за отведённое время."
                    ) from exc

                if attempt < retries:
                    time.sleep(self.RETRY_DELAY)
                    continue

                raise TelegramBotError(
                    "Таймаут ожидания ответа Telegram: "
                    f"{exc}"
                ) from exc

            # ======================================================
            # CONNECT TIMEOUT
            # ======================================================

            except requests.exceptions.ConnectTimeout as exc:

                elapsed = time.perf_counter() - started_at
                last_exception = exc

                print(
                    f"⏱️ Telegram ConnectTimeout: "
                    f"{method} | "
                    f"{elapsed:.3f}s"
                )

                if attempt < retries:
                    time.sleep(self.RETRY_DELAY)
                    continue

                raise TelegramBotError(
                    "Таймаут подключения к Telegram: "
                    f"{exc}"
                ) from exc

            # ======================================================
            # CONNECTION ERROR
            # ======================================================

            except requests.exceptions.ConnectionError as exc:

                elapsed = time.perf_counter() - started_at
                last_exception = exc

                print(
                    f"❌ Telegram ConnectionError: "
                    f"{method} | "
                    f"{elapsed:.3f}s"
                )

                if attempt < retries:
                    time.sleep(self.RETRY_DELAY)
                    continue

                raise TelegramBotError(
                    "Ошибка соединения с Telegram: "
                    f"{exc}"
                ) from exc

            # ======================================================
            # OTHER REQUEST ERROR
            # ======================================================

            except requests.exceptions.RequestException as exc:

                elapsed = time.perf_counter() - started_at
                last_exception = exc

                print(
                    f"❌ Telegram RequestException: "
                    f"{method} | "
                    f"{elapsed:.3f}s"
                )

                if attempt < retries:
                    time.sleep(self.RETRY_DELAY)
                    continue

                raise TelegramBotError(
                    "Ошибка HTTP-запроса к Telegram: "
                    f"{exc}"
                ) from exc

        raise TelegramBotError(
            "Не удалось выполнить запрос Telegram: "
            f"{last_exception}"
        )

    # ==========================================================
    # GET UPDATES
    # ==========================================================

    def get_updates(
        self,
        offset=None,
        timeout=30,
    ):
        """
        Получает новые Telegram updates.

        timeout — время long polling.

        HTTP read timeout должен быть немного
        больше Telegram timeout.

        Обычный ReadTimeout для getUpdates — нормальное
        завершение long polling без новых updates.

        Временные ошибки соединения/DNS переживаются
        с backoff и повторными попытками.
        """

        data = {
            "timeout": timeout,
            "allowed_updates": [
                "message",
                "callback_query",
            ],
        }

        if offset is not None:
            data["offset"] = offset

        read_timeout = timeout + self.GET_UPDATES_READ_TIMEOUT_EXTRA
        last_exception = None

        for attempt in range(self.GET_UPDATES_MAX_RETRIES + 1):
            try:
                return self._request(
                    "getUpdates",
                    data=data,
                    timeout=(
                        self.GET_UPDATES_CONNECT_TIMEOUT,
                        read_timeout,
                    ),
                    retries=0,
                )

            except TelegramBotError as exc:
                last_exception = exc

                # Нормальный конец long polling:
                # новых updates за timeout нет.
                if "не вернул getUpdates" in str(exc):
                    return {
                        "ok": True,
                        "result": [],
                    }

                # После последней попытки передаём ошибку
                # внешнему polling-циклу.
                if attempt >= self.GET_UPDATES_MAX_RETRIES:
                    raise

                delay = self.GET_UPDATES_RETRY_DELAYS[
                    min(
                        attempt,
                        len(self.GET_UPDATES_RETRY_DELAYS) - 1,
                    )
                ]

                print(
                    f"⚠️ Временная ошибка Telegram getUpdates: {exc}"
                )

                print(
                    f"⏳ Повтор getUpdates через {delay} сек..."
                )

                time.sleep(delay)

        raise TelegramBotError(
            "Не удалось получить Telegram updates: "
            f"{last_exception}"
        )

    # ==========================================================
    # SEND MESSAGE
    # ==========================================================

    def send_message(
        self,
        chat_id,
        text,
        parse_mode="HTML",
        reply_markup=None,
    ):
        """
        Отправляет сообщение пользователю или группе.
        """

        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
        }

        if reply_markup is not None:
            data["reply_markup"] = reply_markup

        return self._request(
            "sendMessage",
            data=data,
            timeout=(
                self.DEFAULT_CONNECT_TIMEOUT,
                self.DEFAULT_READ_TIMEOUT,
            ),
        )

    # ==========================================================
    # DELETE MESSAGE
    # ==========================================================

    def delete_message(
        self,
        chat_id,
        message_id,
    ):
        """Удаляет сообщение из чата."""

        data = {
            "chat_id": chat_id,
            "message_id": message_id,
        }

        return self._request(
            "deleteMessage",
            data=data,
            timeout=(
                self.DEFAULT_CONNECT_TIMEOUT,
                self.DEFAULT_READ_TIMEOUT,
            ),
        )

    # ==========================================================
    # SEND MESSAGE TO GROUP
    # ==========================================================

    def send_to_group(
        self,
        text,
        parse_mode="HTML",
        reply_markup=None,
    ):
        """
        Отправляет сообщение в рабочую Telegram-группу.
        """

        chat_id = settings.TELEGRAM_CHAT_ID

        if not chat_id:
            raise TelegramBotError("TELEGRAM_CHAT_ID не настроен.")

        return self.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
        )

    # ==========================================================
    # CALLBACK QUERY
    # ==========================================================

    def answer_callback_query(
        self,
        callback_query_id,
        text=None,
        show_alert=False,
    ):
        """
        Подтверждает нажатие inline-кнопки Telegram.
        """

        data = {
            "callback_query_id": callback_query_id,
            "show_alert": show_alert,
        }

        if text:
            data["text"] = text

        return self._request(
            "answerCallbackQuery",
            data=data,
            timeout=(
                self.DEFAULT_CONNECT_TIMEOUT,
                self.DEFAULT_READ_TIMEOUT,
            ),
        )

    # ==========================================================
    # EDIT MESSAGE
    # ==========================================================

    def edit_message_text(
        self,
        chat_id,
        message_id,
        text,
        parse_mode="HTML",
        reply_markup=None,
    ):
        """
        Изменяет текст уже отправленного сообщения
        вместе с inline-клавиатурой.
        """

        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": parse_mode,
        }

        if reply_markup is not None:
            data["reply_markup"] = reply_markup

        return self._request(
            "editMessageText",
            data=data,
            timeout=(
                self.DEFAULT_CONNECT_TIMEOUT,
                self.DEFAULT_READ_TIMEOUT,
            ),
        )