#!/usr/bin/env python3

from __future__ import annotations

import argparse
import ast
import json
import re
from collections import Counter
from pathlib import Path


FRONTEND_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = FRONTEND_ROOT / "src"
BACKEND_ROOT = FRONTEND_ROOT.parent / "backend"
TRANSLATIONS_FILE = BACKEND_ROOT / "translations" / "data.py"
INVENTORY_FILE = FRONTEND_ROOT / "translation_inventory.json"

EXTENSIONS = {".vue", ".js", ".jsx", ".html"}

IGNORED_DIRS = {
    "node_modules",
    "dist",
    ".git",
    ".vite",
    "coverage",
}

IGNORED_FILE_PATTERNS = (
    "*.backup.vue",
    "*.before-geocode.vue",
    "*.new.vue",
)

RUSSIAN_RE = re.compile(r"[А-Яа-яЁё]+")

# Слова, которые чаще всего являются кодом, а не пользовательским текстом.
TECHNICAL_WORDS = {
    "includes",
    "return",
    "const",
    "let",
    "function",
    "async",
    "await",
    "true",
    "false",
    "null",
    "undefined",
    "ref",
    "computed",
    "value",
    "error",
    "response",
    "request",
    "axios",
    "router",
    "params",
    "props",
    "emit",
    "category",
    "name",
    "description",
    "service",
    "services",
    "loading",
    "selected",
    "active",
    "image",
    "title",
    "content",
    "data",
}

# Русские строки, которые явно являются техническими/служебными.
TECHNICAL_PATTERNS = [
    r"name\.includes\s*\(",
    r"categoryName",
    r"console\.",
    r"throw new",
    r"catch\s*\(",
    r"axios\.",
    r"window\.",
    r"document\.",
    r"localStorage",
    r"sessionStorage",
    r"import\s+",
    r"export\s+",
    r"from\s+['\"]",
    r"process\.",
    r"API_BASE_URL",
    r"getLocalized",
    r"normalizeService",
    r"buildCategories",
]


def is_ignored_file(path: Path) -> bool:
    for pattern in IGNORED_FILE_PATTERNS:
        if path.match(pattern):
            return True

    return False


def should_scan(path: Path) -> bool:
    if path.suffix.lower() not in EXTENSIONS:
        return False

    if is_ignored_file(path):
        return False

    for part in path.parts:
        if part in IGNORED_DIRS:
            return False

    return True


def strip_comments(text: str) -> str:
    # HTML/Vue comments
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)

    # JS block comments
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)

    # JS single-line comments
    lines = []
    for line in text.splitlines():
        stripped = line.strip()

        if stripped.startswith("//"):
            continue

        lines.append(line)

    return "\n".join(lines)


def contains_russian(text: str) -> bool:
    return bool(RUSSIAN_RE.search(text))


def russian_words(text: str) -> list[str]:
    return RUSSIAN_RE.findall(text)


def is_technical_context(text: str) -> bool:
    return any(
        re.search(pattern, text, flags=re.I | re.S)
        for pattern in TECHNICAL_PATTERNS
    )


def clean_fragment(fragment: str) -> str:
    fragment = fragment.strip()
    fragment = re.sub(r"\s+", " ", fragment)

    # Убираем мусор вокруг строки.
    fragment = fragment.strip("`'\" ")

    return fragment


def looks_like_real_ui_text(fragment: str) -> bool:
    fragment = clean_fragment(fragment)

    if not fragment:
        return False

    if len(fragment) < 2:
        return False

    if not contains_russian(fragment):
        return False

    # Явно технический контекст.
    if is_technical_context(fragment):
        return False

    # Очень похоже на JS/Python expression.
    if any(
        token in fragment
        for token in [
            "=>",
            "===",
            "!==",
            "&&",
            "||",
            "?.",
            "${",
            "http://",
            "https://",
        ]
    ):
        return False

    # Не считаем чистые имена переменных.
    if re.fullmatch(r"[A-Za-zА-Яа-яЁё_][A-Za-zА-Яа-яЁё0-9_]*", fragment):
        if fragment.lower() in TECHNICAL_WORDS:
            return False

    # CSS-классы/селекторы.
    if fragment.startswith(".") or fragment.startswith("#"):
        return False

    # Обычно это backend/API path.
    if "/" in fragment and not re.search(r"\s", fragment):
        return False

    return True


def extract_vue_visible_text(text: str) -> list[str]:
    results = []

    # 1. Обычный текст между HTML-тегами.
    template_match = re.search(
        r"<template[^>]*>(.*?)</template>",
        text,
        flags=re.S | re.I,
    )

    if template_match:
        template = template_match.group(1)

        # Удаляем Vue-комментарии.
        template = re.sub(r"<!--.*?-->", "", template, flags=re.S)

        # Удаляем теги.
        chunks = re.sub(r"<[^>]+>", "\n", template)

        for line in chunks.splitlines():
            line = clean_fragment(line)

            if looks_like_real_ui_text(line):
                results.append(line)

    # 2. Атрибуты, которые реально видит пользователь/скринридер.
    attr_patterns = [
        r'(?:placeholder|aria-label|title)\s*=\s*"([^"]+)"',
        r"(?:placeholder|aria-label|title)\s*=\s*'([^']+)'",
    ]

    for pattern in attr_patterns:
        for match in re.finditer(pattern, text, flags=re.I):
            value = clean_fragment(match.group(1))

            if looks_like_real_ui_text(value):
                results.append(value)

    # 3. Vue :placeholder / :title / :aria-label со строковым fallback.
    dynamic_attr_pattern = re.compile(
        r":(?:placeholder|aria-label|title)\s*=\s*['\"]([^'\"]*[\u0400-\u04FF][^'\"]*)['\"]",
        flags=re.I,
    )

    for match in dynamic_attr_pattern.finditer(text):
        value = clean_fragment(match.group(1))

        if looks_like_real_ui_text(value):
            results.append(value)

    return results


def extract_js_user_strings(text: str) -> list[str]:
    results = []

    # Строки в JS.
    patterns = [
        r"'([^'\n]*[А-Яа-яЁё][^'\n]*)'",
        r'"([^"\n]*[А-Яа-яЁё][^"\n]*)"',
        r"`([^`\n]*[А-Яа-яЁё][^`\n]*)`",
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, text):
            value = clean_fragment(match.group(1))

            if looks_like_real_ui_text(value):
                results.append(value)

    return results


def load_backend_translations():
    if not TRANSLATIONS_FILE.exists():
        return {}

    source = TRANSLATIONS_FILE.read_text(encoding="utf-8")

    tree = ast.parse(source)

    translations = None

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "TRANSLATIONS":
                    translations = ast.literal_eval(node.value)

    if not isinstance(translations, dict):
        return {}

    return translations


def build_backend_reverse_map(translations):
    result = {}

    ru = translations.get("ru", {})

    if not isinstance(ru, dict):
        return result

    for key, value in ru.items():
        if isinstance(value, str):
            result[clean_fragment(value)] = key

    return result


def scan_frontend():
    files = []
    all_fragments = []
    files_with_russian = []

    for path in sorted(SRC_ROOT.rglob("*")):
        if not path.is_file():
            continue

        if not should_scan(path):
            continue

        files.append(path)

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        clean_text = strip_comments(text)

        fragments = []

        if path.suffix == ".vue":
            fragments.extend(extract_vue_visible_text(clean_text))

        fragments.extend(extract_js_user_strings(clean_text))

        fragments = [
            clean_fragment(x)
            for x in fragments
            if looks_like_real_ui_text(x)
        ]

        if fragments:
            files_with_russian.append(path)
            all_fragments.extend(
                (path.relative_to(FRONTEND_ROOT).as_posix(), fragment)
                for fragment in fragments
            )

    return files, files_with_russian, all_fragments


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--export-backend",
        action="store_true",
        help="Export clean translation inventory JSON",
    )

    args = parser.parse_args()

    translations = load_backend_translations()
    reverse_map = build_backend_reverse_map(translations)

    files, files_with_russian, fragments = scan_frontend()

    counter = Counter(fragment for _, fragment in fragments)

    found = []
    missing = []

    for fragment, count in counter.most_common():
        backend_key = reverse_map.get(fragment)

        item = {
            "text": fragment,
            "count": count,
            "backend_key": backend_key,
            "files": sorted({
                file
                for file, text in fragments
                if text == fragment
            }),
        }

        if backend_key:
            found.append(item)
        else:
            missing.append(item)

    languages = {
        lang: len(translations.get(lang, {}))
        for lang in ("ru", "uz", "en", "zh")
    }

    print()
    print("=" * 72)
    print("  EMERALD SERVICE — RUSSIAN UI AUDIT v2")
    print("=" * 72)
    print()

    print(f"Файлов просканировано:       {len(files)}")
    print(f"Файлов с UI-текстом:         {len(files_with_russian)}")
    print(f"Уникальных UI-фраз:          {len(counter)}")
    print(f"Уже есть в backend:          {len(found)}")
    print(f"Нужно добавить:              {len(missing)}")
    print()

    print("BACKEND TRANSLATIONS")
    print("-" * 72)

    for lang, count in languages.items():
        print(f"{lang.upper():<8}: {count}")

    print()

    print("УЖЕ ЕСТЬ В BACKEND")
    print("-" * 72)

    for item in found:
        print(
            f"[OK] {item['backend_key']}: "
            f"{item['text']}"
        )

    print()

    print("НУЖНО ДОБАВИТЬ")
    print("-" * 72)

    for index, item in enumerate(missing, 1):
        print(
            f"{index:03d}. {item['text']}"
        )

        for file in item["files"]:
            print(f"      └─ {file}")

    print()

    inventory = {
        "generated_by": "audit_russian.py v2",
        "frontend_root": str(FRONTEND_ROOT),
        "backend_translation_file": str(TRANSLATIONS_FILE),
        "backend_languages": languages,
        "summary": {
            "files_scanned": len(files),
            "files_with_ui_text": len(files_with_russian),
            "unique_ui_phrases": len(counter),
            "already_in_backend": len(found),
            "missing_in_backend": len(missing),
        },
        "existing": found,
        "missing": missing,
    }

    if args.export_backend:
        INVENTORY_FILE.write_text(
            json.dumps(
                inventory,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        print("=" * 72)
        print("Создан файл:")
        print(INVENTORY_FILE)
        print()
        print("Backend НЕ изменён.")
        print("=" * 72)
        print()


if __name__ == "__main__":
    main()
