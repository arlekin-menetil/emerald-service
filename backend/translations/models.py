from django.db import models


class Translation(models.Model):
    """
    Статический перевод интерфейса сайта.

    Один объект = один translation key
    с переводами на RU / UZ / EN / ZH.
    """

    key = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="Ключ",
    )

    ru = models.TextField(
        blank=True,
        default="",
        verbose_name="Русский",
    )

    uz = models.TextField(
        blank=True,
        default="",
        verbose_name="O‘zbek",
    )

    en = models.TextField(
        blank=True,
        default="",
        verbose_name="English",
    )

    zh = models.TextField(
        blank=True,
        default="",
        verbose_name="中文",
    )

    # ==========================================================
    # SOURCE
    # ==========================================================

    source_file = models.CharField(
        max_length=500,
        blank=True,
        default="",
        verbose_name="Исходный файл",
        help_text="Frontend-файл, откуда взят исходный текст.",
    )

    source_text = models.TextField(
        blank=True,
        default="",
        verbose_name="Исходный текст",
        help_text="Оригинальный текст интерфейса.",
    )

    source_line = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Строка",
        help_text="Номер строки в исходном frontend-файле.",
    )

    description = models.TextField(
        blank=True,
        default="",
        verbose_name="Описание",
    )

    # ==========================================================
    # STATUS
    # ==========================================================

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="Активен",
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
        verbose_name = "Перевод сайта"
        verbose_name_plural = "Переводы сайта"
        ordering = ["key"]

    # ==========================================================
    # STRING
    # ==========================================================

    def __str__(self):
        return self.key
