from django.db import models


class VacancyApplication(models.Model):
    STATUS_NEW = "new"
    STATUS_REVIEWED = "reviewed"
    STATUS_ACCEPTED = "accepted"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_NEW, "Новая"),
        (STATUS_REVIEWED, "На рассмотрении"),
        (STATUS_ACCEPTED, "Принята"),
        (STATUS_REJECTED, "Отклонена"),
    ]

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
        max_length=150,
        verbose_name="Имя",
    )

    phone = models.CharField(
        max_length=50,
        verbose_name="Телефон",
    )

    experience = models.CharField(
        max_length=500,
        verbose_name="Опыт работы",
    )

    specialization = models.CharField(
        max_length=255,
        verbose_name="Специализация",
    )

    about = models.TextField(
        max_length=3000,
        verbose_name="О себе",
    )

    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default=LANGUAGE_RU,
        db_index=True,
        verbose_name="Язык заявки",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
        db_index=True,
        verbose_name="Статус",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Дата создания",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка на вакансию"
        verbose_name_plural = "Заявки на вакансии"

    def __str__(self):
        return f"#{self.pk} — {self.name} — {self.specialization}"
