import re

SUPPORTED_LANGUAGES = ("ru", "uz", "en", "zh")

DEFAULT_LANGUAGE = "ru"

TRANSLATIONS = {

    # ==========================================================

    # RUSSIAN

    # ==========================================================

    "ru": {

        # ======================================================

        # COMMON

        # ======================================================

        "cancel": "❌ Отмена",

        "skip": "⏭ Пропустить",

        "back_to_menu": "⬅️ Главное меню",

        # ======================================================

        # MAIN MENU

        # ======================================================

        "menu_create": "📝 Создать заявку",

        "menu_requests": "📋 Мои заявки",

        "menu_services": "ℹ️ Услуги",

        "menu_contact": "📞 Связаться",

        "welcome": (

            "👋 <b>{name}</b>\n\n"

            "Добро пожаловать в «Изумруд Сервис».\n\n"

            "Что хотите сделать?"

        ),

        "client_not_registered": (

            "⚠️ Ваш Telegram ещё не зарегистрирован.\n\n" "Отправьте команду /start."

        ),

        "client_not_found": (

            "⚠️ Клиент не найден.\n\n"

            "Для регистрации отправьте свой номер через /start."

        ),

        "client_not_found_start": ("⚠️ Клиент не найден.\n\n" "Отправьте /start."),

        "unknown_command": (

            "Я не совсем понял команду.\n\n" "Выберите действие из меню."

        ),

        # ======================================================

        # SERVICES

        # ======================================================

        "services_title": "ℹ️ <b>Наши услуги</b>",

        "services_empty": ("ℹ️ <b>Наши услуги</b>\n\n" "Сейчас список услуг пуст."),

        "services_category_other": "Другие услуги",

        "services_price_from_unit": " — от {price} за {unit}",

        "services_price_from": " — от {price}",

        "services_price_to_be_confirmed": " — стоимость уточняется",

        # Aliases for formatter compatibility

        "price_from": " — от {price} за {unit}",

        "price_from_without_unit": " — от {price}",

        "price_to_be_confirmed": " — стоимость уточняется",

        # ======================================================

        # CREATE REQUEST

        # ======================================================

        "create_request_title": (

            "📝 <b>Создание заявки</b>\n\n" "Выберите необходимую услугу:"

        ),

        "create_request_unavailable": (

            "❌ <b>Создание заявки недоступно.</b>\n\n" "Список услуг пока пуст."

        ),

        "service_unavailable": (

            "❌ <b>Услуга недоступна.</b>\n\n" "Пожалуйста, выберите услугу заново."

        ),

        "selected_service": (

            "🔧 <b>Вы выбрали:</b>\n\n"

            "{name}\n\n"

            "{price_text}\n\n"

            "⚠️ Это предварительная стоимость.\n"

            "Окончательная цена может зависеть от объёма и сложности работ."

        ),

        "selected_service_price": (

            "💰 <b>Предварительная стоимость:</b>\n" "от {price}"

        ),

        "selected_service_price_unknown": (

            "💰 <b>Стоимость:</b>\n" "уточняется специалистом"

        ),

        "estimated_price": ("💰 <b>Предварительная стоимость:</b>\n" "от {price}"),

        "estimated_price_with_unit": (

            "💰 <b>Предварительная стоимость:</b>\n" "от {price} за {unit}"

        ),

        "price_specialist": ("💰 <b>Стоимость:</b>\n" "уточняется специалистом"),

        # ======================================================

        # LOCATION

        # ======================================================

        "share_location": "📍 Поделиться геолокацией",

        "location_prompt": (

            "📍 <b>Место выполнения работ</b>\n\n"

            "Нажмите кнопку <b>«📍 Поделиться геолокацией»</b> ниже.\n\n"

            "Telegram автоматически отправит ваше местоположение боту.\n\n"

            "📍 Геолокация нужна, чтобы сантехник смог точно определить место выезда."

        ),

        "location_not_expected": (

            "⚠️ Сейчас геолокация не ожидается.\n\n"

            "Если хотите создать заявку — начните оформление заново."

        ),

        "location_invalid": (

            "⚠️ <b>Не удалось получить корректную геолокацию.</b>\n\n"

            "Нажмите кнопку <b>«📍 Поделиться геолокацией»</b> "

            "и отправьте местоположение ещё раз."

        ),

        "location_received": "✅ Геолокация получена.",

        "location_required": (

            "📍 <b>Нужна геолокация.</b>\n\n"

            "Нажмите кнопку <b>«📍 Поделиться геолокацией»</b> "

            "и отправьте ваше местоположение."

        ),

        "location_text_required": "📍 Пожалуйста, отправьте геолокацию через кнопку ниже.",

        "location_address": "Геолокация клиента",

        "client_location": "Геолокация клиента",

        "location_not_specified": "Не указано",

        "location_received_short": "Геолокация получена",

        "open_map": "🗺 Открыть на карте",

        # ======================================================

        # CALENDAR

        # ======================================================

        "calendar_choose_date": ("📅 <b>Выберите дату приезда</b>\n\n"),

        "calendar_today": ("Сегодня: <b>{date}</b>\n\n"),

        "calendar_past_day": "▫️ — прошедший день\n",

        "calendar_today_legend": "🟢 — сегодня\n\n",

        "calendar_choose_convenient_date": "Выберите удобную дату.",

        "month_1": "Январь",

        "month_2": "Февраль",

        "month_3": "Март",

        "month_4": "Апрель",

        "month_5": "Май",

        "month_6": "Июнь",

        "month_7": "Июль",

        "month_8": "Август",

        "month_9": "Сентябрь",

        "month_10": "Октябрь",

        "month_11": "Ноябрь",

        "month_12": "Декабрь",

        "weekday_mon": "Пн",

        "weekday_tue": "Вт",

        "weekday_wed": "Ср",

        "weekday_thu": "Чт",

        "weekday_fri": "Пт",

        "weekday_sat": "Сб",

        "weekday_sun": "Вс",

        # ======================================================

        # TIME

        # ======================================================

        "time_choose": (

            "🕐 <b>Выберите время приезда</b>\n\n"

            "📅 Дата: <b>{date}</b>\n\n"

            "Доступные интервалы:"

        ),

        "time_unavailable": "⚠️ Нет доступного времени",

        "choose_another_date": "◀️ Выбрать другую дату",

        # ======================================================

        # DATE ERRORS

        # ======================================================

        "date_selection_unavailable": (

            "⚠️ <b>Выбор даты сейчас недоступен.</b>\n\n"

            "Начните оформление заявки заново."

        ),

        "invalid_date": (

            "❌ <b>Некорректная дата.</b>\n\n" "Выберите дату из календаря."

        ),

        "date_already_passed": (

            "⚠️ <b>Эта дата уже прошла.</b>\n\n"

            "Выберите сегодняшнюю или будущую дату."

        ),

        "no_slots_today": (

            "⚠️ <b>На сегодня свободного времени больше нет.</b>\n\n"

            "Выберите другой день."

        ),

        "no_slots_selected_date": (

            "⚠️ <b>На выбранную дату нет доступного времени.</b>\n\n"

            "Выберите другой день."

        ),

        # ======================================================

        # TIME ERRORS

        # ======================================================

        "time_selection_unavailable": (

            "⚠️ <b>Выбор времени сейчас недоступен.</b>\n\n"

            "Начните оформление заявки заново."

        ),

        "invalid_date_or_time": (

            "❌ <b>Некорректные дата или время.</b>\n\n"

            "Пожалуйста, выберите время ещё раз."

        ),

        "time_slot_unavailable": (

            "⚠️ <b>Это время уже недоступно.</b>\n\n"

            "Выберите другой временной интервал."

        ),

        "time_already_passed": (

            "⚠️ <b>Это время уже прошло.</b>\n\n" "Выберите другое время."

        ),

        # ======================================================

        # COMMENT

        # ======================================================

        "comment_prompt": (

            "💬 <b>Комментарий к заявке</b>\n\n"

            "Напишите дополнительную информацию для специалиста.\n\n"

            "Например:\n"

            "«Позвонить за 30 минут до приезда».\n\n"

            "Если комментарий не нужен — нажмите «⏭ Пропустить»."

        ),

        "comment_too_long": (

            "⚠️ <b>Комментарий слишком длинный.</b>\n\n"

            "Сократите его до 5000 символов."

        ),

        # ======================================================

        # ======================================================

        # ONLINE CONSULTATION

        # ======================================================

        "consultation_question_prompt": (

            "💬 <b>Онлайн-консультация</b>\n\n"

            "Опишите вашу проблему или задайте вопрос сантехнику."

        ),

        "consultation_question_required": (

            "⚠️ <b>Вопрос не указан.</b>\n\n"

            "Пожалуйста, опишите вашу проблему или задайте вопрос."

        ),

        "consultation_question_too_long": (

            "⚠️ <b>Вопрос слишком длинный.</b>\n\n"

            "Сократите его до 5000 символов."

        ),

        "consultation_request_created": "✅ <b>Консультация создана</b>",

        "consultation_question_label": "<b>Ваш вопрос</b>",

        "consultation_request_sent": (

            "Ваш вопрос передан специалистам.\n\n"

            "Как только специалист примет консультацию, мы отправим вам его контактные данные."

        ),

        # REQUEST PREVIEW

        # ======================================================

        "request_preview_title": "📋 <b>Проверьте заявку</b>",

        "request_service": "🔧 <b>Услуга:</b>",

        "request_location": "📍 <b>Место выполнения:</b>",

        "request_date": "📅 <b>Дата:</b>",

        "request_time": "🕐 <b>Время:</b>",

        "request_comment": "💬 <b>Комментарий:</b>",

        "request_location_received": "Геолокация получена",

        "request_preliminary_price": ("💰 <b>Предварительная стоимость:</b>\n"),

        "request_price_to_be_confirmed": (

            "💰 <b>Предварительная стоимость:</b>\n" "Стоимость уточняется специалистом"

        ),

        "request_price_warning": ("⚠️ <i>Стоимость является предварительной.</i>"),

        "request_price_inspection": (

            "Точная цена может быть определена после осмотра специалистом."

        ),

        "request_confirm_prompt": ("Если всё верно — подтвердите заявку."),

        "request_invalid_draft": (

            "❌ <b>Не удалось сформировать заявку.</b>\n\n"

            "Необходимо заново выбрать услугу, отправить геолокацию, "

            "дату и время."

        ),

        # ======================================================

        # REQUEST CREATION

        # ======================================================

        "request_confirmation_unavailable": ("⚠️ Сейчас нет заявки для подтверждения."),

        "request_creation_failed": (

            "❌ <b>Не удалось создать заявку.</b>\n\n"

            "{error}\n\n"

            "Начните оформление заново."

        ),

        "request_created": "✅ <b>Заявка успешно создана!</b>",

        "request_number": ("📋 Номер заявки: <b>№{request_id}</b>"),

        "request_location_success": "📍 Геолокация получена",

        "request_preliminary_price_short": ("💰 Предварительно: <b>от {price}</b>"),

        "request_price_specialist_short": (

            "💰 Стоимость: <b>уточняется специалистом</b>"

        ),

        "request_sent_to_specialists": ("Мы передали заявку специалистам."),

        "request_employee_notification": (

            "Как только заявка будет принята, мы сообщим вам."

        ),

        # ======================================================

        # MY REQUESTS

        # ======================================================

        "my_requests_title": "📋 <b>Мои заявки</b>",

        "my_requests_client_not_found": (

            "📋 <b>Мои заявки</b>\n\n" "Клиент не найден."

        ),

        "my_requests_empty": ("📋 <b>Мои заявки</b>\n\n" "У вас пока нет заявок."),

        "request_created_at": "🗓 Создана: {date}",

        "request_scheduled_at": "⏰ Приезд: {datetime}",

        "request_price_list": "💰 от {price}",

        "request_rating": "⭐ Ваша оценка: {stars}",

        "request_not_rated": "⭐ Оценка: ещё не выставлена",

        "request_service_not_specified": "Услуга не указана",

        # ======================================================

        # REQUEST STATUS

        # ======================================================

        "status_new": "Новая",

        "status_in_progress": "В работе",

        "status_completed": "Выполнена",

        "status_cancelled": "Отменена",

        "status_unknown": "Неизвестный статус",

        # ======================================================

        # RATING

        # ======================================================

        "rating_service": "Услуга",

        "rating_completed": ("✅ <b>Заявка выполнена!</b>"),

        "rating_request_number": ("📋 Заявка №<b>{request_id}</b>"),

        "rating_service_label": "🔧 <b>Услуга:</b> ",

        "rating_thanks": ("Спасибо, что воспользовались «Изумруд Сервис»!"),

        "rating_prompt": ("⭐ <b>Оцените работу специалиста:</b>"),

        "rating_help": ("Ваша оценка помогает нам становиться лучше."),

        "rating_success": ("❤️ <b>Спасибо за вашу оценку!</b>"),

        "rating_your_rating": "Ваша оценка:",

        "rating_service_better": ("Спасибо, что помогаете нам делать сервис лучше!"),

        "rating_star": "⭐ {rating}",

        # ======================================================

        # CALLBACK ALERTS

        # ======================================================

        "callback_unknown": "Неизвестная команда.",

        "callback_client_not_found": "Клиент не найден.",

        "callback_calendar_unavailable": "Сейчас календарь недоступен.",

        "callback_bad_date": "Некорректная дата.",

        "callback_bad_time": "Некорректное время.",

        "callback_bad_rating": "Некорректная оценка.",

        "callback_rating_range": "Оценка должна быть от 1 до 5.",

        "callback_request_not_found": "Заявка не найдена.",

        "callback_cannot_rate": "Эту заявку пока нельзя оценить.",

        "callback_already_rated": "Вы уже оценили заявку: {stars}",

        "callback_rating_success": "Спасибо за оценку! ❤️",

        "callback_rating_save_failed": "Не удалось сохранить оценку.",

        "callback_bad_service": "Некорректная услуга.",

        "callback_session_stale": "Сессия заявки устарела.",

        "callback_step_unavailable": "Сейчас этот шаг недоступен.",

        "callback_confirm": "Создаём заявку...",

        "callback_cancel": "Создание заявки отменено.",

        # ======================================================

        # CANCEL / CONFIRM

        # ======================================================

        "request_cancelled": "❌ Оформление заявки отменено.",

        "request_already_ready": (

            "⚠️ <b>Заявка уже готова.</b>\n\n"

            "Проверьте данные выше и нажмите "

            "«✅ Подтвердить заявку»."

        ),

        "confirm_request": "✅ Подтвердить заявку",

        "edit_request": "✏️ Изменить",

        "continue": "➡️ Продолжить",

        "choose_another": "⬅️ Выбрать другую",

        # ======================================================

        # CONTACT

        # ======================================================

        "contact_title": ("📞 <b>Связаться с «Изумруд Сервис»</b>"),

        "contact_description": (

            "Контактные данные компании будут загружаться "

            "из базы данных.\n\n"

            "Этот раздел подключим к модели компании."

        ),

        # ======================================================

        # PRICE FORMATTER

        # ======================================================

        "price_to_be_confirmed_short": "Стоимость уточняется",

        # ======================================================

        # WORKER / SERVICE GROUP

        # ======================================================

        "worker_new_request": "🆕 <b>ЗАЯВКА</b>",

        "worker_request_number": "🆔 Номер:",

        "worker_client": "👤 Клиент:",

        "worker_phone": "📱 Телефон:",

        "worker_client_language": "🌐 Язык клиента:",

        "worker_address": "📍 Адрес:",

        "worker_service": "🔧 Услуга:",

        "worker_comment": "💬 Комментарий:",

        "worker_plumber_answers": "👷 <b>ОТВЕТЫ САНТЕХНИКОВ:</b>",

        "worker_action": "👇 Действие:",

        "worker_request_completed": "🏁 Заявка завершена.",

        "worker_request_closed": "🚫 Заявка закрыта.",

        "worker_status_waiting": "⏳ ожидает ответа",

        "worker_status_going": "🚰 ЕДЕТ",

        "worker_status_cannot": "❌ НЕ МОЖЕТ",

        "worker_status_completed": "✅ ВЫПОЛНИЛ",

        "worker_status_in_progress": "Статус: Заявка в работе.",

        "worker_status_cancelled": "Статус: Заявка отменена.",

        "worker_status_completed_request": "Статус: Заявка выполнена.",

        "worker_status_waiting_plumbers": "Статус: Ожидаем ответа сантехников.",

        "worker_status_all_completed": "Статус: Все сантехники завершили работу.",

        "worker_status_assigned_one": "Статус: Сантехник назначен.",

        "worker_status_assigned_many": "Статус: Сантехники назначены.",

        "worker_no_plumbers": "⚠️ Нет привязанных сантехников.",

        "worker_arrival_unknown": "📅 Приезд: Не указано",

        "worker_arrival": "📅 Приезд: {datetime}",

        "worker_go": "🚰 Я ЕДУ",

        "worker_cannot": "❌ НЕ МОГУ",

        "worker_change_answer": "🔄 Изменить ответ",

        "worker_completed": "✅ ВЫПОЛНЕНО",

        "worker_open_google_maps": "📍 Открыть Google Maps",

        "worker_open_yandex_maps": "🗺 Открыть Яндекс Карты",

        "worker_client_language_not_specified": "Не указан",

        "worker_language_ru": "Русский",

        "worker_language_uz": "Узбекский",

        "worker_language_en": "Английский",

        "worker_language_zh": "Китайский",

        "worker_group_address": "Рабочая группа",

        "worker_without_username": "без username",

        "worker_without_name": "Без имени",

        "no_time_slots_today": "⚠️ На сегодня свободного времени больше нет.\n\nВыберите другой день.",
        "no_time_slots_date": "⚠️ На выбранную дату нет доступного времени.\n\nВыберите другой день.",
    },

    # ==========================================================

    # UZBEK

    # ==========================================================

    "uz": {

        "cancel": "❌ Bekor qilish",

        "skip": "⏭ O‘tkazib yuborish",

        "back_to_menu": "⬅️ Bosh menyu",

        "menu_create": "📝 Buyurtma yaratish",

        "menu_requests": "📋 Mening buyurtmalarim",

        "menu_services": "ℹ️ Xizmatlar",

        "menu_contact": "📞 Bog‘lanish",

        "welcome": (

            "👋 <b>{name}</b>\n\n"

            "«Izumrud Servis» xizmatiga xush kelibsiz.\n\n"

            "Nima qilmoqchisiz?"

        ),

        "client_not_registered": (

            "⚠️ Telegram profilingiz hali ro‘yxatdan o‘tmagan.\n\n"

            "/start buyrug‘ini yuboring."

        ),

        "client_not_found": (

            "⚠️ Mijoz topilmadi.\n\n"

            "Ro‘yxatdan o‘tish uchun /start orqali telefon raqamingizni yuboring."

        ),

        "client_not_found_start": (

            "⚠️ Mijoz topilmadi.\n\n" "/start buyrug‘ini yuboring."

        ),

        "unknown_command": (

            "Buyruqni tushunmadim.\n\n" "Menyudan kerakli amalni tanlang."

        ),

        # SERVICES

        "services_title": "ℹ️ <b>Bizning xizmatlarimiz</b>",

        "services_empty": (

            "ℹ️ <b>Bizning xizmatlarimiz</b>\n\n" "Hozircha xizmatlar ro‘yxati bo‘sh."

        ),

        "services_category_other": "Boshqa xizmatlar",

        "services_price_from_unit": " — {price} dan / {unit}",

        "services_price_from": " — {price} dan",

        "services_price_to_be_confirmed": " — narx aniqlanadi",

        "price_from": " — {price} dan / {unit}",

        "price_from_without_unit": " — {price} dan",

        "price_to_be_confirmed": " — narx aniqlanadi",

        # CREATE REQUEST

        "create_request_title": (

            "📝 <b>Buyurtma yaratish</b>\n\n" "Kerakli xizmatni tanlang:"

        ),

        "create_request_unavailable": (

            "❌ <b>Buyurtma yaratish imkonsiz.</b>\n\n"

            "Xizmatlar ro‘yxati hozircha bo‘sh."

        ),

        "service_unavailable": (

            "❌ <b>Xizmat mavjud emas.</b>\n\n" "Iltimos, xizmatni qaytadan tanlang."

        ),

        "selected_service": (

            "🔧 <b>Siz tanladingiz:</b>\n\n"

            "{name}\n\n"

            "{price_text}\n\n"

            "⚠️ Bu dastlabki narx.\n"

            "Yakuniy narx ish hajmi va murakkabligiga bog‘liq bo‘lishi mumkin."

        ),

        "selected_service_price": ("💰 <b>Dastlabki narx:</b>\n" "{price} dan"),

        "selected_service_price_unknown": (

            "💰 <b>Narx:</b>\n" "mutaxassis tomonidan aniqlanadi"

        ),

        "estimated_price": ("💰 <b>Dastlabki narx:</b>\n" "{price} dan"),

        "estimated_price_with_unit": (

            "💰 <b>Dastlabki narx:</b>\n" "{price} dan {unit} uchun"

        ),

        "price_specialist": ("💰 <b>Narx:</b>\n" "mutaxassis tomonidan aniqlanadi"),

        # LOCATION

        "share_location": "📍 Geolokatsiyani ulashish",

        "location_prompt": (

            "📍 <b>Ish bajariladigan joy</b>\n\n"

            "Quyidagi <b>«📍 Geolokatsiyani ulashish»</b> tugmasini bosing.\n\n"

            "Telegram joylashuvingizni avtomatik ravishda botga yuboradi.\n\n"

            "📍 Geolokatsiya santexnik manzilni aniq topishi uchun kerak."

        ),

        "location_not_expected": (

            "⚠️ Hozir geolokatsiya kutilmayapti.\n\n"

            "Buyurtma yaratmoqchi bo‘lsangiz, jarayonni qaytadan boshlang."

        ),

        "location_invalid": (

            "⚠️ <b>To‘g‘ri geolokatsiyani olishning iloji bo‘lmadi.</b>\n\n"

            "«📍 Geolokatsiyani ulashish» tugmasini bosib, "

            "joylashuvingizni yana yuboring."

        ),

        "location_received": "✅ Geolokatsiya olindi.",

        "location_required": (

            "📍 <b>Geolokatsiya kerak.</b>\n\n"

            "«📍 Geolokatsiyani ulashish» tugmasini bosib, "

            "joylashuvingizni yuboring."

        ),

        "location_text_required": "📍 Iltimos, quyidagi tugma orqali geolokatsiyangizni yuboring.",

        "location_address": "Mijoz geolokatsiyasi",

        "client_location": "Mijoz geolokatsiyasi",

        "location_not_specified": "Ko‘rsatilmagan",

        "location_received_short": "Geolokatsiya olindi",

        "open_map": "🗺 Xaritada ochish",

        # CALENDAR

        "calendar_choose_date": "📅 <b>Kelish sanasini tanlang</b>\n\n",

        "calendar_today": "Bugun: <b>{date}</b>\n\n",

        "calendar_past_day": "▫️ — o‘tgan kun\n",

        "calendar_today_legend": "🟢 — bugun\n\n",

        "calendar_choose_convenient_date": "Qulay sanani tanlang.",

        "month_1": "Yanvar",

        "month_2": "Fevral",

        "month_3": "Mart",

        "month_4": "Aprel",

        "month_5": "May",

        "month_6": "Iyun",

        "month_7": "Iyul",

        "month_8": "Avgust",

        "month_9": "Sentabr",

        "month_10": "Oktabr",

        "month_11": "Noyabr",

        "month_12": "Dekabr",

        "weekday_mon": "Du",

        "weekday_tue": "Se",

        "weekday_wed": "Ch",

        "weekday_thu": "Pa",

        "weekday_fri": "Ju",

        "weekday_sat": "Sh",

        "weekday_sun": "Ya",

        # TIME

        "time_choose": (

            "🕐 <b>Kelish vaqtini tanlang</b>\n\n"

            "📅 Sana: <b>{date}</b>\n\n"

            "Mavjud vaqtlar:"

        ),

        "time_unavailable": "⚠️ Mavjud vaqt yo‘q",

        "choose_another_date": "◀️ Boshqa sanani tanlash",

        # ERRORS

        "date_selection_unavailable": (

            "⚠️ <b>Hozir sana tanlash imkonsiz.</b>\n\n"

            "Buyurtma yaratishni qaytadan boshlang."

        ),

        "invalid_date": ("❌ <b>Noto‘g‘ri sana.</b>\n\n" "Sanani kalendardan tanlang."),

        "date_already_passed": (

            "⚠️ <b>Bu sana o‘tib ketgan.</b>\n\n"

            "Bugungi yoki kelajakdagi sanani tanlang."

        ),

        "no_slots_today": (

            "⚠️ <b>Bugun bo‘sh vaqt qolmagan.</b>\n\n" "Boshqa kunni tanlang."

        ),

        "no_slots_selected_date": (

            "⚠️ <b>Tanlangan sanada bo‘sh vaqt yo‘q.</b>\n\n" "Boshqa kunni tanlang."

        ),

        "time_selection_unavailable": (

            "⚠️ <b>Hozir vaqt tanlash imkonsiz.</b>\n\n"

            "Buyurtma yaratishni qaytadan boshlang."

        ),

        "invalid_date_or_time": (

            "❌ <b>Sana yoki vaqt noto‘g‘ri.</b>\n\n" "Vaqtni qaytadan tanlang."

        ),

        "time_slot_unavailable": (

            "⚠️ <b>Bu vaqt allaqachon band.</b>\n\n" "Boshqa vaqt oralig‘ini tanlang."

        ),

        "time_already_passed": (

            "⚠️ <b>Bu vaqt o‘tib ketgan.</b>\n\n" "Boshqa vaqtni tanlang."

        ),

        # COMMENT

        "comment_prompt": (

            "💬 <b>Buyurtma uchun izoh</b>\n\n"

            "Mutaxassis uchun qo‘shimcha ma’lumot yozing.\n\n"

            "Masalan:\n"

            "«Kelishdan 30 daqiqa oldin qo‘ng‘iroq qiling».\n\n"

            "Izoh kerak bo‘lmasa — «⏭ O‘tkazib yuborish» tugmasini bosing."

        ),

        "comment_too_long": (

            "⚠️ <b>Izoh juda uzun.</b>\n\n" "Uni 5000 belgigacha qisqartiring."

        ),

        # ======================================================

        # ONLINE CONSULTATION

        # ======================================================

        "consultation_question_prompt": (

            "💬 <b>Onlayn maslahat</b>\n\n"

            "Muammoingizni tasvirlab bering yoki santexnikka savolingizni yozing."

        ),

        "consultation_question_required": (

            "⚠️ <b>Savol ko‘rsatilmagan.</b>\n\n"

            "Iltimos, muammoingizni tasvirlab bering yoki savolingizni yozing."

        ),

        "consultation_question_too_long": (

            "⚠️ <b>Savol juda uzun.</b>\n\n"

            "Uni 5000 belgigacha qisqartiring."

        ),

        "consultation_request_created": "✅ <b>Onlayn maslahat so‘rovi yaratildi</b>",

        "consultation_question_label": "<b>Sizning savolingiz</b>",

        "consultation_request_sent": (

            "Savolingiz mutaxassislarga yuborildi.\n\n"

            "Mutaxassis maslahatni qabul qilgach, uning aloqa ma’lumotlarini sizga yuboramiz."

        ),

        # PREVIEW

        "request_preview_title": "📋 <b>Buyurtmani tekshiring</b>",

        "request_service": "🔧 <b>Xizmat:</b>",

        "request_location": "📍 <b>Bajariladigan joy:</b>",

        "request_date": "📅 <b>Sana:</b>",

        "request_time": "🕐 <b>Vaqt:</b>",

        "request_comment": "💬 <b>Izoh:</b>",

        "request_location_received": "Geolokatsiya olindi",

        "request_preliminary_price": ("💰 <b>Dastlabki narx:</b>\n"),

        "request_price_to_be_confirmed": (

            "💰 <b>Dastlabki narx:</b>\n" "Narx mutaxassis tomonidan aniqlanadi"

        ),

        "request_price_warning": ("⚠️ <i>Narx dastlabki hisoblanadi.</i>"),

        "request_price_inspection": (

            "Aniq narx mutaxassis ko‘rigidan so‘ng belgilanadi."

        ),

        "request_confirm_prompt": ("Hammasi to‘g‘ri bo‘lsa — buyurtmani tasdiqlang."),

        "request_invalid_draft": (

            "❌ <b>Buyurtmani shakllantirib bo‘lmadi.</b>\n\n"

            "Xizmatni, geolokatsiyani, sana va vaqtni qaytadan tanlang."

        ),

        # CREATION

        "request_confirmation_unavailable": (

            "⚠️ Hozir tasdiqlash uchun buyurtma mavjud emas."

        ),

        "request_creation_failed": (

            "❌ <b>Buyurtmani yaratib bo‘lmadi.</b>\n\n"

            "{error}\n\n"

            "Jarayonni qaytadan boshlang."

        ),

        "request_created": ("✅ <b>Buyurtma muvaffaqiyatli yaratildi!</b>"),

        "request_number": ("📋 Buyurtma raqami: <b>№{request_id}</b>"),

        "request_location_success": "📍 Geolokatsiya olindi",

        "request_preliminary_price_short": ("💰 Dastlabki narx: <b>{price} dan</b>"),

        "request_price_specialist_short": (

            "💰 Narx: <b>mutaxassis tomonidan aniqlanadi</b>"

        ),

        "request_sent_to_specialists": ("Buyurtmangiz mutaxassislarga yuborildi."),

        "request_employee_notification": (

            "Buyurtma qabul qilinganda sizga xabar beramiz."

        ),

        # REQUESTS

        "my_requests_title": "📋 <b>Mening buyurtmalarim</b>",

        "my_requests_client_not_found": (

            "📋 <b>Mening buyurtmalarim</b>\n\n" "Mijoz topilmadi."

        ),

        "my_requests_empty": (

            "📋 <b>Mening buyurtmalarim</b>\n\n" "Sizda hali buyurtmalar yo‘q."

        ),

        "request_created_at": "🗓 Yaratilgan: {date}",

        "request_scheduled_at": "⏰ Kelish: {datetime}",

        "request_price_list": "💰 {price} dan",

        "request_rating": "⭐ Sizning bahoyingiz: {stars}",

        "request_not_rated": "⭐ Baho: hali qo‘yilmagan",

        "request_service_not_specified": "Xizmat ko‘rsatilmagan",

        # STATUS

        "status_new": "Yangi",

        "status_in_progress": "Jarayonda",

        "status_completed": "Bajarildi",

        "status_cancelled": "Bekor qilindi",

        "status_unknown": "Noma’lum holat",

        # RATING

        "rating_service": "Xizmat",

        "rating_completed": "✅ <b>Buyurtma bajarildi!</b>",

        "rating_request_number": "📋 Buyurtma №<b>{request_id}</b>",

        "rating_service_label": "🔧 <b>Xizmat:</b> ",

        "rating_thanks": "«Izumrud Servis» xizmatidan foydalanganingiz uchun rahmat!",

        "rating_prompt": "⭐ <b>Mutaxassis ishini baholang:</b>",

        "rating_help": "Sizning bahoyingiz bizga yanada yaxshiroq xizmat ko‘rsatishga yordam beradi.",

        "rating_success": "❤️ <b>Bahoyingiz uchun rahmat!</b>",

        "rating_your_rating": "Sizning bahoyingiz:",

        "rating_service_better": "Xizmatimizni yaxshilashga yordam berganingiz uchun rahmat!",

        "rating_star": "⭐ {rating}",

        # CALLBACKS

        "callback_unknown": "Noma’lum buyruq.",

        "callback_client_not_found": "Mijoz topilmadi.",

        "callback_calendar_unavailable": "Hozir kalendar mavjud emas.",

        "callback_bad_date": "Noto‘g‘ri sana.",

        "callback_bad_time": "Noto‘g‘ri vaqt.",

        "callback_bad_rating": "Noto‘g‘ri baho.",

        "callback_rating_range": "Baho 1 dan 5 gacha bo‘lishi kerak.",

        "callback_request_not_found": "Buyurtma topilmadi.",

        "callback_cannot_rate": "Bu buyurtmani hozircha baholab bo‘lmaydi.",

        "callback_already_rated": "Siz bu buyurtmani allaqachon baholagansiz: {stars}",

        "callback_rating_success": "Bahoyingiz uchun rahmat! ❤️",

        "callback_rating_save_failed": "Bahoni saqlab bo‘lmadi.",

        "callback_bad_service": "Noto‘g‘ri xizmat.",

        "callback_session_stale": "Buyurtma sessiyasi eskirgan.",

        "callback_step_unavailable": "Hozir bu bosqich mavjud emas.",

        "callback_confirm": "Buyurtma yaratilmoqda...",

        "callback_cancel": "Buyurtma yaratish bekor qilindi.",

        # CONFIRM / CANCEL

        "request_cancelled": "❌ Buyurtma yaratish bekor qilindi.",

        "request_already_ready": (

            "⚠️ <b>Buyurtma allaqachon tayyor.</b>\n\n"

            "Ma’lumotlarni tekshiring va "

            "«✅ Buyurtmani tasdiqlash» tugmasini bosing."

        ),

        "confirm_request": "✅ Buyurtmani tasdiqlash",

        "edit_request": "✏️ O‘zgartirish",

        "continue": "➡️ Davom etish",

        "choose_another": "⬅️ Boshqasini tanlash",

        # CONTACT

        "contact_title": "📞 <b>«Izumrud Servis» bilan bog‘lanish</b>",

        "contact_description": (

            "Kompaniyaning aloqa ma’lumotlari ma’lumotlar bazasidan yuklanadi.\n\n"

            "Bu bo‘lim kompaniya modeli bilan ulanadi."

        ),

        "coordinates_not_specified": "Ko‘rsatilmagan",

        "price_to_be_confirmed_short": "Narx aniqlanadi",

        # ======================================================

        # ISHCHI / ISHCHI GURUHI

        # ======================================================

        "worker_new_request": "🆕 <b>BUYURTMA</b>",

        "worker_request_number": "🆔 Raqam:",

        "worker_client": "👤 Mijoz:",

        "worker_phone": "📱 Telefon:",

        "worker_client_language": "🌐 Mijoz tili:",

        "worker_address": "📍 Manzil:",

        "worker_service": "🔧 Xizmat:",

        "worker_comment": "💬 Izoh:",

        "worker_plumber_answers": "👷 <b>SANTEXNIKLAR JAVOBLARI:</b>",

        "worker_action": "👇 Amal:",

        "worker_request_completed": "🏁 Buyurtma bajarildi.",

        "worker_request_closed": "🚫 Buyurtma yopildi.",

        "worker_status_waiting": "⏳ javob kutilmoqda",

        "worker_status_going": "🚰 BORYAPMAN",

        "worker_status_cannot": "❌ BORA OLMAYMAN",

        "worker_status_completed": "✅ BAJARDIM",

        "worker_status_in_progress": "Holat: Buyurtma bajarilmoqda.",

        "worker_status_cancelled": "Holat: Buyurtma bekor qilindi.",

        "worker_status_completed_request": "Holat: Buyurtma bajarildi.",

        "worker_status_waiting_plumbers": "Holat: Santexniklarning javobi kutilmoqda.",

        "worker_status_all_completed": "Holat: Barcha santexniklar ishni yakunladi.",

        "worker_status_assigned_one": "Holat: Santexnik tayinlandi.",

        "worker_status_assigned_many": "Holat: Santexniklar tayinlandi.",

        "worker_no_plumbers": "⚠️ Biriktirilgan santexniklar yo‘q.",

        "worker_arrival_unknown": "📅 Kelish: Ko‘rsatilmagan",

        "worker_arrival": "📅 Kelish: {datetime}",

        "worker_go": "🚰 BORYAPMAN",

        "worker_cannot": "❌ BORA OLMAYMAN",

        "worker_change_answer": "🔄 Javobni o‘zgartirish",

        "worker_completed": "✅ BAJARILDI",

        "worker_open_google_maps": "📍 Google Maps'ni ochish",

        "worker_open_yandex_maps": "🗺 Yandex Xaritalarni ochish",

        "worker_client_language_not_specified": "Ko‘rsatilmagan",

        "worker_language_ru": "Rus tili",

        "worker_language_uz": "O‘zbek tili",

        "worker_language_en": "Ingliz tili",

        "worker_language_zh": "Xitoy tili",

        "worker_group_address": "Ishchi guruhi",

        "worker_without_username": "username yo‘q",

        "worker_without_name": "Ism ko‘rsatilmagan",

        "no_time_slots_today": "⚠️ Bugun bo‘sh vaqtlar mavjud emas.\n\nIltimos, boshqa kunni tanlang.",
        "no_time_slots_date": "⚠️ Tanlangan sana uchun bo‘sh vaqtlar mavjud emas.\n\nIltimos, boshqa kunni tanlang.",
    },

    # ==========================================================

    # ENGLISH

    # ==========================================================

    "en": {

        "cancel": "❌ Cancel",

        "skip": "⏭ Skip",

        "back_to_menu": "⬅️ Main menu",

        "menu_create": "📝 Create request",

        "menu_requests": "📋 My requests",

        "menu_services": "ℹ️ Services",

        "menu_contact": "📞 Contact us",

        "welcome": (

            "👋 <b>{name}</b>\n\n"

            "Welcome to Emerald Service.\n\n"

            "What would you like to do?"

        ),

        "client_not_registered": (

            "⚠️ Your Telegram is not registered yet.\n\n" "Send the /start command."

        ),

        "client_not_found": (

            "⚠️ Client not found.\n\n"

            "To register, send your phone number through /start."

        ),

        "client_not_found_start": ("⚠️ Client not found.\n\n" "Send /start."),

        "unknown_command": (

            "I didn't quite understand the command.\n\n"

            "Please choose an action from the menu."

        ),

        # SERVICES

        "services_title": "ℹ️ <b>Our services</b>",

        "services_empty": (

            "ℹ️ <b>Our services</b>\n\n" "The service list is currently empty."

        ),

        "services_category_other": "Other services",

        "services_price_from_unit": " — from {price} per {unit}",

        "services_price_from": " — from {price}",

        "services_price_to_be_confirmed": " — price to be confirmed",

        "price_from": " — from {price} per {unit}",

        "price_from_without_unit": " — from {price}",

        "price_to_be_confirmed": " — price to be confirmed",

        # CREATE REQUEST

        "create_request_title": (

            "📝 <b>Create a request</b>\n\n" "Choose the service you need:"

        ),

        "create_request_unavailable": (

            "❌ <b>Request creation is unavailable.</b>\n\n"

            "The service list is currently empty."

        ),

        "service_unavailable": (

            "❌ <b>Service unavailable.</b>\n\n" "Please select the service again."

        ),

        "selected_service": (

            "🔧 <b>You selected:</b>\n\n"

            "{name}\n\n"

            "{price_text}\n\n"

            "⚠️ This is a preliminary price.\n"

            "The final price may depend on the scope and complexity of the work."

        ),

        "selected_service_price": ("💰 <b>Preliminary price:</b>\n" "from {price}"),

        "selected_service_price_unknown": (

            "💰 <b>Price:</b>\n" "to be confirmed by a specialist"

        ),

        "estimated_price": ("💰 <b>Preliminary price:</b>\n" "from {price}"),

        "estimated_price_with_unit": (

            "💰 <b>Preliminary price:</b>\n" "from {price} per {unit}"

        ),

        "price_specialist": ("💰 <b>Price:</b>\n" "to be confirmed by a specialist"),

        # LOCATION

        "share_location": "📍 Share location",

        "location_prompt": (

            "📍 <b>Work location</b>\n\n"

            "Press <b>«📍 Share location»</b> below.\n\n"

            "Telegram will automatically send your location to the bot.\n\n"

            "📍 Your location is needed so the plumber can accurately find the place."

        ),

        "location_not_expected": (

            "⚠️ Location is not expected at this stage.\n\n"

            "If you want to create a request, start the process again."

        ),

        "location_invalid": (

            "⚠️ <b>Could not get a valid location.</b>\n\n"

            "Press <b>«📍 Share location»</b> and send your location again."

        ),

        "location_received": "✅ Location received.",

        "location_required": (

            "📍 <b>Location required.</b>\n\n"

            "Press <b>«📍 Share location»</b> and send your location."

        ),

        "location_text_required": "📍 Please send your location using the button below.",

        "location_address": "Client location",

        "client_location": "Client location",

        "location_not_specified": "Not specified",

        "location_received_short": "Location received",

        "open_map": "🗺 Open on map",

        # CALENDAR

        "calendar_choose_date": "📅 <b>Choose arrival date</b>\n\n",

        "calendar_today": "Today: <b>{date}</b>\n\n",

        "calendar_past_day": "▫️ — past day\n",

        "calendar_today_legend": "🟢 — today\n\n",

        "calendar_choose_convenient_date": "Choose a convenient date.",

        "month_1": "January",

        "month_2": "February",

        "month_3": "March",

        "month_4": "April",

        "month_5": "May",

        "month_6": "June",

        "month_7": "July",

        "month_8": "August",

        "month_9": "September",

        "month_10": "October",

        "month_11": "November",

        "month_12": "December",

        "weekday_mon": "Mon",

        "weekday_tue": "Tue",

        "weekday_wed": "Wed",

        "weekday_thu": "Thu",

        "weekday_fri": "Fri",

        "weekday_sat": "Sat",

        "weekday_sun": "Sun",

        # TIME

        "time_choose": (

            "🕐 <b>Choose arrival time</b>\n\n"

            "📅 Date: <b>{date}</b>\n\n"

            "Available time slots:"

        ),

        "time_unavailable": "⚠️ No available time",

        "choose_another_date": "◀️ Choose another date",

        # ERRORS

        "date_selection_unavailable": (

            "⚠️ <b>Date selection is currently unavailable.</b>\n\n"

            "Start the request process again."

        ),

        "invalid_date": (

            "❌ <b>Invalid date.</b>\n\n" "Choose a date from the calendar."

        ),

        "date_already_passed": (

            "⚠️ <b>This date has already passed.</b>\n\n"

            "Choose today or a future date."

        ),

        "no_slots_today": (

            "⚠️ <b>No available time is left for today.</b>\n\n" "Choose another day."

        ),

        "no_slots_selected_date": (

            "⚠️ <b>No available time for the selected date.</b>\n\n"

            "Choose another day."

        ),

        "time_selection_unavailable": (

            "⚠️ <b>Time selection is currently unavailable.</b>\n\n"

            "Start the request process again."

        ),

        "invalid_date_or_time": (

            "❌ <b>Invalid date or time.</b>\n\n" "Please choose the time again."

        ),

        "time_slot_unavailable": (

            "⚠️ <b>This time is no longer available.</b>\n\n"

            "Choose another time slot."

        ),

        "time_already_passed": (

            "⚠️ <b>This time has already passed.</b>\n\n" "Choose another time."

        ),

        # COMMENT

        "comment_prompt": (

            "💬 <b>Request comment</b>\n\n"

            "Write additional information for the specialist.\n\n"

            "For example:\n"

            "«Call me 30 minutes before arrival».\n\n"

            "If you don't need a comment, press «⏭ Skip»."

        ),

        "comment_too_long": (

            "⚠️ <b>Comment is too long.</b>\n\n" "Shorten it to 5000 characters."

        ),

        # ======================================================

        # ONLINE CONSULTATION

        # ======================================================

        "consultation_question_prompt": (

            "💬 <b>Online consultation</b>\n\n"

            "Describe your problem or ask the plumber a question."

        ),

        "consultation_question_required": (

            "⚠️ <b>No question provided.</b>\n\n"

            "Please describe your problem or ask your question."

        ),

        "consultation_question_too_long": (

            "⚠️ <b>Your question is too long.</b>\n\n"

            "Shorten it to 5000 characters."

        ),

        "consultation_request_created": "✅ <b>Consultation request created</b>",

        "consultation_question_label": "<b>Your question</b>",

        "consultation_request_sent": (

            "Your question has been sent to our specialists.\n\n"

            "Once a specialist accepts the consultation, we will send you their contact details."

        ),

        # PREVIEW

        "request_preview_title": "📋 <b>Check your request</b>",

        "request_service": "🔧 <b>Service:</b>",

        "request_location": "📍 <b>Work location:</b>",

        "request_date": "📅 <b>Date:</b>",

        "request_time": "🕐 <b>Time:</b>",

        "request_comment": "💬 <b>Comment:</b>",

        "request_location_received": "Location received",

        "request_preliminary_price": ("💰 <b>Preliminary price:</b>\n"),

        "request_price_to_be_confirmed": (

            "💰 <b>Preliminary price:</b>\n" "Price will be confirmed by a specialist"

        ),

        "request_price_warning": ("⚠️ <i>The price is preliminary.</i>"),

        "request_price_inspection": (

            "The exact price can be determined after the specialist's inspection."

        ),

        "request_confirm_prompt": ("If everything is correct, confirm the request."),

        "request_invalid_draft": (

            "❌ <b>Could not build the request.</b>\n\n"

            "You need to select the service, send your location, "

            "date and time again."

        ),

        # CREATION

        "request_confirmation_unavailable": (

            "⚠️ There is currently no request to confirm."

        ),

        "request_creation_failed": (

            "❌ <b>Could not create the request.</b>\n\n"

            "{error}\n\n"

            "Start the process again."

        ),

        "request_created": ("✅ <b>Request created successfully!</b>"),

        "request_number": ("📋 Request number: <b>№{request_id}</b>"),

        "request_location_success": "📍 Location received",

        "request_preliminary_price_short": ("💰 Preliminary: <b>from {price}</b>"),

        "request_price_specialist_short": (

            "💰 Price: <b>to be confirmed by a specialist</b>"

        ),

        "request_sent_to_specialists": (

            "We have sent your request to our specialists."

        ),

        "request_employee_notification": (

            "We will notify you as soon as the request is accepted."

        ),

        # REQUESTS

        "my_requests_title": "📋 <b>My requests</b>",

        "my_requests_client_not_found": (

            "📋 <b>My requests</b>\n\n" "Client not found."

        ),

        "my_requests_empty": (

            "📋 <b>My requests</b>\n\n" "You don't have any requests yet."

        ),

        "request_created_at": "🗓 Created: {date}",

        "request_scheduled_at": "⏰ Arrival: {datetime}",

        "request_price_list": "💰 from {price}",

        "request_rating": "⭐ Your rating: {stars}",

        "request_not_rated": "⭐ Rating: not yet provided",

        "request_service_not_specified": "Service not specified",

        # STATUS

        "status_new": "New",

        "status_in_progress": "In progress",

        "status_completed": "Completed",

        "status_cancelled": "Cancelled",

        "status_unknown": "Unknown status",

        # RATING

        "rating_service": "Service",

        "rating_completed": "✅ <b>Request completed!</b>",

        "rating_request_number": "📋 Request №<b>{request_id}</b>",

        "rating_service_label": "🔧 <b>Service:</b> ",

        "rating_thanks": "Thank you for using Emerald Service!",

        "rating_prompt": "⭐ <b>Please rate the specialist's work:</b>",

        "rating_help": "Your rating helps us improve.",

        "rating_success": "❤️ <b>Thank you for your rating!</b>",

        "rating_your_rating": "Your rating:",

        "rating_service_better": "Thank you for helping us make our service better!",

        "rating_star": "⭐ {rating}",

        # CALLBACKS

        "callback_unknown": "Unknown command.",

        "callback_client_not_found": "Client not found.",

        "callback_calendar_unavailable": "Calendar is currently unavailable.",

        "callback_bad_date": "Invalid date.",

        "callback_bad_time": "Invalid time.",

        "callback_bad_rating": "Invalid rating.",

        "callback_rating_range": "Rating must be between 1 and 5.",

        "callback_request_not_found": "Request not found.",

        "callback_cannot_rate": "This request cannot be rated yet.",

        "callback_already_rated": "You have already rated this request: {stars}",

        "callback_rating_success": "Thank you for your rating! ❤️",

        "callback_rating_save_failed": "Could not save the rating.",

        "callback_bad_service": "Invalid service.",

        "callback_session_stale": "The request session has expired.",

        "callback_step_unavailable": "This step is currently unavailable.",

        "callback_confirm": "Creating request...",

        "callback_cancel": "Request creation cancelled.",

        # CONFIRM / CANCEL

        "request_cancelled": "❌ Request creation cancelled.",

        "request_already_ready": (

            "⚠️ <b>The request is already ready.</b>\n\n"

            "Check the information above and press "

            "«✅ Confirm request»."

        ),

        "confirm_request": "✅ Confirm request",

        "edit_request": "✏️ Edit",

        "continue": "➡️ Continue",

        "choose_another": "⬅️ Choose another",

        # CONTACT

        "contact_title": "📞 <b>Contact Emerald Service</b>",

        "contact_description": (

            "Company contact details will be loaded from the database.\n\n"

            "This section will be connected to the company model."

        ),

        "coordinates_not_specified": "Not specified",

        "price_to_be_confirmed_short": "Price to be confirmed",

        "no_time_slots_today": "⚠️ There is no available time today.\n\nPlease choose another day.",
        "no_time_slots_date": "⚠️ There is no available time on the selected date.\n\nPlease choose another day.",
    },

    # ==========================================================

    # CHINESE

    # ==========================================================

    "zh": {

        "cancel": "❌ 取消",

        "skip": "⏭ 跳过",

        "back_to_menu": "⬅️ 主菜单",

        "menu_create": "📝 创建订单",

        "menu_requests": "📋 我的订单",

        "menu_services": "ℹ️ 服务",

        "menu_contact": "📞 联系我们",

        "welcome": ("👋 <b>{name}</b>\n\n" "欢迎使用“翡翠服务”。\n\n" "您想做什么？"),

        "client_not_registered": (

            "⚠️ 您的 Telegram 账号尚未注册。\n\n" "请发送 /start 命令。"

        ),

        "client_not_found": (

            "⚠️ 未找到客户。\n\n" "如需注册，请通过 /start 发送您的电话号码。"

        ),

        "client_not_found_start": ("⚠️ 未找到客户。\n\n" "请发送 /start。"),

        "unknown_command": ("我没有理解您的命令。\n\n" "请从菜单中选择操作。"),

        # SERVICES

        "services_title": "ℹ️ <b>我们的服务</b>",

        "services_empty": ("ℹ️ <b>我们的服务</b>\n\n" "目前服务列表为空。"),

        "services_category_other": "其他服务",

        "services_price_from_unit": " — 起价 {price} / {unit}",

        "services_price_from": " — 起价 {price}",

        "services_price_to_be_confirmed": " — 价格待确认",

        "price_from": " — 起价 {price} / {unit}",

        "price_from_without_unit": " — 起价 {price}",

        "price_to_be_confirmed": " — 价格待确认",

        # CREATE REQUEST

        "create_request_title": ("📝 <b>创建订单</b>\n\n" "请选择您需要的服务："),

        "create_request_unavailable": (

            "❌ <b>暂时无法创建订单。</b>\n\n" "目前服务列表为空。"

        ),

        "service_unavailable": ("❌ <b>服务不可用。</b>\n\n" "请重新选择服务。"),

        "selected_service": (

            "🔧 <b>您选择了：</b>\n\n"

            "{name}\n\n"

            "{price_text}\n\n"

            "⚠️ 这是预估价格。\n"

            "最终价格可能取决于工作量和工作难度。"

        ),

        "selected_service_price": ("💰 <b>预估价格：</b>\n" "起价 {price}"),

        "selected_service_price_unknown": ("💰 <b>价格：</b>\n" "由专业人员确认"),

        "estimated_price": ("💰 <b>预估价格：</b>\n" "起价 {price}"),

        "estimated_price_with_unit": ("💰 <b>预估价格：</b>\n" "起价 {price} / {unit}"),

        "price_specialist": ("💰 <b>价格：</b>\n" "由专业人员确认"),

        # LOCATION

        "share_location": "📍 分享位置",

        "location_prompt": (

            "📍 <b>工作地点</b>\n\n"

            "请点击下面的 <b>«📍 分享位置»</b> 按钮。\n\n"

            "Telegram 会自动将您的位置发送给机器人。\n\n"

            "📍 您的位置可以帮助水管工准确找到工作地点。"

        ),

        "location_not_expected": (

            "⚠️ 当前不需要发送位置。\n\n" "如果您想创建订单，请重新开始。"

        ),

        "location_invalid": (

            "⚠️ <b>无法获取有效的位置。</b>\n\n"

            "请点击 <b>«📍 分享位置»</b>，然后再次发送您的位置。"

        ),

        "location_received": "✅ 已收到位置。",

        "location_required": (

            "📍 <b>需要位置信息。</b>\n\n"

            "请点击 <b>«📍 分享位置»</b> 并发送您的位置。"

        ),

        "location_text_required": "📍 请使用下面的按钮发送您的位置。",

        "location_address": "客户位置",

        "client_location": "客户位置",

        "location_not_specified": "未指定",

        "location_received_short": "已收到位置",

        "open_map": "🗺 在地图上打开",

        # CALENDAR

        "calendar_choose_date": "📅 <b>请选择到访日期</b>\n\n",

        "calendar_today": "今天：<b>{date}</b>\n\n",

        "calendar_past_day": "▫️ — 已过去的日期\n",

        "calendar_today_legend": "🟢 — 今天\n\n",

        "calendar_choose_convenient_date": "请选择方便的日期。",

        "month_1": "一月",

        "month_2": "二月",

        "month_3": "三月",

        "month_4": "四月",

        "month_5": "五月",

        "month_6": "六月",

        "month_7": "七月",

        "month_8": "八月",

        "month_9": "九月",

        "month_10": "十月",

        "month_11": "十一月",

        "month_12": "十二月",

        "weekday_mon": "一",

        "weekday_tue": "二",

        "weekday_wed": "三",

        "weekday_thu": "四",

        "weekday_fri": "五",

        "weekday_sat": "六",

        "weekday_sun": "日",

        # TIME

        "time_choose": (

            "🕐 <b>请选择到访时间</b>\n\n" "📅 日期：<b>{date}</b>\n\n" "可用时间段："

        ),

        "time_unavailable": "⚠️ 没有可用时间",

        "choose_another_date": "◀️ 选择其他日期",

        # ERRORS

        "date_selection_unavailable": (

            "⚠️ <b>当前无法选择日期。</b>\n\n" "请重新开始创建订单。"

        ),

        "invalid_date": ("❌ <b>日期无效。</b>\n\n" "请从日历中选择日期。"),

        "date_already_passed": (

            "⚠️ <b>该日期已经过去。</b>\n\n" "请选择今天或未来的日期。"

        ),

        "no_slots_today": ("⚠️ <b>今天已经没有可用时间。</b>\n\n" "请选择其他日期。"),

        "no_slots_selected_date": (

            "⚠️ <b>所选日期没有可用时间。</b>\n\n" "请选择其他日期。"

        ),

        "time_selection_unavailable": (

            "⚠️ <b>当前无法选择时间。</b>\n\n" "请重新开始创建订单。"

        ),

        "invalid_date_or_time": ("❌ <b>日期或时间无效。</b>\n\n" "请重新选择时间。"),

        "time_slot_unavailable": (

            "⚠️ <b>该时间已经不可用。</b>\n\n" "请选择其他时间段。"

        ),

        "time_already_passed": ("⚠️ <b>该时间已经过去。</b>\n\n" "请选择其他时间。"),

        # COMMENT

        "comment_prompt": (

            "💬 <b>订单备注</b>\n\n"

            "请输入给专业人员的其他信息。\n\n"

            "例如：\n"

            "“请在到达前30分钟打电话。”\n\n"

            "如果不需要备注，请点击“⏭ 跳过”。"

        ),

        "comment_too_long": ("⚠️ <b>备注太长。</b>\n\n" "请将其缩短至5000个字符以内。"),

        # ======================================================

        # ONLINE CONSULTATION

        # ======================================================

        "consultation_question_prompt": (

            "💬 <b>在线咨询</b>\n\n"

            "请描述您的问题或向水管工提问。"

        ),

        "consultation_question_required": (

            "⚠️ <b>未提供问题。</b>\n\n"

            "请描述您的问题或提出您的疑问。"

        ),

        "consultation_question_too_long": (

            "⚠️ <b>您的问题太长。</b>\n\n"

            "请将其缩短至5000个字符以内。"

        ),

        "consultation_request_created": "✅ <b>在线咨询请求已创建</b>",

        "consultation_question_label": "<b>您的问题</b>",

        "consultation_request_sent": (

            "您的问题已发送给专业人员。\n\n"

            "专业人员接受咨询后，我们会向您发送其联系方式。"

        ),

        # PREVIEW

        "request_preview_title": "📋 <b>请检查您的订单</b>",

        "request_service": "🔧 <b>服务：</b>",

        "request_location": "📍 <b>工作地点：</b>",

        "request_date": "📅 <b>日期：</b>",

        "request_time": "🕐 <b>时间：</b>",

        "request_comment": "💬 <b>备注：</b>",

        "request_location_received": "已收到位置",

        "request_preliminary_price": ("💰 <b>预估价格：</b>\n"),

        "request_price_to_be_confirmed": (

            "💰 <b>预估价格：</b>\n" "价格由专业人员确认"

        ),

        "request_price_warning": ("⚠️ <i>价格仅为预估价格。</i>"),

        "request_price_inspection": ("最终价格将在专业人员检查后确定。"),

        "request_confirm_prompt": ("如果信息正确，请确认订单。"),

        "request_invalid_draft": (

            "❌ <b>无法创建订单。</b>\n\n" "请重新选择服务、发送位置、日期和时间。"

        ),

        # CREATION

        "request_confirmation_unavailable": ("⚠️ 当前没有可确认的订单。"),

        "request_creation_failed": (

            "❌ <b>无法创建订单。</b>\n\n" "{error}\n\n" "请重新开始。"

        ),

        "request_created": ("✅ <b>订单创建成功！</b>"),

        "request_number": ("📋 订单编号：<b>№{request_id}</b>"),

        "request_location_success": "📍 已收到位置",

        "request_preliminary_price_short": ("💰 预估价格：<b>起价 {price}</b>"),

        "request_price_specialist_short": ("💰 价格：<b>由专业人员确认</b>"),

        "request_sent_to_specialists": ("您的订单已发送给专业人员。"),

        "request_employee_notification": ("订单被接受后，我们会通知您。"),

        # REQUESTS

        "my_requests_title": "📋 <b>我的订单</b>",

        "my_requests_client_not_found": ("📋 <b>我的订单</b>\n\n" "未找到客户。"),

        "my_requests_empty": ("📋 <b>我的订单</b>\n\n" "您目前还没有订单。"),

        "request_created_at": "🗓 创建时间：{date}",

        "request_scheduled_at": "⏰ 到访时间：{datetime}",

        "request_price_list": "💰 起价 {price}",

        "request_rating": "⭐ 您的评分：{stars}",

        "request_not_rated": "⭐ 评分：尚未评分",

        "request_service_not_specified": "未指定服务",

        # STATUS

        "status_new": "新订单",

        "status_in_progress": "处理中",

        "status_completed": "已完成",

        "status_cancelled": "已取消",

        "status_unknown": "未知状态",

        # RATING

        "rating_service": "服务",

        "rating_completed": "✅ <b>订单已完成！</b>",

        "rating_request_number": "📋 订单 №<b>{request_id}</b>",

        "rating_service_label": "🔧 <b>服务：</b> ",

        "rating_thanks": "感谢您使用翡翠服务！",

        "rating_prompt": "⭐ <b>请评价专业人员的工作：</b>",

        "rating_help": "您的评分可以帮助我们不断改进服务。",

        "rating_success": "❤️ <b>感谢您的评分！</b>",

        "rating_your_rating": "您的评分：",

        "rating_service_better": "感谢您帮助我们改善服务！",

        "rating_star": "⭐ {rating}",

        # CALLBACKS

        "callback_unknown": "未知命令。",

        "callback_client_not_found": "未找到客户。",

        "callback_calendar_unavailable": "当前日历不可用。",

        "callback_bad_date": "日期无效。",

        "callback_bad_time": "时间无效。",

        "callback_bad_rating": "评分无效。",

        "callback_rating_range": "评分必须在1到5之间。",

        "callback_request_not_found": "未找到订单。",

        "callback_cannot_rate": "目前无法评价此订单。",

        "callback_already_rated": "您已经评价过此订单：{stars}",

        "callback_rating_success": "感谢您的评分！❤️",

        "callback_rating_save_failed": "无法保存评分。",

        "callback_bad_service": "服务无效。",

        "callback_session_stale": "订单会话已过期。",

        "callback_step_unavailable": "当前步骤不可用。",

        "callback_confirm": "正在创建订单...",

        "callback_cancel": "订单创建已取消。",

        # CONFIRM / CANCEL

        "request_cancelled": "❌ 订单创建已取消。",

        "request_already_ready": (

            "⚠️ <b>订单已经准备好。</b>\n\n"

            "请检查上面的信息，然后点击 "

            "«✅ 确认订单»。"

        ),

        "confirm_request": "✅ 确认订单",

        "edit_request": "✏️ 编辑",

        "continue": "➡️ 继续",

        "choose_another": "⬅️ 选择其他",

        # CONTACT

        "contact_title": "📞 <b>联系翡翠服务</b>",

        "contact_description": (

            "公司的联系方式将从数据库中加载。\n\n" "此部分将连接到公司模型。"

        ),

        "coordinates_not_specified": "未指定",

        "price_to_be_confirmed_short": "价格待确认",

        "no_time_slots_today": "⚠️ 今天没有可用的时间段。\n\n请选择其他日期。",
        "no_time_slots_date": "⚠️ 所选日期没有可用的时间段。\n\n请选择其他日期。",
    },

}

def get_language(client_or_language):

    if isinstance(client_or_language, str):

        language = client_or_language

    else:

        language = getattr(client_or_language, "language", DEFAULT_LANGUAGE)

    return language if language in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE

def _localize_price_value(client_or_language, value):

    if value is None:

        return value

    currency_map = {

        "ru": "сум",

        "uz": "so'm",

        "en": "UZS",

        "zh": "UZS",

    }

    currency = currency_map[get_language(client_or_language)]

    return re.sub(

        r"(?i)(?:сум|sum|so['’]?m|uzs)",

        currency,

        str(value),

    )

def _protect_placeholders(text):

    placeholders = []

    def replace(match):

        placeholders.append(match.group(0))

        return f"ZXPLACEHOLDER{len(placeholders) - 1}ZX"

    protected = re.sub(r"\\\\{[a-zA-Z_][a-zA-Z0-9_]*\\\\}", replace, text)

    return protected, placeholders

def _restore_placeholders(text, placeholders):

    for index, placeholder in enumerate(placeholders):

        text = text.replace(f"ZXPLACEHOLDER{index}ZX", placeholder)

    return text

def _translate_online(text, target_language, source_language="ru"):

    """

    Онлайн-перевод через Yandex Cloud Translate.

    Перевод вызывается только для текста, которого нет

    в статическом словаре выбранного языка.

    Реализация находится в telegram_bot.client.translations_online.

    """

    if not text or target_language == source_language:

        return text

    try:

        from .translations_online import (

            translate_online as yandex_translate_online,

        )

    except ImportError:

        return text

    protected_text, placeholders = _protect_placeholders(str(text))

    try:

        translated = yandex_translate_online(

            protected_text,

            target_language=target_language,

            source_language=source_language,

        )

        if not translated:

            return text

        return _restore_placeholders(translated, placeholders)

    except Exception:

        # Онлайн-перевод не должен ломать работу Telegram-бота.

        return text

def translate_online(text, target_language, source_language="ru"):

    """

    Публичная функция для ручного онлайн-перевода произвольного текста

    через Yandex Cloud Translate.

    """

    if target_language not in SUPPORTED_LANGUAGES:

        target_language = DEFAULT_LANGUAGE

    return _translate_online(text, target_language, source_language)

def t(client_or_language, key, **kwargs):

    language = get_language(client_or_language)

    translations = TRANSLATIONS.get(language, {})

    text = translations.get(key)

    # Если перевода в выбранном языке нет — берём русский

    # и автоматически переводим его онлайн.

    if text is None:

        russian_text = TRANSLATIONS.get(DEFAULT_LANGUAGE, {}).get(key)

        if russian_text is None:

            return key

        text = _translate_online(

            russian_text,

            target_language=language,

            source_language=DEFAULT_LANGUAGE,

        )

    if kwargs:

        try:

            format_kwargs = dict(kwargs)

            if "price" in format_kwargs:

                format_kwargs["price"] = _localize_price_value(

                    client_or_language,

                    format_kwargs["price"],

                )

            return text.format(**format_kwargs)

        except (KeyError, IndexError, ValueError):

            return text

    return text

def format_price_unit(client_or_language, unit):

    if unit is None:

        return ""

    unit_text = str(unit).strip()

    if not unit_text:

        return ""

    language = get_language(client_or_language)

    if language == "ru":

        return f"за {unit_text}"

    if language == "uz":

        return f"{unit_text} uchun"

    if language == "en":

        return f"per {unit_text}"

    if language == "zh":

        return f"/ {unit_text}"

    return f"за {unit_text}"

def get_month_name(client_or_language, month):

    try:

        month = int(month)

    except (TypeError, ValueError):

        return ""

    if not 1 <= month <= 12:

        return ""

    return t(client_or_language, f"month_{month}")

def get_weekday_name(client_or_language, weekday):

    weekday_keys = {

        0: "weekday_mon",

        1: "weekday_tue",

        2: "weekday_wed",

        3: "weekday_thu",

        4: "weekday_fri",

        5: "weekday_sat",

        6: "weekday_sun",

    }

    key = weekday_keys.get(weekday)

    return t(client_or_language, key) if key else ""
