from django.db import transaction

from django.utils import timezone



from employees.models import Employee

from service_requests.models import (

    ServiceRequest,

    ServiceRequestEmployeeResponse,

)



from ..client_handlers import (

    build_client_rating_text,

    get_client_rating_keyboard,

    handle_client_callback,

)

from ..services import TelegramBot, TelegramBotError



from .common import (

    set_telegram_user_language,

    sync_telegram_user,

)

from .start import (

    get_language,

    send_client_phone_request,

)


# ==========================================================
# CLIENT UI MESSAGE
# ==========================================================


def _get_client_ui_message_id(client):
    """
    Возвращает ID основного UI-сообщения клиента.

    В процессе создания заявки это сообщение редактируется
    в финальный экран "Request created successfully".
    Поэтому при принятии заявки его можно удалить, не затрагивая
    данные ServiceRequest в базе.
    """

    if client is None:
        return None

    value = client.get_draft_value(
        "ui_message_id",
    )

    try:
        return int(value)
    except (
        TypeError,
        ValueError,
    ):
        return None


def _clear_client_ui_message_id(client):
    """Удаляет сохранённый ID UI-сообщения клиента."""

    if client is None:
        return

    draft = dict(
        client.draft_data or {},
    )

    if "ui_message_id" not in draft:
        return

    del draft["ui_message_id"]

    client.draft_data = draft
    client.save(
        update_fields=[
            "draft_data",
            "updated_at",
        ],
    )



# ==========================================================

# LANGUAGE SELECTION

# ==========================================================





SUPPORTED_LANGUAGES = {

    "ru",

    "uz",

    "en",

    "zh",

}





def handle_language_callback(

    bot,

    callback_query_id,

    telegram_id,

    language,

):

    """

    Обрабатывает выбор языка нового пользователя.



    callback_data:

        language:ru

        language:uz

        language:en

        language:zh



    После выбора:

        TelegramUser.language = выбранный язык

        TelegramUser.language_selected = True



    Затем бот просит пользователя отправить номер телефона.

    """



    language = (language or "").lower().strip()



    if language not in SUPPORTED_LANGUAGES:

        bot.answer_callback_query(

            callback_query_id,

            text="Некорректный язык.",

            show_alert=True,

        )

        return



    success = set_telegram_user_language(

        telegram_id,

        language,

    )



    if not success:

        bot.answer_callback_query(

            callback_query_id,

            text="Не удалось сохранить выбранный язык.",

            show_alert=True,

        )

        return



    language = get_language(

        language,

        default="ru",

    )



    language_names = {

        "ru": "Русский",

        "uz": "O'zbekcha",

        "en": "English",

        "zh": "中文",

    }



    selected_language_name = language_names.get(

        language,

        language,

    )



    bot.answer_callback_query(

        callback_query_id,

        text=f"Язык выбран: {selected_language_name}",

        show_alert=False,

    )



    # Получаем данные пользователя из callback.

    callback_user = {}



    # Сам Telegram ID уже известен.

    # Имя для запроса телефона здесь не обязательно.

    send_client_phone_request(

        bot,

        telegram_id,

        language,

    )



    print(

        "🌐 Язык пользователя сохранён: "

        f"telegram_id={telegram_id}, "

        f"language={language}"

    )





# ==========================================================

# CALLBACK QUERY

# ==========================================================





def handle_callback_query(

    bot,

    callback_query,

):

    """

    Обрабатывает inline-кнопки:



    \- выбора языка;

    \- клиента;

    \- сотрудника.

    """



    callback_query_id = callback_query.get(

        "id",

    )



    data = callback_query.get(

        "data",

        "",

    )



    telegram_user = callback_query.get(

        "from",

        {},

    )



    telegram_id = telegram_user.get(

        "id",

    )



    if not callback_query_id or not telegram_id:

        return



    # ======================================================

    # СОХРАНЯЕМ TELEGRAM USER

    # ======================================================



    sync_telegram_user(

        telegram_user,

    )



    print(

        f"🔘 handle_callback_query(): " f"telegram_id={telegram_id}, " f"data={data!r}"

    )



    # ======================================================

    # ВЫБОР ЯЗЫКА

    # ======================================================



    if data.startswith("language:"):



        print(f"🌐 Языковой callback: {data}")



        parts = data.split(":", 1)



        if len(parts) != 2:

            bot.answer_callback_query(

                callback_query_id,

                text="Некорректные данные языка.",

                show_alert=True,

            )

            return



        _, language = parts



        handle_language_callback(

            bot,

            callback_query_id,

            telegram_id,

            language,

        )



        return



    # ======================================================

    # ПУСТАЯ КНОПКА

    # ======================================================



    if data == "noop":



        bot.answer_callback_query(

            callback_query_id,

            text="Сейчас нет доступных сантехников.",

            show_alert=True,

        )



        return



    # ======================================================

    # КЛИЕНТ

    # ======================================================



    if data.startswith("client:"):



        print(f"👤 Клиентский callback: {data}")



        handle_client_callback(

            bot,

            callback_query,

        )



        return



    # ======================================================

    # СОТРУДНИК

    # ======================================================



    prefix = "request_response:"



    if not data.startswith(prefix):



        bot.answer_callback_query(

            callback_query_id,

            text="Неизвестная команда.",

            show_alert=True,

        )



        return



    # ======================================================

    # CALLBACK PARSE

    # ======================================================



    try:



        parts = data.split(":")



        if len(parts) != 3:

            raise ValueError



        _, request_id, action = parts



        request_id = int(

            request_id,

        )



    except (

        ValueError,

        TypeError,

    ):



        bot.answer_callback_query(

            callback_query_id,

            text="Некорректные данные заявки.",

            show_alert=True,

        )



        return



    # ======================================================

    # ACTION

    # ======================================================



    allowed_actions = {

        "accepted",

        "declined",

        "change",

        "completed",

    }



    if action not in allowed_actions:



        bot.answer_callback_query(

            callback_query_id,

            text="Неизвестное действие.",

            show_alert=True,

        )



        return



    # ======================================================

    # EMPLOYEE

    # ======================================================



    employee = Employee.objects.filter(

        telegram_id=telegram_id,

        is_active=True,

    ).first()



    if employee is None:



        bot.answer_callback_query(

            callback_query_id,

            text="Ваш Telegram не привязан к сотруднику.",

            show_alert=True,

        )



        return



    print(

        f"👷 Сотрудник: {employee.name} "

        f"(id={employee.id}, language={employee.language})"

    )



    # ======================================================

    # SERVICE REQUEST

    # ======================================================



    now = timezone.now()

    action_text = ""

    request_completed = False

    notify_client_about_assignment = False


    # TRANSACTION

    # ======================================================



    with transaction.atomic():



        # Блокируем саму заявку на время обработки callback.

        # Это гарантирует правило: первый сотрудник, принявший заявку,

        # становится единственным исполнителем даже при почти

        # одновременных нажатиях кнопки несколькими сотрудниками.

        # Блокируем только строку ServiceRequest.
        # select_for_update(of=("self",)) не блокирует nullable JOIN
        # telegram_client и устраняет ошибку PostgreSQL FOR UPDATE.
        service_request = (
            ServiceRequest.objects.select_for_update(of=("self",))
            .select_related(
                "service",
                "telegram_client",
            )
            .filter(pk=request_id)
            .first()
        )

        if service_request is None:
            bot.answer_callback_query(
                callback_query_id,
                text="Заявка не найдена.",
                show_alert=True,
            )
            return

        print(f"📋 Заявка #{service_request.id}: status={service_request.status}")

        is_consultation = (
            service_request.request_type == ServiceRequest.REQUEST_TYPE_CONSULTATION
        )

        # Проверяем закрытое состояние уже под блокировкой.
        if service_request.status in {
            ServiceRequest.STATUS_COMPLETED,
            ServiceRequest.STATUS_CANCELLED,
        }:
            bot.answer_callback_query(
                callback_query_id,
                text="Эта заявка уже закрыта.",
                show_alert=True,
            )
            return

        (

            response,

            created,

        ) = ServiceRequestEmployeeResponse.objects.select_for_update().get_or_create(

            service_request=service_request,

            employee=employee,

            defaults={

                "status": (ServiceRequestEmployeeResponse.STATUS_PENDING),

            },

        )



        print(

            f"👷 Ответ сотрудника: " f"status={response.status}, " f"created={created}"

        )



        # ==================================================

        # ACCEPTED

        # ==================================================



        if action == "accepted":



            # Только первый сотрудник может принять новую заявку.

            # Если заявка уже находится в работе и этот сотрудник

            # не является назначенным исполнителем, второй сотрудник

            # не может забрать её себе.

            if (

                service_request.status != ServiceRequest.STATUS_NEW

                and not service_request.employees.filter(id=employee.id).exists()

                and not response.had_accepted

            ):

                bot.answer_callback_query(

                    callback_query_id,

                    text=(

                        "Эту консультацию уже принял другой сотрудник."

                        if is_consultation

                        else "Эту заявку уже принял другой сантехник."

                    ),

                    show_alert=True,

                )

                return



            if response.status == ServiceRequestEmployeeResponse.STATUS_ACCEPTED:



                bot.answer_callback_query(

                    callback_query_id,

                    text=(

                        "Вы уже приняли консультацию."

                        if is_consultation

                        else "Вы уже подтвердили, что едете."

                    ),

                    show_alert=False,

                )



                return



            if response.status == ServiceRequestEmployeeResponse.STATUS_COMPLETED:



                bot.answer_callback_query(

                    callback_query_id,

                    text="Вы уже отметили заявку выполненной.",

                    show_alert=False,

                )



                return



            response.status = ServiceRequestEmployeeResponse.STATUS_ACCEPTED



            response.responded_at = now



            response.had_accepted = True



            response.save(

                update_fields=[

                    "status",

                    "responded_at",

                    "had_accepted",

                    "updated_at",

                ],

            )



            service_request.employees.add(

                employee,

            )



            if service_request.status == ServiceRequest.STATUS_NEW:



                service_request.status = ServiceRequest.STATUS_IN_PROGRESS



                service_request.save(

                    update_fields=[

                        "status",

                        "updated_at",

                    ],

                )



            notify_client_about_assignment = True



            action_text = (

                "Вы приняли: КОНСУЛЬТАЦИЮ 💬"

                if is_consultation

                else "Вы подтвердили: Я ЕДУ 🚰"

            )



        # ==================================================

        # DECLINED

        # ==================================================



        elif action == "declined":



            if response.status == ServiceRequestEmployeeResponse.STATUS_DECLINED:



                bot.answer_callback_query(

                    callback_query_id,

                    text="Вы уже отказались от этой заявки.",

                    show_alert=False,

                )



                return



            if response.status == ServiceRequestEmployeeResponse.STATUS_COMPLETED:



                bot.answer_callback_query(

                    callback_query_id,

                    text="Вы уже выполнили эту заявку.",

                    show_alert=False,

                )



                return



            response.status = ServiceRequestEmployeeResponse.STATUS_DECLINED



            response.responded_at = now



            response.save(

                update_fields=[

                    "status",

                    "responded_at",

                    "updated_at",

                ],

            )



            service_request.employees.remove(

                employee,

            )



            action_text = "Вы ответили: НЕ МОГУ ❌"



        # ==================================================

        # CHANGE

        # ==================================================



        elif action == "change":



            if response.status == ServiceRequestEmployeeResponse.STATUS_PENDING:



                bot.answer_callback_query(

                    callback_query_id,

                    text="Выберите новый ответ.",

                    show_alert=False,

                )



                return



            if response.status == ServiceRequestEmployeeResponse.STATUS_COMPLETED:



                bot.answer_callback_query(

                    callback_query_id,

                    text="Выполненную заявку изменить нельзя.",

                    show_alert=True,

                )



                return



            response.status = ServiceRequestEmployeeResponse.STATUS_PENDING



            response.responded_at = None



            response.save(

                update_fields=[

                    "status",

                    "responded_at",

                    "updated_at",

                ],

            )



            service_request.employees.remove(

                employee,

            )



            action_text = "Ответ сброшен. " "Вы можете выбрать новый вариант."



        # ==================================================

        # COMPLETED

        # ==================================================



        elif action == "completed":



            # ==============================================

            # CHECK ASSIGNMENT

            # ==============================================



            if not service_request.employees.filter(

                id=employee.id,

            ).exists():



                bot.answer_callback_query(

                    callback_query_id,

                    text="Вы не назначены на эту заявку.",

                    show_alert=True,

                )



                return



            # ==============================================

            # ALREADY COMPLETED

            # ==============================================



            if response.status == ServiceRequestEmployeeResponse.STATUS_COMPLETED:



                bot.answer_callback_query(

                    callback_query_id,

                    text="Вы уже отметили заявку выполненной.",

                    show_alert=False,

                )



                return



            # ==============================================

            # MUST BE ACCEPTED

            # ==============================================



            if response.status != ServiceRequestEmployeeResponse.STATUS_ACCEPTED:



                bot.answer_callback_query(

                    callback_query_id,

                    text=(

                        "Сначала необходимо принять консультацию."

                        if is_consultation

                        else ("Сначала необходимо " "подтвердить «Я ЕДУ».")

                    ),

                    show_alert=True,

                )



                return



            # ==============================================

            # MARK EMPLOYEE COMPLETED

            # ==============================================



            response.status = ServiceRequestEmployeeResponse.STATUS_COMPLETED



            response.responded_at = now



            response.save(

                update_fields=[

                    "status",

                    "responded_at",

                    "updated_at",

                ],

            )



            action_text = (

                "Вы завершили консультацию: ГОТОВО ✅"

                if is_consultation

                else "Вы отметили заявку как ВЫПОЛНЕННУЮ ✅"

            )



            # ==============================================

            # CHECK OTHER EMPLOYEES

            # ==============================================



            assigned_employees = list(

                service_request.employees.filter(

                    is_active=True,

                )

            )



            assigned_employee_ids = {

                assigned_employee.id for assigned_employee in assigned_employees

            }



            completed_employee_ids = set(

                ServiceRequestEmployeeResponse.objects.filter(

                    service_request=service_request,

                    employee_id__in=assigned_employee_ids,

                    status=(ServiceRequestEmployeeResponse.STATUS_COMPLETED),

                ).values_list(

                    "employee_id",

                    flat=True,

                )

            )



            # ==============================================

            # ALL ASSIGNED EMPLOYEES COMPLETED

            # ==============================================



            if (

                assigned_employee_ids

                and assigned_employee_ids == completed_employee_ids

            ):



                service_request.status = ServiceRequest.STATUS_COMPLETED



                if service_request.completed_at is None:

                    service_request.completed_at = now



                # ------------------------------------------

                # УДАЛЯЕМ ГЕОЛОКАЦИЮ

                # ------------------------------------------



                service_request.latitude = None

                service_request.longitude = None



                service_request.save(

                    update_fields=[

                        "status",

                        "completed_at",

                        "latitude",

                        "longitude",

                        "updated_at",

                    ],

                )



                request_completed = True



                print(f"🏁 Заявка #{service_request.id} " "полностью завершена.")



                print(

                    f"🔒 Геолокация заявки "

                    f"#{service_request.id} "

                    "очищена из базы."

                )



    # ======================================================

    # ANSWER CALLBACK

    # ======================================================



    bot.answer_callback_query(

        callback_query_id,

        text=action_text,

        show_alert=False,

    )



    # ======================================================

    # CLIENT ASSIGNMENT NOTIFICATION

    # ======================================================



    if action == "accepted" and notify_client_about_assignment:



        from telegram_bot.notifications import (

            notify_client_employee_assigned,

        )



        try:



            sent_message = notify_client_employee_assigned(

                service_request,

                employee,

            )



            message_id = (

                sent_message.get("result", {}).get("message_id")

                if isinstance(sent_message, dict)

                else None

            )



            if message_id:

                service_request.client_assignment_message_id = message_id

                service_request.save(

                    update_fields=[

                        "client_assignment_message_id",

                        "updated_at",

                    ],

                )

                print(

                    "💾 Сохранён message_id уведомления клиенту: "

                    f"{message_id} (заявка #{service_request.id})"

                )



            print(

                "✅ Клиент уведомлён о назначении "

                f"сантехника: {employee.name}, "

                f"заявка #{service_request.id}"

            )

        except TelegramBotError as exc:



            print(

                "⚠️ Не удалось уведомить клиента " "о назначении сантехника: " f"{exc}"

            )



        except Exception as exc:



            print(

                "⚠️ Неожиданная ошибка при отправке " "уведомления клиенту: " f"{exc}"

            )



    # ======================================================
    # DELETE CLIENT REQUEST-CREATED MESSAGE
    # ======================================================

    if action == "accepted" and notify_client_about_assignment:

        telegram_client = service_request.telegram_client
        client_ui_message_id = _get_client_ui_message_id(
            telegram_client,
        )

        if (
            client_ui_message_id
            and telegram_client
            and telegram_client.telegram_id
        ):
            try:
                delete_result = bot.delete_message(
                    chat_id=telegram_client.telegram_id,
                    message_id=client_ui_message_id,
                )

                if delete_result and delete_result.get("ok"):
                    print(
                        "🗑️ Удалено сообщение о создании заявки у клиента: "
                        f"message_id={client_ui_message_id}, "
                        f"заявка #{service_request.id}"
                    )
                    _clear_client_ui_message_id(
                        telegram_client,
                    )
                else:
                    print(
                        "⚠️ Telegram не подтвердил удаление сообщения "
                        "о создании заявки: "
                        f"заявка #{service_request.id}. "
                        "ID оставлен в draft_data."
                    )

            except TelegramBotError as exc:
                print(
                    "⚠️ Не удалось удалить сообщение о создании заявки "
                    f"#{service_request.id}: {exc}"
                )
            except Exception as exc:
                print(
                    "⚠️ Неожиданная ошибка при удалении сообщения "
                    "о создании заявки "
                    f"#{service_request.id}: {exc}"
                )

    # ======================================================
    # REQUEST COMPLETED -> RATING
    # ======================================================



    if action == "completed" and request_completed:


        service_request.refresh_from_db()


        # Удаляем у клиента старое уведомление о назначении сантехника.
        client_assignment_message_id = (

            service_request.client_assignment_message_id

        )

        telegram_client = service_request.telegram_client


        if (

            client_assignment_message_id

            and telegram_client

            and telegram_client.telegram_id

        ):

            try:

                delete_result = bot.delete_message(

                    chat_id=telegram_client.telegram_id,

                    message_id=client_assignment_message_id,

                )


                if delete_result and delete_result.get("ok"):

                    print(

                        "🗑️ Удалено сообщение о назначении у клиента: "

                        f"message_id={client_assignment_message_id}, "

                        f"заявка #{service_request.id}"

                    )

                    service_request.client_assignment_message_id = None

                    service_request.save(

                        update_fields=[

                            "client_assignment_message_id",

                            "updated_at",

                        ],

                    )

                else:

                    print(

                        "⚠️ Telegram не подтвердил удаление сообщения о "

                        f"назначении заявки #{service_request.id}. "

                        "ID оставлен в базе."

                    )


            except TelegramBotError as exc:

                print(

                    "⚠️ Не удалось удалить сообщение о назначении "

                    f"заявки #{service_request.id}: {exc}"

                )

            except Exception as exc:

                print(

                    "⚠️ Неожиданная ошибка при удалении сообщения о "

                    f"назначении заявки #{service_request.id}: {exc}"

                )

        elif client_assignment_message_id:

            print(

                "⚠️ Не удалось удалить сообщение о назначении заявки "

                f"#{service_request.id}: отсутствует Telegram-клиент "

                "или Telegram ID клиента."

            )






        if telegram_client is None:



            print(

                "⚠️ Заявка "

                f"#{service_request.id} "

                "не связана с Telegram-клиентом. "

                "Оценку отправить невозможно."

            )



        elif not telegram_client.telegram_id:



            print(

                "⚠️ У Telegram-клиента заявки "

                f"#{service_request.id} "

                "отсутствует Telegram ID."

            )



        elif service_request.rating is not None:



            print(

                "ℹ️ Заявка "

                f"#{service_request.id} "

                "уже имеет оценку. "

                "Повторный запрос не отправляем."

            )



        else:



            rating_text = build_client_rating_text(

                service_request,

                telegram_client,

            )



            rating_keyboard = get_client_rating_keyboard(

                service_request,

                telegram_client,

            )



            try:



                bot.send_message(

                    telegram_client.telegram_id,

                    rating_text,

                    reply_markup=rating_keyboard,

                )



                print(

                    "⭐ Клиенту отправлен запрос "

                    "на оценку заявки "

                    f"#{service_request.id}"

                )



            except TelegramBotError as exc:



                print(

                    "⚠️ Не удалось отправить клиенту "

                    "запрос на оценку заявки "

                    f"#{service_request.id}: {exc}"

                )



            except Exception as exc:



                print(

                    "⚠️ Неожиданная ошибка при отправке "

                    "запроса на оценку заявки "

                    f"#{service_request.id}: {exc}"

                )



    # ======================================================

    # UPDATE GROUP MESSAGE

    # ======================================================



    message = callback_query.get(

        "message",

    )



    if not message:



        print("⚠️ В callback_query " "отсутствует message.")



        return



    chat = message.get(

        "chat",

        {},

    )



    chat_id = chat.get(

        "id",

    )



    message_id = message.get(

        "message_id",

    )



    if not chat_id or not message_id:



        print("⚠️ Не удалось определить " "chat_id/message_id группы.")



        return



    # ======================================================

    # NOTIFICATIONS

    # ======================================================



    from telegram_bot.notifications import (

        format_service_request_message,

        get_group_keyboard,

    )



    service_request.refresh_from_db()



    # ======================================================

    # GROUP KEYBOARD

    # ======================================================



    try:



        group_keyboard = get_group_keyboard(

            service_request,

        )



        print("🔘 Общая клавиатура заявки " "подготовлена.")



        # --------------------------------------------------

        # COMPLETED

        # --------------------------------------------------



        if service_request.status == ServiceRequest.STATUS_COMPLETED:



            print(f"🏁 Заявка #{service_request.id} " "завершена.")



            print("🔒 Геолокация клиента " "больше не доступна.")



        # --------------------------------------------------

        # CANCELLED

        # --------------------------------------------------



        elif service_request.status == ServiceRequest.STATUS_CANCELLED:



            print(f"🚫 Заявка #{service_request.id} " "отменена.")



        # --------------------------------------------------

        # ACTIVE

        # --------------------------------------------------



        else:



            print("📋 Обновляется активная " "заявка.")



        bot.edit_message_text(

            chat_id=chat_id,

            message_id=message_id,

            text=format_service_request_message(

                service_request,

            ),

            reply_markup=group_keyboard,

        )



        print("✅ Сообщение заявки в группе " "обновлено.")



    except TelegramBotError as exc:



        print("⚠️ Не удалось обновить сообщение " "заявки в группе: " f"{exc}")



    except Exception as exc:



        print(

            "⚠️ Неожиданная ошибка при обновлении "

            "сообщения заявки в группе: "

            f"{exc}"

        )
