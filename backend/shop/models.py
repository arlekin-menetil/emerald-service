from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Название",
    )
    name_uz = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Название UZ",
    )
    name_en = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Название EN",
    )
    name_zh = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Название ZH",
    )

    slug = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name="Slug",
    )

    image = models.ImageField(
        upload_to="shop/categories/",
        blank=True,
        null=True,
        verbose_name="Изображение",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления",
    )

    class Meta:
        verbose_name = "Категория магазина"
        verbose_name_plural = "Категории магазина"
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Категория",
    )

    name = models.CharField(
        max_length=255,
        verbose_name="Название",
    )
    name_uz = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Название UZ",
    )
    name_en = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Название EN",
    )
    name_zh = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Название ZH",
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Slug",
    )

    sku = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Артикул",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )
    description_uz = models.TextField(
        blank=True,
        verbose_name="Описание UZ",
    )
    description_en = models.TextField(
        blank=True,
        verbose_name="Описание EN",
    )
    description_zh = models.TextField(
        blank=True,
        verbose_name="Описание ZH",
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Цена",
    )

    uzum_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на товар в Uzum",
    )


    stock_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Остаток",
    )

    image = models.ImageField(
        upload_to="shop/products/",
        blank=True,
        null=True,
        verbose_name="Фото",
    )

    is_available = models.BooleanField(
        default=True,
        verbose_name="Доступен",
    )

    is_featured = models.BooleanField(
        default=False,
        verbose_name="Популярный",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
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
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["sort_order", "-created_at"]

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='gallery',
        verbose_name='Товар',
    )

    image = models.ImageField(
        upload_to='shop/products/gallery/',
        verbose_name='Изображение',
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )

    class Meta:
        verbose_name = 'Дополнительное изображение товара'
        verbose_name_plural = 'Дополнительные изображения товаров'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f'{self.product.name} — фото {self.id}'



class UzumClick(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="uzum_clicks",
        verbose_name="Товар",
    )
    visitor_id = models.CharField(
        max_length=36,
        db_index=True,
        verbose_name="Анонимный идентификатор посетителя",
    )
    clicked_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Дата перехода",
    )

    class Meta:
        verbose_name = "Переход на Uzum"
        verbose_name_plural = "Переходы на Uzum"
        ordering = ["-clicked_at"]

    def __str__(self):
        return f"{self.product.name} — {self.clicked_at}"
