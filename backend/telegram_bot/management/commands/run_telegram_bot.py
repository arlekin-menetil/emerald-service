import html
import time

from django.core.management.base import BaseCommand
from django.db import transaction

from employees.models import Employee

from telegram_bot.client_handlers import (
    handle_client_location_message,
    handle_client_text,
)

from telegram_bot.handlers import (
    handle_callback_query,
    handle_contact,
    handle_start,
)

from telegram_bot.services import (
    TelegramBot,
    TelegramBotError,
)

from telegram_bot.handlers.common import (
    find_employee_by_phone,
    normalize_phone,
    sync_telegram_user,
)

from telegram_structure.services import (
    get_saved_group_members,
    sync_telegram_chat_member,
)


class Command(BaseCommand):
    help = "Запускает Telegram-бота для работы с заявками."

    # ==========================================================
    # SETTINGS
    # ==========================================================

    POLLING_TIMEOUT = 30

    ERROR_RETRY_DELAY = 2

    # Временные сессии регистрации сотрудников в рабочей группе.
    # После перезапуска бота пользователь может снова выбрать язык.
    employee_registration_sessions = {}

    # Защита от двойного приглашения при одновременном приходе
    # chat_member и message.new_chat_members.
    employee_registration_invites = set()

    # Защита от повторной обработки одного и того же Telegram-сообщения.
    employee_registration_processed_messages = set()

    # ==========================================================
    # HANDLE
    # ==========================================================

    def handle(self, *args, **options):

        self.stdout.write(self.style.SUCCESS("🤖 Telegram-бот запущен."))

        # ======================================================
        # INITIALIZE BOT
        # ======================================================

        try:

            bot = TelegramBot()

        except TelegramBotError as exc:

            self.stderr.write(
                self.style.ERROR(
                    "❌ Не удалось инициализировать " f"Telegram-бота: {exc}"
                )
            )

            return

        # ======================================================
        # OFFSET
        # ======================================================

        offset = None

        self.stdout.write("📡 Polling запущен. " "Ожидаю сообщения...")

        # ======================================================
        # POLLING LOOP
        # ======================================================

        while True:

            try:

                response = bot.get_updates(
                    offset=offset,
                    timeout=self.POLLING_TIMEOUT,
                )

                updates = response.get(
                    "result",
                    [],
                )

                # --------------------------------------------------
                # PROCESS UPDATES
                # --------------------------------------------------

                for update in updates:

                    update_id = update.get("update_id")

                    if update_id is not None:

                        offset = update_id + 1

                    print("🔥 FULL UPDATE:", update)

                    try:

                        self.handle_update(
                            bot,
                            update,
                        )

                    except TelegramBotError as exc:

                        self.stderr.write(
                            self.style.ERROR(
                                "❌ Ошибка Telegram " "при обработке update: " f"{exc}"
                            )
                        )

                    except Exception as exc:

                        self.stderr.write(
                            self.style.ERROR(
                                "❌ Ошибка при " "обработке update: " f"{exc}"
                            )
                        )

            # ======================================================
            # TELEGRAM ERROR
            # ======================================================

            except TelegramBotError as exc:

                self.stderr.write(self.style.ERROR(f"❌ Ошибка Telegram: {exc}"))

                self.stdout.write(
                    f"⏳ Повтор через " f"{self.ERROR_RETRY_DELAY} сек..."
                )

                time.sleep(self.ERROR_RETRY_DELAY)

            # ======================================================
            # CTRL+C
            # ======================================================

            except KeyboardInterrupt:

                self.stdout.write(self.style.WARNING("\n🤖 Telegram-бот остановлен."))

                break

            # ======================================================
            # UNKNOWN POLLING ERROR
            # ======================================================

            except Exception as exc:

                self.stderr.write(
                    self.style.ERROR("❌ Неожиданная ошибка polling: " f"{exc}")
                )

                self.stdout.write(
                    f"⏳ Повтор через " f"{self.ERROR_RETRY_DELAY} сек..."
                )

                time.sleep(self.ERROR_RETRY_DELAY)

    # ==========================================================
    # HANDLE UPDATE
    # ==========================================================

    def handle_update(
        self,
        bot,
        update,
    ):
        """
        Обрабатывает одно входящее обновление Telegram.

        Приоритет:

        1. chat_member
           └── новый участник рабочей группы

        2. callback_query

        3. message
           ├── новые участники группы
           ├── синхронизация Telegram-группы
           ├── location
           ├── contact
           ├── /start
           ├── /checkgroup
           └── text
        """

        # ======================================================
        # CHAT MEMBER
        # ======================================================

        chat_member_update = update.get("chat_member")

        if chat_member_update is not None:

            self.handle_chat_member_update(
                bot,
                chat_member_update,
            )

            return

        # ======================================================
        # CALLBACK QUERY
        # ======================================================

        callback_query = update.get("callback_query")

        if callback_query is not None:

            callback_data = callback_query.get("data", "") or ""

            if callback_data.startswith("employee_registration:"):
                self.handle_employee_registration_language(
                    bot,
                    callback_query,
                )
                return

            handle_callback_query(
                bot,
                callback_query,
            )

            return

        # ======================================================
        # MESSAGE
        # ======================================================

        message = update.get("message")

        if message is None:
            return

        # ======================================================
        # CHAT
        # ======================================================

        chat = message.get("chat", {})

        if not isinstance(chat, dict):
            return

        chat_type = chat.get("type")

        chat_id = chat.get("id")

        # ======================================================
        # NEW GROUP MEMBERS
        # ======================================================

        new_chat_members = message.get("new_chat_members")

        if chat_type in {
            "group",
            "supergroup",
        } and isinstance(
            new_chat_members,
            list,
        ):

            for new_user in new_chat_members:

                if not isinstance(
                    new_user,
                    dict,
                ):
                    continue

                self.handle_new_group_member(
                    bot,
                    chat,
                    new_user,
                )

        # ======================================================
        # TELEGRAM GROUP MEMBER SYNC
        # ======================================================

        if chat_type in {
            "group",
            "supergroup",
        }:

            try:

                sync_telegram_chat_member(message)

            except Exception as exc:

                self.stderr.write(
                    self.style.ERROR(
                        "⚠️ Не удалось синхронизировать "
                        "участника Telegram-чата: "
                        f"{exc}"
                    )
                )

        print("📨 RAW MESSAGE KEYS:", list(message.keys()))
        print("📨 RAW MESSAGE:", message)

        # ======================================================
        # LOCATION
        # ======================================================

        if "location" in message:

            location = message.get("location")

            if not isinstance(
                location,
                dict,
            ):

                self.stderr.write(
                    self.style.ERROR("❌ message.location " "имеет неожиданный формат.")
                )

                return

            latitude = location.get("latitude")

            longitude = location.get("longitude")

            if latitude is None or longitude is None:

                self.stderr.write(
                    self.style.ERROR(
                        "❌ В location отсутствуют " "latitude или longitude."
                    )
                )

                return

            handle_client_location_message(
                bot,
                message,
            )

            return

        # ======================================================
        # CONTACT
        # ======================================================

        contact = message.get("contact")

        if contact is not None:

            handle_contact(
                bot,
                message,
            )

            return

        # ======================================================
        # TEXT
        # ======================================================

        text = (
            message.get(
                "text",
                "",
            )
            or ""
        ).strip()

        if not text:
            return

        # ======================================================
        # EMPLOYEE REGISTRATION IN GROUP
        # ======================================================

        if chat_type in {"group", "supergroup"}:
            if self.handle_employee_registration_text(
                bot,
                message,
            ):
                return

        # ======================================================
        # START
        # ======================================================


        if text == "/start":
            # /start — явная команда пользователя.
            # Не блокируем её из-за активного flow_state: если пользователь
            # сам отправил /start, он ожидает возврата в главное меню.
            print(
                "🚀 /start получен от пользователя: "
                f"telegram_id={chat_id}. "
                "Запускаю главное меню."
            )

            handle_start(
                bot,
                message,
            )

            return

        # ======================================================
        # CHECK GROUP
        # ======================================================

        if text == "/checkgroup":

            if chat_type not in {
                "group",
                "supergroup",
            }:

                self.stderr.write(
                    self.style.WARNING(
                        "⚠️ Команда /checkgroup " "вызвана не из группы."
                    )
                )

                return

            if chat_id is None:

                self.stderr.write(
                    self.style.ERROR("❌ Не удалось определить " "chat_id.")
                )

                return

            memberships = get_saved_group_members(chat_id)

            if not memberships:

                bot.send_message(
                    chat_id,
                    "👥 <b>Участники группы</b>\n\n" "Пока нет сохранённых участников.",
                )

                return

            lines = [
                "👥 <b>Участники рабочей группы</b>",
                "",
            ]

            for index, membership in enumerate(
                memberships,
                start=1,
            ):

                user = membership.user

                username = f"@{user.username}" if user.username else "без username"

                full_name = " ".join(
                    part
                    for part in [
                        user.first_name,
                        user.last_name,
                    ]
                    if part
                ).strip()

                if not full_name:

                    full_name = "Без имени"

                lines.append(
                    f"{index}. 👤 <b>{full_name}</b>\n"
                    f"   {username}\n"
                    f"   ID: <code>{user.telegram_id}</code>"
                )

            bot.send_message(
                chat_id,
                "\n".join(lines),
            )

            return

        # ======================================================
        # CLIENT TEXT
        # ======================================================

        handle_client_text(
            bot,
            message,
        )

    # ==========================================================
    # CHAT MEMBER UPDATE
    # ==========================================================

    def handle_chat_member_update(
        self,
        bot,
        chat_member_update,
    ):
        """
        Обрабатывает изменение статуса участника Telegram-чата.

        Если пользователь только что вступил в рабочую группу,
        бот предлагает пройти регистрацию.
        """

        if not isinstance(
            chat_member_update,
            dict,
        ):
            return

        chat = chat_member_update.get("chat", {})

        new_member = chat_member_update.get("new_chat_member", {})

        if not isinstance(
            chat,
            dict,
        ):
            return

        if not isinstance(
            new_member,
            dict,
        ):
            return

        chat_type = chat.get("type")

        if chat_type not in {
            "group",
            "supergroup",
        }:
            return

        chat_id = chat.get("id")

        telegram_user = new_member.get("user", {})

        if not isinstance(
            telegram_user,
            dict,
        ):
            return

        telegram_id = telegram_user.get("id")

        if telegram_id is None:
            return

        old_status = chat_member_update.get("old_chat_member", {}).get("status")

        new_status = new_member.get("status")

        # ======================================================
        # НОВЫЙ ВХОД
        # ======================================================

        joined_statuses = {
            "member",
            "administrator",
        }

        previous_statuses = {
            "left",
            "kicked",
        }

        if new_status not in joined_statuses or old_status not in previous_statuses:
            return

        self.send_employee_registration_message(
            bot,
            chat_id,
            telegram_user,
        )

    # ==========================================================
    # NEW GROUP MEMBER
    # ==========================================================

    def handle_new_group_member(
        self,
        bot,
        chat,
        telegram_user,
    ):
        """
        Обрабатывает системное сообщение Telegram
        о новом участнике группы.
        """

        if not isinstance(
            chat,
            dict,
        ):
            return

        if not isinstance(
            telegram_user,
            dict,
        ):
            return

        chat_type = chat.get("type")

        if chat_type not in {
            "group",
            "supergroup",
        }:
            return

        chat_id = chat.get("id")

        if chat_id is None:
            return

        self.send_employee_registration_message(
            bot,
            chat_id,
            telegram_user,
        )

    # ==========================================================
    # EMPLOYEE REGISTRATION MESSAGE
    # ==========================================================

    def send_employee_registration_message(
        self,
        bot,
        chat_id,
        telegram_user,
    ):
        """Предлагает новому участнику выбрать язык и зарегистрироваться."""

        if chat_id is None:
            return

        telegram_id = telegram_user.get("id")

        if telegram_id is None:
            return

        invite_key = (chat_id, telegram_id)

        # Telegram может прислать два update на одно вступление:
        # chat_member и message.new_chat_members.
        if invite_key in self.employee_registration_invites:
            return

        # Уже зарегистрированного сотрудника повторно не приглашаем.
        existing_employee = Employee.objects.filter(
            telegram_id=telegram_id,
            is_active=True,
        ).first()

        if existing_employee is not None:
            return

        first_name = telegram_user.get("first_name", "") or ""
        last_name = telegram_user.get("last_name", "") or ""

        display_name = " ".join(
            part
            for part in [first_name, last_name]
            if part
        ).strip()

        if not display_name:
            username = telegram_user.get("username", "") or ""
            display_name = f"@{username}" if username else "коллега"

        keyboard = {
            "inline_keyboard": [
                [
                    {
                        "text": "🇷🇺 Русский",
                        "callback_data": "employee_registration:ru",
                    },
                    {
                        "text": "🇺🇿 O'zbekcha",
                        "callback_data": "employee_registration:uz",
                    },
                ],
            ],
        }

        mention = self._employee_registration_mention(
            telegram_user,
            telegram_id,
        )

        text = (
            f"👋 <b>Добро пожаловать, {html.escape(display_name)}!</b>\n\n"
            f"{mention}, выберите язык для регистрации сотрудника.\n\n"
            "🌐 Выберите язык:"
        )

        try:
            bot.send_message(
                chat_id,
                text,
                reply_markup=keyboard,
            )

            self.employee_registration_invites.add(invite_key)

            print(
                "👷 Отправлено приглашение на регистрацию сотруднику: "
                f"telegram_id={telegram_id}"
            )

        except TelegramBotError as exc:
            self.stderr.write(
                self.style.ERROR(
                    "❌ Не удалось отправить приглашение на регистрацию: "
                    f"{exc}"
                )
            )

    def _employee_registration_text(self, language, key):
        texts = {
            "ru": {
                "prompt": (
                    "🌐 <b>Русский язык выбран.</b>\n\n"
                    "📱 Теперь отправьте ваш номер телефона сообщением в эту группу.\n\n"
                    "Например: <code>+998901234567</code>"
                ),
                "invalid": (
                    "❌ Не удалось найти активного сотрудника по этому номеру.\n\n"
                    "Проверьте номер и отправьте его ещё раз."
                ),
                "already_linked": (
                    "⚠️ Этот номер уже привязан к другому Telegram-аккаунту.\n\n"
                    "Если это ваш номер, обратитесь к администратору."
                ),
                "success": (
                    "✅ <b>Регистрация успешно завершена!</b>\n\n"
                    "👷 Сотрудник: <b>{name}</b>\n"
                    "🌐 Язык: Русский\n\n"
                    "Теперь вы будете получать новые заявки от клиентов."
                ),
                "bad_phone": (
                    "❌ Пожалуйста, отправьте корректный номер телефона.\n\n"
                    "Например: <code>+998901234567</code>"
                ),
            },
            "uz": {
                "prompt": (
                    "🌐 <b>O'zbek tili tanlandi.</b>\n\n"
                    "📱 Endi telefon raqamingizni ushbu guruhga xabar sifatida yuboring.\n\n"
                    "Masalan: <code>+998901234567</code>"
                ),
                "invalid": (
                    "❌ Ushbu raqam bo'yicha faol xodim topilmadi.\n\n"
                    "Raqamni tekshirib, qayta yuboring."
                ),
                "already_linked": (
                    "⚠️ Bu raqam boshqa Telegram akkauntiga biriktirilgan.\n\n"
                    "Agar bu sizning raqamingiz bo'lsa, administratorga murojaat qiling."
                ),
                "success": (
                    "✅ <b>Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!</b>\n\n"
                    "👷 Xodim: <b>{name}</b>\n"
                    "🌐 Til: O'zbekcha\n\n"
                    "Endi siz mijozlarning yangi buyurtmalarini olasiz."
                ),
                "bad_phone": (
                    "❌ Iltimos, to'g'ri telefon raqamini yuboring.\n\n"
                    "Masalan: <code>+998901234567</code>"
                ),
            },
        }
        return texts.get(language, texts["ru"])[key]

    def _employee_registration_mention(self, telegram_user, telegram_id):
        """Возвращает безопасное персональное упоминание пользователя."""

        first_name = (telegram_user.get("first_name", "") or "").strip()
        last_name = (telegram_user.get("last_name", "") or "").strip()
        username = (telegram_user.get("username", "") or "").strip()

        display_name = " ".join(
            part
            for part in [first_name, last_name]
            if part
        ).strip()

        if not display_name:
            display_name = f"@{username}" if username else "коллега"

        return (
            f'<a href="tg://user?id={telegram_id}">'
            f"{html.escape(display_name)}"
            "</a>"
        )

    def _employee_registration_prompt_markup(self, language):
        """ForceReply с selective=True, чтобы поле ответа показывалось адресату."""

        return {
            "force_reply": True,
            "selective": True,
            "input_field_placeholder": (
                "Введите номер телефона"
                if language == "ru"
                else "Telefon raqamingizni kiriting"
            ),
        }

    def _employee_registration_prompt(
        self,
        language,
        telegram_user,
        telegram_id,
        error_key=None,
    ):
        """Формирует одну персональную подсказку вместо пары сообщений."""

        mention = self._employee_registration_mention(
            telegram_user,
            telegram_id,
        )

        if error_key:
            error_text = self._employee_registration_text(
                language,
                error_key,
            )
            base_prompt = self._employee_registration_text(
                language,
                "prompt",
            )
            return f"{error_text}\n\n{mention},\n{base_prompt}"

        return f"{mention},\n{self._employee_registration_text(language, 'prompt')}"

    def _delete_employee_registration_message(
        self,
        bot,
        chat_id,
        message_id,
        label,
    ):
        """Пытается удалить регистрационное сообщение и не ломает flow при 400."""

        if not message_id:
            return False

        try:
            bot.delete_message(
                chat_id,
                message_id,
            )
            return True
        except TelegramBotError as exc:
            print(
                f"⚠️ Не удалось удалить {label}: {exc}"
            )
            return False

    def handle_employee_registration_language(
        self,
        bot,
        callback_query,
    ):
        """Обрабатывает выбор языка регистрации сотрудника в группе."""

        callback_query_id = callback_query.get("id")
        telegram_user = callback_query.get("from", {}) or {}
        telegram_id = telegram_user.get("id")
        data = callback_query.get("data", "") or ""
        callback_message = callback_query.get("message", {}) or {}
        chat = callback_message.get("chat", {}) or {}
        chat_id = chat.get("id")
        chat_type = chat.get("type")
        message_id = callback_message.get("message_id")

        if not callback_query_id or not telegram_id:
            return

        if chat_type not in {"group", "supergroup"} or chat_id is None:
            bot.answer_callback_query(
                callback_query_id,
                text="Регистрация сотрудника доступна только в рабочей группе.",
                show_alert=True,
            )
            return

        try:
            _, language = data.split(":", 1)
        except ValueError:
            bot.answer_callback_query(
                callback_query_id,
                text="Некорректный язык.",
                show_alert=True,
            )
            return

        if language not in {"ru", "uz"}:
            bot.answer_callback_query(
                callback_query_id,
                text="Некорректный язык.",
                show_alert=True,
            )
            return

        sync_telegram_user(telegram_user)

        employee = Employee.objects.filter(
            telegram_id=telegram_id,
            is_active=True,
        ).first()

        if employee is not None:
            # Старая кнопка регистрации могла остаться в группе.
            # Не позволяем зарегистрированному сотруднику повторно
            # запускать регистрацию и удаляем устаревшее сообщение.
            self.employee_registration_sessions.pop(telegram_id, None)

            if message_id:
                try:
                    bot.delete_message(
                        chat_id,
                        message_id,
                    )
                except TelegramBotError as exc:
                    print(
                        "⚠️ Не удалось удалить старое сообщение регистрации: "
                        f"{exc}"
                    )

            bot.answer_callback_query(
                callback_query_id,
                text="Вы уже зарегистрированы как сотрудник.",
                show_alert=True,
            )
            return

        self.employee_registration_sessions[telegram_id] = {
            "chat_id": chat_id,
            "language": language,
        }

        bot.answer_callback_query(
            callback_query_id,
            text="Язык выбран." if language == "ru" else "Til tanlandi.",
            show_alert=False,
        )

        # Убираем сообщение с выбором языка, чтобы группа не засорялась.
        if message_id:
            try:
                bot.delete_message(
                    chat_id,
                    message_id,
                )
            except TelegramBotError as exc:
                print(
                    "⚠️ Не удалось удалить сообщение выбора языка: "
                    f"{exc}"
                )

        prompt_message = bot.send_message(
            chat_id,
            self._employee_registration_prompt(
                language,
                telegram_user,
                telegram_id,
            ),
            reply_markup=self._employee_registration_prompt_markup(language),
        )

        if isinstance(prompt_message, dict):
            prompt_message_id = prompt_message.get("message_id")
            if prompt_message_id is not None:
                self.employee_registration_sessions[telegram_id][
                    "prompt_message_id"
                ] = prompt_message_id

        print(
            "🌐 Язык регистрации сотрудника выбран: "
            f"telegram_id={telegram_id}, language={language}"
        )

    def handle_employee_registration_text(
        self,
        bot,
        message,
    ):
        """Обрабатывает номер телефона сотрудника в рабочей группе."""

        telegram_user = message.get("from", {}) or {}
        telegram_id = telegram_user.get("id")
        chat = message.get("chat", {}) or {}
        chat_id = chat.get("id")
        message_id = message.get("message_id")
        text = (message.get("text") or "").strip()

        if not telegram_id or chat_id is None or not text:
            return False

        session = self.employee_registration_sessions.get(telegram_id)
        if not session or session.get("chat_id") != chat_id:
            return False

        processed_key = (chat_id, message_id)
        if message_id is not None and processed_key in self.employee_registration_processed_messages:
            print(
                "ℹ️ Повторное update одного сообщения регистрации пропущен: "
                f"chat_id={chat_id}, message_id={message_id}, telegram_id={telegram_id}"
            )
            return True

        if message_id is not None:
            self.employee_registration_processed_messages.add(processed_key)

        print(
            "📱 Получен текст для регистрации сотрудника: "
            f"telegram_id={telegram_id}, chat_id={chat_id}, text={text!r}"
        )

        # Дополнительная защита: сотрудник мог быть зарегистрирован
        # уже после создания регистрационной сессии.
        existing_employee = Employee.objects.filter(
            telegram_id=telegram_id,
            is_active=True,
        ).first()

        if existing_employee is not None:
            self.employee_registration_sessions.pop(telegram_id, None)

            if message_id:
                try:
                    bot.delete_message(
                        chat_id,
                        message_id,
                    )
                except TelegramBotError as exc:
                    print(
                        "⚠️ Не удалось удалить сообщение зарегистрированного сотрудника: "
                        f"{exc}"
                    )

            bot.send_message(
                chat_id,
                "⚠️ Вы уже зарегистрированы как сотрудник.",
            )
            return True

        language = session.get("language", "ru")

        # Номер больше не должен оставаться в рабочей группе.
        self._delete_employee_registration_message(
            bot,
            chat_id,
            message_id,
            "сообщение с номером телефона",
        )

        prompt_message_id = session.get("prompt_message_id")

        normalized_phone = normalize_phone(text)

        if len(normalized_phone) < 9 or len(normalized_phone) > 15:
            # Не создаём второй полный блок инструкции: старое сообщение
            # может остаться в группе, если у бота нет права Delete messages.
            # Поэтому после ошибки отправляем только компактное сообщение
            # с новой персональной ForceReply-подсказкой.
            retry_text = (
                self._employee_registration_text(language, "bad_phone")
                + "\n\n"
                + self._employee_registration_mention(telegram_user, telegram_id)
                + (
                    ", отправьте номер ещё раз."
                    if language == "ru"
                    else ", raqamni yana yuboring."
                )
            )
            prompt_message = bot.send_message(
                chat_id,
                retry_text,
                reply_markup=self._employee_registration_prompt_markup(language),
            )
            if isinstance(prompt_message, dict):
                session["prompt_message_id"] = prompt_message.get("message_id")
            return True

        # Ищем сотрудника по номеру.
        # Если такого сотрудника ещё нет — он будет создан ниже.
        employee = find_employee_by_phone(normalized_phone)

        with transaction.atomic():
            # Повторно ищем сотрудника уже внутри транзакции.
            # Это важно, чтобы два одновременных запроса не создали
            # двух сотрудников с одним и тем же номером.
            employee = (
                Employee.objects
                .select_for_update()
                .filter(
                    phone=normalized_phone,
                    is_active=True,
                )
                .first()
            )

            if employee is not None:
                # Номер уже существует в базе.
                # Проверяем, не привязан ли он к другому Telegram.
                if (
                    employee.telegram_id is not None
                    and employee.telegram_id != telegram_id
                ):
                    self.employee_registration_sessions.pop(
                        telegram_id,
                        None,
                    )
                    self.employee_registration_invites.discard(
                        (chat_id, telegram_id)
                    )

                    self._delete_employee_registration_message(
                        bot,
                        chat_id,
                        prompt_message_id,
                        "подсказку регистрации",
                    )

                    bot.send_message(
                        chat_id,
                        self._employee_registration_text(
                            language,
                            "already_linked",
                        ),
                    )

                    return True

            else:
                # ---------------------------------------------------------
                # НОВЫЙ СОТРУДНИК
                # ---------------------------------------------------------
                # Сотрудника с таким номером ещё нет.
                # Создаём его автоматически из данных Telegram.
                # ---------------------------------------------------------

                first_name = (
                    telegram_user.get("first_name", "")
                    or ""
                ).strip()

                last_name = (
                    telegram_user.get("last_name", "")
                    or ""
                ).strip()

                username = (
                    telegram_user.get("username", "")
                    or ""
                ).strip()

                # Формируем имя нового сотрудника.
                name_parts = [
                    part
                    for part in [first_name, last_name]
                    if part
                ]

                if name_parts:
                    employee_name = " ".join(name_parts)
                elif username:
                    employee_name = f"@{username}"
                else:
                    employee_name = f"Telegram {telegram_id}"

                employee = Employee.objects.create(
                    name=employee_name,
                    position="Сантехник",
                    experience=0,
                    phone=normalized_phone,
                    language=language,
                    telegram_id=telegram_id,
                    telegram_username=username,
                    is_active=True,
                )

                print(
                    "🆕 Создан новый сотрудник: "
                    f"employee_id={employee.id}, "
                    f"name={employee.name}, "
                    f"phone={employee.phone}, "
                    f"telegram_id={telegram_id}"
                )

            # -------------------------------------------------------------
            # Привязываем Telegram к существующему или только что
            # созданному сотруднику.
            # -------------------------------------------------------------

            employee.telegram_id = telegram_id
            employee.telegram_username = (
                telegram_user.get("username", "")
                or ""
            )
            employee.language = language

            employee.save(
                update_fields=[
                    "telegram_id",
                    "telegram_username",
                    "language",
                    "updated_at",
                ]
            )

        # -------------------------------------------------------------
        # Регистрация завершена.
        # -------------------------------------------------------------

        self.employee_registration_sessions.pop(
            telegram_id,
            None,
        )

        self.employee_registration_invites.discard(
            (chat_id, telegram_id)
        )

        # Удаляем сообщение-подсказку с запросом телефона.
        self._delete_employee_registration_message(
            bot,
            chat_id,
            prompt_message_id,
            "подсказку регистрации",
        )

        # Сообщаем об успешной регистрации.
        bot.send_message(
            chat_id,
            self._employee_registration_text(
                language,
                "success",
            ).format(
                name=employee.name,
            ),
        )

        print(
            "✅ Сотрудник зарегистрирован в группе: "
            f"employee_id={employee.id}, "
            f"telegram_id={telegram_id}, "
            f"language={language}, "
            f"phone={employee.phone}"
        )

        return True

