from django.db import models


class Company(models.Model):
    name = models.CharField(
        "Название компании",
        max_length=255,
    )

    short_name = models.CharField(
        "Краткое название",
        max_length=100,
        blank=True,
    )

    description = models.TextField(
        "Описание",
        blank=True,
    )

    phone = models.CharField(
        "Основной телефон",
        max_length=50,
    )

    phone_secondary = models.CharField(
        "Дополнительный телефон",
        max_length=50,
        blank=True,
    )

    email = models.EmailField(
        "Email",
        blank=True,
    )

    address = models.CharField(
        "Адрес",
        max_length=500,
        blank=True,
    )

    city = models.CharField(
        "Город",
        max_length=100,
        default="Ташкент",
    )

    working_hours = models.CharField(
        "График работы",
        max_length=255,
        blank=True,
    )

    work_start = models.TimeField(
        "Начало рабочего дня",
        default="09:00",
    )

    work_end = models.TimeField(
        "Окончание рабочего дня",
        default="17:00",
    )

    booking_step_minutes = models.PositiveIntegerField(
        "Шаг записи (минуты)",
        default=30,
    )

    telegram_url = models.URLField(
        "Telegram",
        blank=True,
    )

    instagram_url = models.URLField(
        "Instagram",
        blank=True,
    )

    facebook_url = models.URLField(
        "Facebook",
        blank=True,
    )

    youtube_url = models.URLField(
        "YouTube",
        blank=True,
    )

    latitude = models.DecimalField(
        "Широта",
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    longitude = models.DecimalField(
        "Долгота",
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    logo = models.ImageField(
        "Логотип",
        upload_to="company/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        "Активная компания",
        default=True,
    )

    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Дата изменения",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компания"
        ordering = ["name"]

    def __str__(self):
        return self.name
