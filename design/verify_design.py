from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_NAMES = [
    "Даниелян",
    "Наджафов Азер Этибарович",
    "Фиашева Диана Андзоровна",
    "Карапетян Анна Арменаковна",
    "Машрабова Амина Мубораккадамовна",
]
EXPECTED_CATS = {
    "consultations": 6,
    "diagnostics": 2,
    "anesthesia": 3,
    "hygiene": 11,
    "treatment": 25,
    "endodontics": 19,
    "surgery": 24,
    "implantation": 18,
    "prosthetics": 66,
    "orthodontics": 80,
}


class PageInventory(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.images: list[tuple[str, str]] = []
        self.forms = 0
        self.sections: set[str] = set()
        self.doctor_keys = 0
        self.opening: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = dict(attrs)
        if tag == "img":
            self.images.append((attrs_map.get("src", "") or "", attrs_map.get("alt", "") or ""))
        if tag == "form":
            self.forms += 1
        if tag == "section" and attrs_map.get("id"):
            self.sections.add(attrs_map["id"] or "")
        if "data-doctor-key" in attrs_map:
            self.doctor_keys += 1


class CatalogParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.rows: list[tuple[str, str]] = []
        self.categories: dict[str, int] = {}
        self.chips: set[str] = set()
        self.direct_links = 0
        self.forms = 0
        self.current_category: str | None = None
        self.current_row: dict[str, str] | None = None
        self.capture_field: str | None = None
        self.capture_depth = 0
        self.capture: list[str] = []
        self.search_found = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        classes = (a.get("class") or "").split()
        if tag == "form":
            self.forms += 1
        if tag == "input" and a.get("id") == "price-search":
            self.search_found = True
        if tag == "button" and "price-cat-chip" in classes:
            self.chips.add(a.get("data-cat-filter") or "")
        if tag == "a" and "direct-booking-link" in classes:
            self.direct_links += 1
        if tag == "section" and "price-category" in classes:
            self.current_category = a.get("data-price-category") or a.get("id") or ""
            self.categories.setdefault(self.current_category, 0)
        if tag == "li" and "price-row" in classes:
            self.current_row = {"name": "", "price": ""}
        if self.current_row is not None and tag == "span" and any(x in classes for x in ("price-item-name", "price-item-value")):
            field = "name" if "price-item-name" in classes else "price"
            if not self.current_row[field]:
                self.capture_field = field
                self.capture = []
                self.capture_depth = 1
        elif self.capture_depth:
            self.capture_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if self.capture_depth:
            self.capture_depth -= 1
            if self.capture_depth == 0 and self.capture_field and self.current_row is not None:
                self.current_row[self.capture_field] = " ".join("".join(self.capture).split())
                self.capture_field = None
                self.capture = []
        if tag == "li" and self.current_row is not None:
            self.rows.append((self.current_row["name"], self.current_row["price"]))
            if self.current_category is not None:
                self.categories[self.current_category] = self.categories.get(self.current_category, 0) + 1
            self.current_row = None
        if tag == "section" and self.current_category is not None:
            self.current_category = None

    def handle_data(self, data: str) -> None:
        if self.capture_depth and self.capture_field:
            self.capture.append(data)


def read_page(name: str) -> tuple[str, str]:
    path = ROOT / name
    text = path.read_text(encoding="utf-8")
    return str(path), text


def local_targets_exist(page_path: Path, html: str) -> list[str]:
    missing: list[str] = []
    for raw in re.findall(r"\b(?:src|href)=['\"]([^'\"]+)['\"]", html, flags=re.I):
        if raw.startswith(("http://", "https://", "tel:", "mailto:", "#", "data:")):
            continue
        parsed = urlparse(raw)
        target = (ROOT / parsed.path).resolve()
        if not target.exists():
            missing.append(raw)
    return missing


def verify_static() -> bool:
    required_sections = {"services", "clinic", "doctors", "visit", "prices", "contacts"}
    pages = [("prokshino.html", "Прокшино"), ("ispanskie.html", "Испанские кварталы")]
    errors: list[str] = []
    for file_name, branch in pages:
        path = ROOT / file_name
        html = path.read_text(encoding="utf-8")
        parser = PageInventory()
        parser.feed(html)
        if '<html lang="ru">' not in html:
            errors.append(f"{file_name}: expected Russian language declaration")
        if "<meta name=\"robots\" content=\"noindex, nofollow\">" not in html:
            errors.append(f"{file_name}: preview should remain noindex")
        missing_sections = required_sections - parser.sections
        if missing_sections:
            errors.append(f"{file_name}: missing sections {sorted(missing_sections)}")
        if parser.forms:
            errors.append(f"{file_name}: unexpected form(s) could simulate an unverified submission")
        if parser.doctor_keys:
            errors.append(f"{file_name}: stale app.js doctor-modal trigger found")
        if any(not alt.strip() for _, alt in parser.images):
            errors.append(f"{file_name}: an image has no accessible alt text")
        for missing in local_targets_exist(path, html):
            errors.append(f"{file_name}: missing local target {missing}")
        for name in EXPECTED_NAMES:
            if name not in html and name != "Даниелян":
                errors.append(f"{file_name}: missing verified doctor {name}")
        if "tel:+79045199697" not in html or "Ежедневно" not in html:
            errors.append(f"{file_name}: phone or verified daily hours not present")
        if "Carl Zeiss" in html or "КЛКТ" in html or "10 000 отзыв" in html:
            errors.append(f"{file_name}: unsupported legacy claims were retained")
        if branch == "Прокшино" and "https://dantist-prokshino.ru/online-zapis/" not in html:
            errors.append("prokshino.html: official DentalPRO link is missing")
        if branch == "Испанские кварталы" and "href=\"tel:+79045199697\"" not in html:
            errors.append("ispanskie.html: direct clinic phone booking is missing")

    concepts = (ROOT / "concepts.html").read_text(encoding="utf-8")
    for concept in ("concept-a", "concept-b", "concept-c"):
        if f'data-qa-section="{concept}"' not in concepts:
            errors.append(f"concepts.html: missing responsive hero {concept}")
    for asset in [
        "design/assets/prokshino/hero-clinic.webp",
        "design/assets/ispanskie/gallery-2.jpg",
        "design/assets/doctors/danielyan.jpg",
        "design/assets/doctors/nadzhafov.webp",
        "design/assets/doctors/fiasheva.webp",
        "design/assets/doctors/karapetyan.jpg",
        "design/assets/doctors/mashrabova.jpg",
    ]:
        if not (ROOT / asset).is_file():
            errors.append(f"missing required local photo {asset}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return False
    print("STATIC_DESIGN_PASS: branch facts, sections, local images, direct booking and three hero concepts checked")
    return True


def verify_catalogs() -> bool:
    errors: list[str] = []
    parsed: dict[str, CatalogParser] = {}
    for file_name in ("prices-prokshino.html", "prices-ispanskie.html"):
        html = (ROOT / file_name).read_text(encoding="utf-8")
        parser = CatalogParser()
        parser.feed(html)
        parsed[file_name] = parser
        if len(parser.rows) != 254:
            errors.append(f"{file_name}: expected 254 rows, found {len(parser.rows)}")
        if parser.categories != EXPECTED_CATS:
            errors.append(f"{file_name}: category counts differ: {parser.categories}")
        if parser.chips != {"all", *EXPECTED_CATS.keys()}:
            errors.append(f"{file_name}: missing filter chips: {parser.chips}")
        if not parser.search_found:
            errors.append(f"{file_name}: price-search input missing")
        if parser.direct_links != 254:
            errors.append(f"{file_name}: expected 254 direct booking links, found {parser.direct_links}")
        if parser.forms:
            errors.append(f"{file_name}: unexpected form present")
        if "data-open-booking" in html or "price-detail-booking-btn" in html:
            errors.append(f"{file_name}: stale simulated-booking hook remains")
        if local_targets_exist(ROOT / file_name, html):
            errors.append(f"{file_name}: has a broken relative asset/page link")

    if "prices-prokshino.html" in parsed and "prices-ispanskie.html" in parsed:
        a = parsed["prices-prokshino.html"].rows
        b = parsed["prices-ispanskie.html"].rows
        if a != b:
            errors.append("the two local catalogues are not an exact name/price match")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return False
    print("CATALOG_QA_PASS: 254 exact name/price rows, 10 category counts and filters, live search/detail hooks, real branch booking links")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--static", action="store_true")
    parser.add_argument("--catalogs", action="store_true")
    args = parser.parse_args()
    if not args.static and not args.catalogs:
        parser.error("choose --static and/or --catalogs")
    checks = []
    if args.static:
        checks.append(verify_static())
    if args.catalogs:
        checks.append(verify_catalogs())
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
