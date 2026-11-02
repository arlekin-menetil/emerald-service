from django.db import models


class TelegramClient(models.Model):
    """
    Клиент, который привязал свой Telegram
    к системе «Изумруд Сервис».
    """

    # ==========================================
    # ОСНОВНЫЕ ДАННЫЕ
    # ==========================================

    telegram_id = models.BigIntegerField(
        unique=True,
        verbose_name="Telegram ID",
    )

    telegram_username = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Telegram username",
    )

    name = models.CharField(
        max_length=150,
        verbose_name="Имя клиента",
    )

    phone = models.CharField(
        max_length=50,
        verbose_name="Телефон",
    )

    # ==========================================
    # ЯЗЫК КЛИЕНТА
    # ==========================================

    LANGUAGE_RU = "ru"
    LANGUAGE_UZ = "uz"
    LANGUAGE_EN = "en"
    LANGUAGE_ZH = "zh"

    LANGUAGE_CHOICES = [
        (
            LANGUAGE_RU,
            "Русский",
        ),
        (
            LANGUAGE_UZ,
            "O'zbekcha",
        ),
        (
            LANGUAGE_EN,
            "English",
        ),
        (
            LANGUAGE_ZH,
            "中文",
        ),
    ]

    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default=LANGUAGE_RU,
        verbose_name="Язык",
        db_index=True,
        help_text="Язык интерфейса и сообщений клиента в Telegram.",
    )

    # ==========================================
    # СОСТОЯНИЕ ДИАЛОГА
    # ==========================================

    FLOW_NONE = "none"
    FLOW_CHOOSING_SERVICE = "choosing_service"
    FLOW_WAITING_ADDRESS = "waiting_address"

    # Новый отдельный этап выбора даты
    FLOW_CHOOSING_DATE = "choosing_date"

    # Новый отдельный этап выбора времени
    FLOW_CHOOSING_TIME = "choosing_time"

    FLOW_WAITING_COMMENT = "waiting_comment"
    FLOW_CONFIRMING = "confirming"

    FLOW_STATE_CHOICES = [
        (
            FLOW_NONE,
            "Нет активного действия",
        ),
        (
            FLOW_CHOOSING_SERVICE,
            "Выбор услуги",
        ),
        (
            FLOW_WAITING_ADDRESS,
            "Ожидание адреса",
        ),
        (
            FLOW_CHOOSING_DATE,
            "Выбор даты",
        ),
        (
            FLOW_CHOOSING_TIME,
            "Выбор времени",
        ),
        (
            FLOW_WAITING_COMMENT,
            "Ожидание комментария",
        ),
        (
            FLOW_CONFIRMING,
            "Подтверждение заявки",
        ),
    ]

    flow_state = models.CharField(
        max_length=50,
        choices=FLOW_STATE_CHOICES,
        default=FLOW_NONE,
        verbose_name="Состояние диалога",
        db_index=True,
        help_text=("Текущий этап оформления заявки " "через Telegram."),
    )

    # ==========================================
    # ЧЕРНОВИК ЗАЯВКИ
    # ==========================================

    draft_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Черновик заявки",
        help_text=("Временные данные заявки, " "которую клиент сейчас оформляет."),
    )

    # ==========================================
    # ДАТЫ
    # ==========================================

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    # ==========================================
    # META
    # ==========================================

    class Meta:
        verbose_name = "Telegram-клиент"
        verbose_name_plural = "Telegram-клиенты"
        ordering = [
            "name",
        ]

    # ==========================================
    # STRING
    # ==========================================

    def __str__(self):
        return f"{self.name} — {self.phone}"

    # ==========================================
    # DRAFT HELPERS
    # ==========================================

    def clear_draft(self):
        """
        Полностью очищает текущий черновик заявки
        и сбрасывает состояние диалога.
        """

        self.flow_state = self.FLOW_NONE
        self.draft_data = {}

        self.save(
            update_fields=[
                "flow_state",
                "draft_data",
                "updated_at",
            ],
        )

    def start_draft(self):
        """
        Начинает новый черновик заявки.
        """

        self.flow_state = self.FLOW_CHOOSING_SERVICE
        self.draft_data = {}

        self.save(
            update_fields=[
                "flow_state",
                "draft_data",
                "updated_at",
            ],
        )

    def set_draft_value(
        self,
        key,
        value,
    ):
        """
        Сохраняет одно значение в черновик.

        Например:

            client.set_draft_value(
                "service_id",
                7,
            )
        """

        draft = dict(
            self.draft_data or {},
        )

        draft[key] = value

        self.draft_data = draft

        self.save(
            update_fields=[
                "draft_data",
                "updated_at",
            ],
        )

    def get_draft_value(
        self,
        key,
        default=None,
    ):
        """
        Получает значение из черновика.
        """

        draft = self.draft_data or {}

        return draft.get(
            key,
            default,
        )

    def set_flow_state(
        self,
        state,
    ):
        """
        Меняет состояние текущего диалога.
        """

        valid_states = {choice[0] for choice in self.FLOW_STATE_CHOICES}

        if state not in valid_states:
            raise ValueError(f"Неизвестное состояние TelegramClient: {state}")

        self.flow_state = state

        self.save(
            update_fields=[
                "flow_state",
                "updated_at",
            ],
        )
