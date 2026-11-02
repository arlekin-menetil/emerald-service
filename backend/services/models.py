from django.db import models
from django.utils.text import slugify


class ServiceCategory(models.Model):
    """
    Категория сантехнических услуг.
    """

    name = models.CharField(
        max_length=255,
        verbose_name="Название",
    )

    name_uz = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Название (O'zbekcha)",
    )

    name_en = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Название (English)",
    )

    name_zh = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Название (中文)",
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        verbose_name="Slug",
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

    image = models.ImageField(
        upload_to="services/categories/",
        blank=True,
        null=True,
        verbose_name="Изображение",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    class Meta:
        verbose_name = "Категория услуг"
        verbose_name_plural = "Категории услуг"
        ordering = ["sort_order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Service(models.Model):
    """
    Конкретная сантехническая услуга.
    """

    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.PROTECT,
        related_name="services",
        verbose_name="Категория",
    )

    name = models.CharField(
        max_length=255,
        verbose_name="Название услуги",
    )

    name_uz = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Название услуги (O'zbekcha)",
    )

    name_en = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Название услуги (English)",
    )

    name_zh = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Название услуги (中文)",
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        verbose_name="Slug",
    )

    short_description = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Краткое описание",
    )

    short_description_uz = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Краткое описание (O'zbekcha)",
    )

    short_description_en = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Краткое описание (English)",
    )

    short_description_zh = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Краткое описание (中文)",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Полное описание",
    )

    description_uz = models.TextField(
        blank=True,
        verbose_name="Полное описание (O'zbekcha)",
    )

    description_en = models.TextField(
        blank=True,
        verbose_name="Полное описание (English)",
    )

    description_zh = models.TextField(
        blank=True,
        verbose_name="Полное описание (中文)",
    )

    price_from = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Цена от",
        help_text="Цена в сумах. Например: 180000",
    )

    price_unit = models.CharField(
        max_length=100,
        blank=True,
        default="услуга",
        verbose_name="Единица цены",
        help_text="Например: услуга, метр, точка",
    )

    price_unit_uz = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Единица цены (O'zbekcha)",
    )

    price_unit_en = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Единица цены (English)",
    )

    price_unit_zh = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Единица цены (中文)",
    )

    image = models.ImageField(
        upload_to="services/",
        blank=True,
        null=True,
        verbose_name="Изображение",
    )

    is_popular = models.BooleanField(
        default=False,
        verbose_name="Популярная",
    )

    show_on_homepage = models.BooleanField(
        default=False,
        verbose_name="Показывать на главной",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
    )

    seo_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="SEO Title",
    )

    seo_description = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="SEO Description",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["sort_order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
