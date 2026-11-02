from django.db import models

from employees.services.name_translation import (
    translate_employee_name,
    translate_employee_website_name,
)


class Employee(models.Model):
    # ==========================================
    # ОСНОВНЫЕ ДАННЫЕ
    # ==========================================

    website_name = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Имя на сайте",
        help_text="Имя, которое будет отображаться на публичном сайте. Если оставить пустым, используется ФИО.",
    )

    website_name_uz = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Имя на сайте — O‘zbek",
    )

    website_name_en = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Имя на сайте — English",
    )

    website_name_zh = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Имя на сайте — 中文",
    )

    name = models.CharField(
        max_length=150,
        verbose_name="ФИО",
    )

    name_uz = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="ФИО — O‘zbek",
    )

    name_en = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="ФИО — English",
    )

    name_zh = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="ФИО — 中文",
    )

    position = models.CharField(
        max_length=100,
        default="Сантехник",
        verbose_name="Должность",
    )

    position_uz = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Должность — O‘zbek",
    )

    position_en = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Должность — English",
    )

    position_zh = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Должность — 中文",
    )

    experience = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Опыт работы",
        help_text="Количество лет опыта",
    )

    phone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Телефон",
    )

    # ==========================================
    # ЯЗЫК СОТРУДНИКА
    # ==========================================

    LANGUAGE_RU = "ru"
    LANGUAGE_UZ = "uz"

    LANGUAGE_CHOICES = [
        (
            LANGUAGE_RU,
            "Русский",
        ),
        (
            LANGUAGE_UZ,
            "O'zbekcha",
        ),
    ]

    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default=LANGUAGE_RU,
        verbose_name="Язык",
        db_index=True,
        help_text="Язык интерфейса и сообщений сотрудника в Telegram.",
    )

    # ==========================================
    # TELEGRAM
    # ==========================================

    telegram_id = models.BigIntegerField(
        null=True,
        blank=True,
        unique=True,
        verbose_name="Telegram ID",
        help_text=("Заполняется автоматически при привязке " "сотрудника через бота."),
    )

    telegram_username = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Telegram username",
        help_text=("Например: miomoto. " "Заполняется ботом автоматически."),
    )

    # ==========================================
    # ФОТО
    # ==========================================

    photo = models.ImageField(
        upload_to="employees/",
        null=True,
        blank=True,
        verbose_name="Фото",
    )

    # ==========================================
    # СТАТУС
    # ==========================================

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
    )

    is_published = models.BooleanField(
        default=False,
        verbose_name="Показывать на сайте",
        help_text="Если включено, сотрудник отображается на публичном сайте.",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок на сайте",
        help_text="Чем меньше число, тем выше сотрудник отображается на сайте.",
    )

    # ==========================================
    # ДАТЫ
    # ==========================================

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    # ==========================================
    # META
    # ==========================================

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["name"]

    # ==========================================
    # STRING
    # ==========================================


    def save(self, *args, **kwargs):
        name_changed = True
        website_name_changed = True

        if self.pk:
            old = (
                Employee.objects
                .filter(pk=self.pk)
                .values(
                    "name",
                    "website_name",
                )
                .first()
            )

            if old:
                name_changed = old["name"] != self.name
                website_name_changed = old["website_name"] != self.website_name

        name_translations_missing = not all([
            self.name_uz,
            self.name_en,
            self.name_zh,
        ])

        if self.name and (name_changed or name_translations_missing):
            translations = translate_employee_name(self.name)

            self.name_uz = translations.get("name_uz", "")
            self.name_en = translations.get("name_en", "")
            self.name_zh = translations.get("name_zh", "")

        website_translations_missing = not all([
            self.website_name_uz,
            self.website_name_en,
            self.website_name_zh,
        ])

        if self.website_name:
            if website_name_changed or website_translations_missing:
                translations = translate_employee_website_name(
                    self.website_name
                )

                self.website_name_uz = translations.get(
                    "website_name_uz",
                    "",
                )
                self.website_name_en = translations.get(
                    "website_name_en",
                    "",
                )
                self.website_name_zh = translations.get(
                    "website_name_zh",
                    "",
                )
        else:
            self.website_name_uz = ""
            self.website_name_en = ""
            self.website_name_zh = ""

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
