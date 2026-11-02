from django.db import models


class TelegramUser(models.Model):
    """
    Пользователь Telegram, обнаруженный ботом.

    Это общая сущность для Telegram-пользователей:
    клиентов, сотрудников и других участников чатов.
    """

    LANGUAGE_RU = "ru"
    LANGUAGE_UZ = "uz"
    LANGUAGE_EN = "en"
    LANGUAGE_ZH = "zh"

    LANGUAGE_CHOICES = [
        (LANGUAGE_RU, "Русский"),
        (LANGUAGE_UZ, "O'zbekcha"),
        (LANGUAGE_EN, "English"),
        (LANGUAGE_ZH, "中文"),
    ]

    telegram_id = models.BigIntegerField(
        unique=True,
        verbose_name="Telegram ID",
    )

    username = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Username",
    )

    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Имя",
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Фамилия",
    )

    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default=LANGUAGE_RU,
        verbose_name="Язык",
        db_index=True,
        help_text="Язык интерфейса и сообщений пользователя Telegram.",
    )

    language_selected = models.BooleanField(
        default=False,
        verbose_name="Язык выбран",
        help_text="Пользователь уже выбрал язык интерфейса.",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата обнаружения",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    class Meta:
        verbose_name = "Telegram-пользователь"
        verbose_name_plural = "Telegram-пользователи"
        ordering = ["first_name", "last_name"]

    def __str__(self):
        username = f"@{self.username}" if self.username else "без username"

        full_name = " ".join(
            part
            for part in [
                self.first_name,
                self.last_name,
            ]
            if part
        )

        return f"{full_name or 'Без имени'} — " f"{username} — " f"{self.telegram_id}"


class TelegramChat(models.Model):
    """
    Telegram-чат или группа, известная системе.
    """

    CHAT_TYPE_PRIVATE = "private"
    CHAT_TYPE_GROUP = "group"
    CHAT_TYPE_SUPERGROUP = "supergroup"
    CHAT_TYPE_CHANNEL = "channel"

    CHAT_TYPE_CHOICES = [
        (
            CHAT_TYPE_PRIVATE,
            "Личная переписка",
        ),
        (
            CHAT_TYPE_GROUP,
            "Группа",
        ),
        (
            CHAT_TYPE_SUPERGROUP,
            "Супергруппа",
        ),
        (
            CHAT_TYPE_CHANNEL,
            "Канал",
        ),
    ]

    chat_id = models.BigIntegerField(
        unique=True,
        verbose_name="Telegram Chat ID",
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Название",
    )

    username = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Username",
    )

    chat_type = models.CharField(
        max_length=30,
        choices=CHAT_TYPE_CHOICES,
        verbose_name="Тип чата",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата обнаружения",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    class Meta:
        verbose_name = "Telegram-чат"
        verbose_name_plural = "Telegram-чаты"
        ordering = ["title", "chat_id"]

    def __str__(self):
        return self.title or str(self.chat_id)


class TelegramChatMember(models.Model):
    """
    Связь Telegram-пользователя с Telegram-чатом.

    Один пользователь может состоять в нескольких чатах.
    Один чат может содержать множество пользователей.
    """

    chat = models.ForeignKey(
        TelegramChat,
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name="Telegram-чат",
    )

    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name="chat_memberships",
        verbose_name="Telegram-пользователь",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Участник активен",
    )

    joined_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    class Meta:
        verbose_name = "Участник Telegram-чата"
        verbose_name_plural = "Участники Telegram-чатов"
        ordering = ["chat", "user"]

        constraints = [
            models.UniqueConstraint(
                fields=["chat", "user"],
                name="unique_telegram_chat_member",
            ),
        ]

    def __str__(self):
        return f"{self.user} → {self.chat}"
