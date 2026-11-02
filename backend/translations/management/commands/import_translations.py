from django.core.management.base import BaseCommand

from translations.data import TRANSLATIONS, TRANSLATION_SOURCES
from translations.models import Translation


class Command(BaseCommand):
    help = "Импортирует статические переводы из translations/data.py в базу данных."

    def handle(self, *args, **options):
        languages = ("ru", "uz", "en", "zh")

        total = 0
        created = 0
        updated = 0

        for language in languages:
            for key, value in TRANSLATIONS.get(language, {}).items():
                total += 1

                source = TRANSLATION_SOURCES.get(key, {})

                defaults = {
                    "ru": TRANSLATIONS.get("ru", {}).get(key, ""),
                    "uz": TRANSLATIONS.get("uz", {}).get(key, ""),
                    "en": TRANSLATIONS.get("en", {}).get(key, ""),
                    "zh": TRANSLATIONS.get("zh", {}).get(key, ""),
                    "source_file": source.get("file", ""),
                    "source_text": source.get("source", ""),
                    "source_line": source.get("line"),
                    "description": source.get("description", ""),
                    "is_active": True,
                }

                obj, was_created = Translation.objects.update_or_create(
                    key=key,
                    defaults=defaults,
                )

                if was_created:
                    created += 1
                else:
                    updated += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Импорт переводов завершён."))
        self.stdout.write(f"Ключей обработано: {total}")
        self.stdout.write(f"Создано: {created}")
        self.stdout.write(f"Обновлено: {updated}")
        self.stdout.write(
            f"Всего записей в БД: {Translation.objects.count()}"
        )
