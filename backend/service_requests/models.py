import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class ServiceRequest(models.Model):
    """
    Заявка клиента на сантехнические работы.

    Жизненный цикл заявки:

        new
            ↓
        in_progress
            ↓
        completed

    В любой момент заявка также может быть отменена:

        new / in_progress → cancelled

    К заявке можно назначить одного или нескольких
    сотрудников-сантехников.

    Для обычной заявки клиент указывает желаемое
    время приезда сантехника и местоположение.

    Для онлайн-консультации местоположение не требуется.

    Заявка может быть создана:
        - через сайт;
        - через Telegram-бота.

    Если заявка создана через Telegram,
    telegram_client содержит связанного клиента.

    После выполнения клиент может оставить
    оценку от 1 до 5.
    """

    # ==========================================================
    # STATUS
    # ==========================================================

    STATUS_NEW = "new"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (
            STATUS_NEW,
            "Новая",
        ),
        (
            STATUS_IN_PROGRESS,
            "В работе",
        ),
        (
            STATUS_COMPLETED,
            "Выполнена",
        ),
        (
            STATUS_CANCELLED,
            "Отменена",
        ),
    ]

    # ==========================================================
    # REQUEST TYPE
    # ==========================================================

    REQUEST_TYPE_SERVICE = "service"
    REQUEST_TYPE_CONSULTATION = "consultation"

    REQUEST_TYPE_CHOICES = [
        (
            REQUEST_TYPE_SERVICE,
            "Обычная услуга",
        ),
        (
            REQUEST_TYPE_CONSULTATION,
            "Онлайн-консультация",
        ),
    ]

    request_type = models.CharField(
        max_length=30,
        choices=REQUEST_TYPE_CHOICES,
        default=REQUEST_TYPE_SERVICE,
        verbose_name="Тип заявки",
        db_index=True,
        help_text=(
            "Тип заявки: обычная сантехническая услуга " "или онлайн-консультация."
        ),
    )

    # ==========================================================
    # CLIENT
    # ==========================================================

    LANGUAGE_RU = "ru"
    LANGUAGE_UZ = "uz"
    LANGUAGE_EN = "en"
    LANGUAGE_ZH = "zh"

    LANGUAGE_CHOICES = [
        (LANGUAGE_RU, "Русский"),
        (LANGUAGE_UZ, "O‘zbekcha"),
        (LANGUAGE_EN, "English"),
        (LANGUAGE_ZH, "中文"),
    ]


    name = models.CharField(
        verbose_name="Имя клиента",
        max_length=150,
    )

    phone = models.CharField(
        verbose_name="Телефон",
        max_length=50,
    )

    language = models.CharField(
        verbose_name="Язык клиента",
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default=LANGUAGE_RU,
        db_index=True,
        help_text="Язык, выбранный клиентом при создании заявки.",
    )

    address = models.CharField(
        verbose_name="Адрес клиента",
        max_length=500,
        blank=True,
        help_text=(
            "Текстовый адрес клиента. "
            "Может быть заполнен вручную или получен "
            "из географических координат."
        ),
    )

    # ==========================================================
    # LOCATION
    # ==========================================================

    latitude = models.DecimalField(
        verbose_name="Широта",
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Географическая широта местоположения клиента.",
    )

    longitude = models.DecimalField(
        verbose_name="Долгота",
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Географическая долгота местоположения клиента.",
    )

    # ==========================================================
    # TELEGRAM CLIENT
    # ==========================================================

    telegram_client = models.ForeignKey(
        "telegram_clients.TelegramClient",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="service_requests",
        verbose_name="Telegram-клиент",
        help_text=(
            "Заполняется автоматически, если заявка " "создана через Telegram-бота."
        ),
    )

    client_assignment_message_id = models.BigIntegerField(
        verbose_name="Telegram message ID уведомления клиенту",
        null=True,
        blank=True,
        help_text=(
            "ID сообщения Telegram, которое бот отправил клиенту "
            "после назначения сантехника."
        ),
    )

    client_request_message_id = models.BigIntegerField(
        verbose_name="Telegram message ID сообщения о создании заявки",
        null=True,
        blank=True,
        help_text=(
            "ID сообщения Telegram, которое бот отправил клиенту "
            "после создания заявки."
        ),
    )

    # ==========================================================
    # ARRIVAL / CONSULTATION TIME
    # ==========================================================

    scheduled_at = models.DateTimeField(
        verbose_name="Желаемое время",
        null=True,
        blank=True,
        db_index=True,
        help_text=(
            "Для обычной заявки — желаемое время приезда. "
            "Для онлайн-консультации — запланированное время консультации."
        ),
    )

    # ==========================================================
    # REQUEST
    # ==========================================================

    service = models.ForeignKey(
        "services.Service",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="requests",
        verbose_name="Услуга",
    )

    # ==========================================================
    # EMPLOYEES
    # ==========================================================

    employees = models.ManyToManyField(
        "employees.Employee",
        blank=True,
        related_name="service_requests",
        verbose_name="Сотрудники на вызове",
        help_text=(
            "Сантехники, назначенные на выполнение " "данной заявки или консультации."
        ),
    )

    # ==========================================================
    # COMMENT / QUESTION
    # ==========================================================

    comment = models.TextField(
        verbose_name="Комментарий / вопрос",
        blank=True,
        help_text=(
            "Для обычной заявки — комментарий клиента. "
            "Для онлайн-консультации — вопрос клиента."
        ),
    )

    # ==========================================================
    # STATUS
    # ==========================================================

    status = models.CharField(
        verbose_name="Статус",
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
        db_index=True,
    )

    completed_at = models.DateTimeField(
        verbose_name="Дата выполнения",
        null=True,
        blank=True,
    )

    # ==========================================================
    # RATING
    # ==========================================================

    rating = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

    rating_token = models.UUIDField(
        verbose_name="Токен оценки",
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    # ==========================================================
    # TIMESTAMPS
    # ==========================================================

    created_at = models.DateTimeField(
        verbose_name="Дата заявки",
        auto_now_add=True,
        db_index=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # ==========================================================
    # META
    # ==========================================================

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

        ordering = [
            "-created_at",
        ]

        indexes = [
            models.Index(
                fields=[
                    "status",
                    "-created_at",
                ],
                name="request_status_created_idx",
            ),
            models.Index(
                fields=[
                    "phone",
                ],
                name="request_phone_idx",
            ),
            models.Index(
                fields=[
                    "request_type",
                    "-created_at",
                ],
                name="request_type_created_idx",
            ),
        ]

    # ==========================================================
    # STRING
    # ==========================================================

    def __str__(self):
        return f"{self.name} — {self.phone}"

    # ==========================================================
    # REQUEST TYPE HELPERS
    # ==========================================================

    @property
    def is_consultation(self):
        """
        Возвращает True, если заявка является
        онлайн-консультацией.
        """

        return self.request_type == self.REQUEST_TYPE_CONSULTATION

    @property
    def is_service_request(self):
        """
        Возвращает True, если заявка является
        обычной сантехнической услугой.
        """

        return self.request_type == self.REQUEST_TYPE_SERVICE

    # ==========================================================
    # STATUS METHODS
    # ==========================================================

    def mark_completed(self):
        """
        Перевести заявку в статус «Выполнена».

        Если completed_at ещё не установлен,
        автоматически устанавливаем текущее время.
        """

        self.status = self.STATUS_COMPLETED

        if self.completed_at is None:
            self.completed_at = timezone.now()

        self.save(
            update_fields=[
                "status",
                "completed_at",
                "updated_at",
            ],
        )

    # ==========================================================
    # RATING
    # ==========================================================

    @property
    def is_rated(self):
        """
        Возвращает True, если клиент уже оставил оценку.
        """

        return self.rating is not None


# ==============================================================
# REQUEST TRANSLATION
# ==============================================================


class RequestTranslation(models.Model):
    """
    Перевод текста заявки для конкретного языка сотрудника.

    Оригинальный текст заявки никогда не изменяется.

    Например:

        source_language = "en"
        target_language = "ru"

        source_text =
            "My sink is leaking"

        translated_text =
            "У меня протекает раковина."

    Для одной заявки могут существовать несколько переводов:

        EN → RU
        EN → UZ

    или:

        ZH → RU
        ZH → UZ
    """

    # ==========================================================
    # RELATION
    # ==========================================================

    service_request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name="translations",
        verbose_name="Заявка",
    )

    # ==========================================================
    # LANGUAGES
    # ==========================================================

    source_language = models.CharField(
        max_length=2,
        verbose_name="Исходный язык",
        db_index=True,
        help_text=("Язык, на котором клиент написал " "комментарий или вопрос."),
    )

    target_language = models.CharField(
        max_length=2,
        verbose_name="Язык перевода",
        db_index=True,
        help_text=("Язык, на который переводится " "текст для сотрудника."),
    )

    # ==========================================================
    # TEXT
    # ==========================================================

    source_text = models.TextField(
        verbose_name="Оригинальный текст",
    )

    translated_text = models.TextField(
        verbose_name="Переведённый текст",
    )

    # ==========================================================
    # TIMESTAMPS
    # ==========================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    # ==========================================================
    # META
    # ==========================================================

    class Meta:
        verbose_name = "Перевод заявки"
        verbose_name_plural = "Переводы заявок"

        ordering = [
            "-created_at",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "service_request",
                    "source_language",
                    "target_language",
                    "source_text",
                ],
                name="unique_request_translation",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "service_request",
                    "source_language",
                    "target_language",
                ],
                name="request_translation_lang_idx",
            ),
        ]

    # ==========================================================
    # STRING
    # ==========================================================

    def __str__(self):
        return (
            f"Заявка #{self.service_request_id}: "
            f"{self.source_language} → "
            f"{self.target_language}"
        )


# ==============================================================
# EMPLOYEE RESPONSE
# ==============================================================


class ServiceRequestEmployeeResponse(models.Model):
    """
    Ответ конкретного сантехника на заявку.

    Каждый сантехник имеет отдельный ответ
    по каждой заявке.

    Возможные состояния:

        pending
            ↓
        accepted
            ↓
        completed

        pending
            ↓
        declined

    Сотрудник может изменить свой ответ.

    completed означает, что именно этот сантехник
    сообщил о выполнении своей работы.
    """

    # ==========================================================
    # RESPONSE STATUS
    # ==========================================================

    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_DECLINED = "declined"
    STATUS_COMPLETED = "completed"

    STATUS_CHOICES = [
        (
            STATUS_PENDING,
            "Ожидает ответа",
        ),
        (
            STATUS_ACCEPTED,
            "Едет",
        ),
        (
            STATUS_DECLINED,
            "Не может",
        ),
        (
            STATUS_COMPLETED,
            "Выполнил",
        ),
    ]

    # ==========================================================
    # RELATIONS
    # ==========================================================

    service_request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name="employee_responses",
        verbose_name="Заявка",
    )

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.CASCADE,
        related_name="request_responses",
        verbose_name="Сотрудник",
    )

    # ==========================================================
    # STATUS
    # ==========================================================

    status = models.CharField(
        verbose_name="Ответ",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        db_index=True,
    )

    had_accepted = models.BooleanField(
        default=False,
        verbose_name="Ранее принимал заявку",
        help_text=(
            "Показывает, что сотрудник ранее уже принимал "
            "эту заявку и может повторно выбрать ответ после "
            "изменения своего решения."
        ),
    )

    # ==========================================================
    # RESPONSE TIME
    # ==========================================================

    responded_at = models.DateTimeField(
        verbose_name="Дата ответа",
        null=True,
        blank=True,
    )

    # ==========================================================
    # TELEGRAM EMPLOYEE MESSAGE
    # ==========================================================

    employee_message_id = models.BigIntegerField(
        verbose_name="Telegram message ID сотрудника",
        null=True,
        blank=True,
        help_text=(
            "ID личного сообщения с заявкой, "
            "которое бот отправил сотруднику в Telegram."
        ),
    )

    # ==========================================================
    # TIMESTAMPS
    # ==========================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    # ==========================================================
    # META
    # ==========================================================

    class Meta:
        verbose_name = "Ответ сантехника"
        verbose_name_plural = "Ответы сантехников"

        ordering = [
            "employee__name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "service_request",
                    "employee",
                ],
                name="unique_request_employee_response",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "service_request",
                    "status",
                ],
                name="request_employee_status_idx",
            ),
        ]

    # ==========================================================
    # STRING
    # ==========================================================

    def __str__(self):
        return (
            f"{self.service_request} — "
            f"{self.employee} — "
            f"{self.get_status_display()}"
        )
