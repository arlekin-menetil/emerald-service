from decimal import Decimal

from django.core.management.base import BaseCommand

from services.models import Service, ServiceCategory

SERVICES = [
    {
        "category": "Ремонт и устранение неисправностей",
        "name": "Устранение засоров",
        "slug": "ustranenie-zasorov",
        "price_from": "180000",
        "sort_order": 1,
    },
    {
        "category": "Монтаж сантехники",
        "name": "Монтаж сантехники",
        "slug": "montazh-santehniki",
        "price_from": "130000",
        "sort_order": 2,
    },
    {
        "category": "Канализация",
        "name": "Очистка канализации",
        "slug": "ochistka-kanalizatsii",
        "price_from": "130000",
        "sort_order": 3,
    },
    {
        "category": "Ремонт и устранение неисправностей",
        "name": "Ремонт труб",
        "slug": "remont-trub",
        "price_from": "130000",
        "sort_order": 4,
    },
    {
        "category": "Монтаж сантехники",
        "name": "Ремонт заполнительного элемента",
        "slug": "remont-zapolnitelnogo-elementa",
        "price_from": "130000",
        "sort_order": 5,
    },
    {
        "category": "Ремонт и устранение неисправностей",
        "name": "Устранение утечек",
        "slug": "ustranenie-utechek",
        "price_from": "130000",
        "sort_order": 6,
    },
    {
        "category": "Монтаж сантехники",
        "name": "Установка унитаза",
        "slug": "ustanovka-unitaza",
        "price_from": "280000",
        "sort_order": 7,
    },
    {
        "category": "Монтаж сантехники",
        "name": "Установка ванны",
        "slug": "ustanovka-vanny",
        "price_from": "280000",
        "sort_order": 8,
    },
    {
        "category": "Монтаж сантехники",
        "name": "Установка душевой кабины",
        "slug": "ustanovka-dushevoy-kabiny",
        "price_from": "450000",
        "sort_order": 9,
    },
    {
        "category": "Ремонт и устранение неисправностей",
        "name": "Ремонт туалета",
        "slug": "remont-tualeta",
        "price_from": "130000",
        "sort_order": 10,
    },
    {
        "category": "Монтаж сантехники",
        "name": "Установка джакузи",
        "slug": "ustanovka-dzhakuzi",
        "price_from": "450000",
        "sort_order": 11,
    },
    {
        "category": "Монтаж сантехники",
        "name": "Установка биде",
        "slug": "ustanovka-bide",
        "price_from": "280000",
        "sort_order": 12,
    },
    {
        "category": "Канализация",
        "name": "Замена канализации",
        "slug": "zamena-kanalizatsii",
        "price_from": "450000",
        "sort_order": 13,
    },
    {
        "category": "Монтаж сантехники",
        "name": "Установка сифона",
        "slug": "ustanovka-sifona",
        "price_from": "130000",
        "sort_order": 14,
    },
    {
        "category": "Отопление",
        "name": "Монтаж котла",
        "slug": "montazh-kotla",
        "price_from": "450000",
        "sort_order": 15,
    },
    {
        "category": "Консультация",
        "name": "Диагностика и консультации",
        "slug": "diagnostika-i-konsultatsii",
        "price_from": "130000",
        "sort_order": 16,
    },
    {
        "category": "Отопление",
        "name": "Установка системы подогрева пола",
        "slug": "ustanovka-sistemy-podogreva-pola",
        "price_from": "48000",
        "price_unit": "сум/м²",
        "sort_order": 17,
    },
    {
        "category": "Консультация",
        "name": "Онлайн-консультация",
        "slug": "onlayn-konsultatsiya",
        "price_from": "0",
        "sort_order": 18,
    },
]


class Command(BaseCommand):
    help = "Создаёт и обновляет услуги ООО «Изумруд Сервис»"

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for data in SERVICES:
            category = ServiceCategory.objects.get(name=data["category"])

            defaults = {
                "category": category,
                "slug": data["slug"],
                "short_description": "",
                "description": "",
                "price_from": Decimal(data["price_from"]),
                "is_popular": False,
                "show_on_homepage": True,
                "is_active": True,
                "sort_order": data["sort_order"],
            }

            if "price_unit" in data:
                defaults["price_unit"] = data["price_unit"]

            service, created = Service.objects.update_or_create(
                name=data["name"],
                defaults=defaults,
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Создана: {service.name}"))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f"Обновлена: {service.name}"))

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Готово. Создано: {created_count}, " f"обновлено: {updated_count}"
            )
        )
