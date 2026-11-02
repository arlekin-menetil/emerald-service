from django.db import models


class Work(models.Model):
    """
    Выполненная работа для портфолио сайта.
    """

    CATEGORY_CHOICES = [
        ("plumbing", "Сантехника"),
        ("bathroom", "Ванная"),
        ("sewerage", "Канализация"),
        ("heating", "Отопление"),
        ("installation", "Монтаж"),
        ("other", "Другое"),
    ]

    title = models.CharField(
        max_length=255,
        verbose_name="Название",
    )

    title_uz = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Название (O'zbekcha)",
    )

    title_en = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Название (English)",
    )

    title_zh = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Название (中文)",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )

    description_uz = models.TextField(
        blank=True,
        verbose_name="Описание (O'zbekcha)",
    )

    description_en = models.TextField(
        blank=True,
        verbose_name="Описание (English)",
    )

    description_zh = models.TextField(
        blank=True,
        verbose_name="Описание (中文)",
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default="plumbing",
        verbose_name="Категория",
    )

    image = models.ImageField(
        upload_to="works/",
        verbose_name="Фото",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    class Meta:
        verbose_name = "Выполненная работа"
        verbose_name_plural = "Выполненные работы"
        ordering = ["sort_order", "-created_at"]

    def __str__(self):
        return self.title


class Video(models.Model):
    """
    YouTube-видео для сайта.

    Само видео на сервере не хранится.
    В базе сохраняется только YouTube URL и ID.
    """

    title = models.CharField(
        max_length=255,
        verbose_name="Название",
    )

    title_uz = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Название (O'zbekcha)",
    )

    title_en = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Название (English)",
    )

    title_zh = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Название (中文)",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )

    description_uz = models.TextField(
        blank=True,
        verbose_name="Описание (O'zbekcha)",
    )

    description_en = models.TextField(
        blank=True,
        verbose_name="Описание (English)",
    )

    description_zh = models.TextField(
        blank=True,
        verbose_name="Описание (中文)",
    )

    youtube_url = models.URLField(
        verbose_name="YouTube ссылка",
    )

    youtube_id = models.CharField(
        max_length=32,
        blank=True,
        verbose_name="YouTube ID",
        help_text="Например: dQw4w9WgXcQ",
    )

    thumbnail = models.ImageField(
        upload_to="videos/",
        blank=True,
        null=True,
        verbose_name="Своё превью",
        help_text="Необязательно. Если не указано, используем превью YouTube.",
    )

    category = models.CharField(
        max_length=30,
        choices=Work.CATEGORY_CHOICES,
        default="plumbing",
        verbose_name="Категория",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
        ordering = ["sort_order", "-created_at"]

    def __str__(self):
        return self.title
