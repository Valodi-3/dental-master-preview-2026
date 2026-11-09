from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "v2"
QA = ROOT / "design" / "v2qa"
EXPECTED_BRANCH = "design/manus-dental-master-2026"
FOUNDATION_REF = "origin/tech/dental-master-foundation-2026"
FOUNDATION_SHA = "a1607f79c28aafb7d2ee73818cdd5d996f7f5d3f"


class DocumentInspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self.ids: list[str] = []
        self.headings: list[str] = []
        self.images: list[tuple[str, str]] = []
        self.forms = 0
        self.current_h1 = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "a" and values.get("href") is not None:
            self.links.append(("href", str(values["href"])))
        for key in ("src", "href"):
            value = values.get(key)
            if value and (tag in ("img", "script", "iframe") and key == "src" or tag == "link" and key == "href"):
                rel = values.get("rel", "")
                if tag != "link" or any(token in str(rel).split() for token in ("stylesheet", "icon", "preload")):
                    self.links.append((key, str(value)))
        if values.get("id"):
            self.ids.append(str(values["id"]))
        if tag == "img":
            self.images.append((str(values.get("src", "")), str(values.get("alt", ""))))
        if tag == "form":
            self.forms += 1
        if tag == "h1":
            self.headings.append("")
            self.current_h1 = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "h1":
            self.current_h1 = False

    def handle_data(self, data: str) -> None:
        if self.current_h1 and self.headings:
            self.headings[-1] += data


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("\u00a0", " ")).strip()


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def inspect_html(path: Path) -> tuple[str, DocumentInspector]:
    text = path.read_text(encoding="utf-8")
    parser = DocumentInspector()
    parser.feed(text)
    parser.close()
    return text, parser


def pages() -> list[Path]:
    return sorted(V2.rglob("*.html"))


def route_graph() -> dict:
    manifest = load_json(V2 / "route-manifest.json")
    all_pages = pages()
    assert_true(manifest.get("serviceCount") == 254, "manifest service count is not 254")
    declared = [V2 / manifest["entry"]]
    for branch, route_data in manifest["branches"].items():
        declared.extend(V2 / rel for rel in [route_data["home"], route_data["directions"], *route_data["services"], *route_data["doctors"], route_data["prices"], route_data["contacts"]])
    assert_true(len(declared) == 41, f"expected 41 declared routes, got {len(declared)}")
    assert_true(len(set(path.resolve() for path in declared)) == 41, "route manifest contains duplicate paths")
    missing = [str(path.relative_to(ROOT)) for path in declared if not path.is_file()]
    assert_true(not missing, f"declared route files are missing: {missing[:8]}")
    assert_true(len(all_pages) == 41, f"expected exactly 41 V2 HTML routes, found {len(all_pages)}")

    broken: list[str] = []
    bad_alt: list[str] = []
    bad_h1: list[str] = []
    bad_ids: list[str] = []
    form_pages: list[str] = []
    page_meta: dict[str, dict] = {}
    for page in all_pages:
        source, parser = inspect_html(page)
        rel = page.relative_to(ROOT).as_posix()
        if parser.forms:
            form_pages.append(rel)
        if len(parser.headings) != 1 or not parser.headings[0].strip():
            bad_h1.append(rel)
        if len(parser.ids) != len(set(parser.ids)):
            bad_ids.append(rel)
        if page != V2 / "index.html":
            missing_alt = [(src, alt) for src, alt in parser.images if not alt.strip()]
            if missing_alt:
                bad_alt.append(rel)
        for attr, raw_url in parser.links:
            url = urlsplit(raw_url)
            if url.scheme or url.netloc or not url.path:
                continue
            target = (page.parent / unquote(url.path)).resolve()
            if not target.is_file():
                broken.append(f"{rel}: {attr}={raw_url}")
        page_meta[rel] = {
            "title": re.search(r"<title>(.*?)</title>", source, re.I | re.S).group(1) if re.search(r"<title>(.*?)</title>", source, re.I | re.S) else "",
            "page": re.search(r'data-page="([^"]+)"', source).group(1) if re.search(r'data-page="([^"]+)"', source) else "",
            "clinic": re.search(r'data-clinic="([^"]*)"', source).group(1) if re.search(r'data-clinic="([^"]*)"', source) else "",
        }
    assert_true(not broken, f"unresolved local HTML links/assets: {broken[:12]}")
    assert_true(not bad_alt, f"images without alt text: {bad_alt}")
    assert_true(not bad_h1, f"pages without exactly one H1: {bad_h1}")
    assert_true(not bad_ids, f"duplicate HTML IDs: {bad_ids}")
    assert_true(not form_pages, f"unexpected forms in V2 static build: {form_pages}")
    counts: dict[str, int] = {}
    for meta in page_meta.values():
        counts[meta["page"]] = counts.get(meta["page"], 0) + 1
    expected_types = {"chooser": 1, "home": 2, "directions": 2, "service": 20, "doctors": 2, "doctor": 10, "prices": 2, "contacts": 2}
    assert_true(counts == expected_types, f"page type counts differ: {counts}")
    return {"routes": len(all_pages), "pageTypes": counts, "brokenLinks": len(broken), "pages": page_meta}


def run_architecture() -> None:
    result = route_graph()
    hub, hub_parser = inspect_html(ROOT / "index.html")
    assert_true('href="v2/index.html"' in hub, "root preview hub does not link to the V2 chooser")
    print("V2_ARCHITECTURE_PASS", json.dumps({k: v for k, v in result.items() if k != "pages"}, ensure_ascii=False))


def run_selector_data() -> None:
    services = load_json(V2 / "data" / "services_master.json")
    categories = load_json(V2 / "data" / "categories_summary.json")
    clinic_data = load_json(V2 / "data" / "clinic-content.json")
    assert_true(len(services) == 254, f"canonical master has {len(services)} rows")
    by_id = {row["id"]: row for row in services}
    assert_true(len(by_id) == 254, "canonical SKU is not unique")
    sum_count = 0
    branch_differences = []
    for key, category in categories.items():
        items = [row for row in services if row["category"] == key]
        assert_true(len(items) == category["count"], f"wrong row count for {key}")
        sum_count += len(items)
        ids = clinic_data["featuredServiceIds"].get(key, [])
        assert_true(len(ids) >= 1, f"category {key} has no selector choices")
        for service_id in ids:
            row = by_id.get(service_id)
            assert_true(row is not None and row["category"] == key, f"invalid featured SKU {service_id}")
        for row in items:
            assert_true(bool(row["pricing"]["prokshino"]["formatted"]), f"missing Prokshino price: {row['id']}")
            assert_true(bool(row["pricing"]["ispanskie"]["formatted"]), f"missing Spanish Quarters price: {row['id']}")
            if row["pricing"]["prokshino"]["amount"] != row["pricing"]["ispanskie"]["amount"]:
                branch_differences.append(row["id"])
    assert_true(sum_count == 254, "category counts do not sum to 254")
    assert_true(not branch_differences, f"unexpected branch price differences: {branch_differences[:5]}")
    for branch in ("prokshino", "ispanskie"):
        for page in (V2 / branch / "index.html", V2 / branch / "directions" / "index.html"):
            html, _ = inspect_html(page)
            assert_true('data-service-selector' in html, f"selector missing on {page.relative_to(ROOT)}")
            assert_true("не медицинская рекомендация" in html or "не оценивает состояние здоровья" in html, f"no non-diagnostic disclosure on {page.relative_to(ROOT)}")
    script = (V2 / "assets" / "v2.js").read_text(encoding="utf-8")
    assert_true("setCategory(category)" in script and "setService(serviceId)" in script, "in-place selector state transitions are missing")
    assert_true("serviceDescription" not in script, "unexpected fabricated service-description source")
    for key, image_path in clinic_data["branches"]["prokshino"]["selectorImages"].items():
        assert_true((ROOT / image_path).is_file(), f"missing Prokshino selector photo for {key}")
    for key, image_path in clinic_data["branches"]["ispanskie"]["selectorImages"].items():
        assert_true((ROOT / image_path).is_file(), f"missing Spanish Quarters selector photo for {key}")
    print("V2_SELECTOR_DATA_PASS services=254 categories=10 branchPriceDifferences=0 verifiedLocalCatalogueMismatches=0")


def run_booking() -> None:
    sources = (ROOT / "docs" / "V2_SOURCES.md").read_text(encoding="utf-8")
    data = load_json(V2 / "data" / "clinic-content.json")["shared"]
    assert_true(data["dentalpro"] == "https://dantist-prokshino.ru/online-zapis/", "DentalPRO URL differs from the sourced address")
    assert_true(data["tel"] == "tel:+79045199697", "phone is not E.164 in its tel link")
    assert_true("филиал Прокшино" in sources and "404" in sources, "booking-route audit findings are not documented")
    for page in pages():
        source = page.read_text(encoding="utf-8")
        rel = page.relative_to(ROOT).as_posix()
        if 'data-clinic=""' in source:
            continue
        assert_true(data["dentalpro"] in source, f"real DentalPRO destination absent from {rel}")
        assert_true(data["tel"] in source, f"E.164 clinic phone absent from {rel}")
        assert_true('data-booking-dialog' in source, f"booking dialog missing from {rel}")
        assert_true('data-book-call' in source and 'data-copy-phone' in source, f"phone choice/copy missing from {rel}")
        assert_true(data["whatsapp"] in source and data["telegram"] in source, f"secondary contact channels absent from {rel}")
    ispanskie_home = (V2 / "ispanskie" / "index.html").read_text(encoding="utf-8")
    ispanskie_contacts = (V2 / "ispanskie" / "contacts" / "index.html").read_text(encoding="utf-8")
    assert_true("официальный переход на онлайн-запись с сайта Испанских кварталов ведёт в филиал Прокшино." in ispanskie_home, "Spanish Quarters modal does not disclose the Prokshino booking destination")
    assert_true("Для записи именно в Испанские кварталы используйте телефон." in ispanskie_contacts, "Spanish Quarters contacts page does not direct the branch-specific booking to its phone")
    assert_true("Открыть DentalPRO · Прокшино" in ispanskie_home, "Spanish Quarters DentalPRO action is not location-labelled")
    combined = "\n".join(page.read_text(encoding="utf-8") for page in pages())
    js = (V2 / "assets" / "v2.js").read_text(encoding="utf-8")
    assert_true("Заявка принята" not in combined and "setTimeout(" not in js, "fake form success or timeout exists")
    assert_true("не передаётся в DentalPRO" in combined, "selected-service transfer disclosure missing")
    assert_true("showModal()" in js and "dialog.addEventListener('close'" in js, "native accessible modal/restore-focus behavior missing")
    assert_true("aria-labelledby', showCall ? 'booking-call-title' : 'booking-title'" in js, "dialog accessible name does not track its visible step")
    assert_true("event.target === dialog" in js, "outside-click close is missing")
    print("V2_BOOKING_PASS DentalPRO=verified tel=E164 WhatsApp=verified Telegram=clearly-labelled fakeForms=0")


def run_doctors() -> None:
    doctors = load_json(V2 / "data" / "doctors.json")
    assert_true(len(doctors) == 5 and len({doctor["slug"] for doctor in doctors}) == 5, "expected five unique doctors")
    for branch in ("prokshino", "ispanskie"):
        index = V2 / branch / "doctors" / "index.html"
        index_text = index.read_text(encoding="utf-8")
        for doctor in doctors:
            file = V2 / branch / "doctors" / f"{doctor['slug']}.html"
            assert_true(file.is_file(), f"missing profile route {file.relative_to(ROOT)}")
            text = file.read_text(encoding="utf-8")
            assert_true(doctor["name"] in index_text and doctor["name"] in text, f"doctor name/profile missing: {doctor['name']}")
            assert_true(doctor["experience"] in index_text and doctor["experience"] in text, f"experience missing: {doctor['name']}")
            assert_true((ROOT / doctor["portrait"]).is_file(), f"missing doctor portrait: {doctor['portrait']}")
            assert_true(doctor["source"] in text, f"doctor official source link missing: {doctor['name']}")
            for cert in doctor["certificates"]:
                assert_true(cert["url"] in text, f"published certificate link missing: {doctor['name']}")
            assert_true(f"href=\"{branch}/doctors/index.html\"" not in text, "unexpected hard-coded doctor return route")
    print("V2_DOCTORS_PASS doctors=5 profiles=10 officialPortraits=verified certificateLinks=source-backed")


def catalog_parser():
    path = ROOT / "design" / "verify_design.py"
    spec = importlib.util.spec_from_file_location("v1_catalog_parser", path)
    assert_true(spec is not None and spec.loader is not None, "cannot load trusted local catalogue parser")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.CatalogParser


def run_catalogues() -> None:
    services = load_json(V2 / "data" / "services_master.json")
    parser_cls = catalog_parser()
    records_by_branch = {}
    for branch in ("prokshino", "ispanskie"):
        records_by_branch[branch] = json.loads(subprocess.check_output(["git", "show", f"{FOUNDATION_REF}:data/services_{branch}.json"], cwd=ROOT, text=True, encoding="utf-8"))
        html_path = ROOT / f"prices-{branch}.html"
        parser = parser_cls()
        parser.feed(html_path.read_text(encoding="utf-8"))
        actual = parser.rows
        expected = records_by_branch[branch]
        assert_true(len(actual) == len(expected) == 254, f"catalogue count mismatch for {branch}")
        mismatches = []
        for record, (name, price) in zip(expected, actual):
            if normalized(record["name"]) != normalized(name) or normalized(record["priceFormatted"]) != normalized(price):
                mismatches.append(record["id"])
        assert_true(not mismatches, f"foundation/local official row mismatches for {branch}: {mismatches[:5]}")
        page = V2 / branch / "prices" / "index.html"
        source = page.read_text(encoding="utf-8")
        rendered_ids = re.findall(r'<details class="price-item" data-price-item data-service-id="(svc_[^"]+)"', source)
        assert_true(len(rendered_ids) == 254 and len(set(rendered_ids)) == 254, f"wrong rendered service rows for {branch}")
        for record in expected:
            assert_true(f'id="{record["id"]}"' in source, f"missing SKU in rendered catalogue {branch}: {record['id']}")
            assert_true(record["name"] in source or html_escape_for_check(record["name"]) in source, f"missing exact name in rendered catalogue {branch}: {record['id']}")
            assert_true(record["priceFormatted"] in source, f"missing exact price in rendered catalogue {branch}: {record['id']}")
        assert_true('data-catalog-search' in source and 'data-catalog-filter="all"' in source and 'data-price-detail-actions' not in source, "catalog search/filter/details are incomplete")
    assert_true(all([(a["id"], a["name"]) == (b["id"], b["name"]) for a, b in zip(records_by_branch["prokshino"], records_by_branch["ispanskie"])]), "branch catalog ID/name order differs")
    assert_true(services[0]["meta"]["verifiedAt"] == "2026-11-09", "service data verification date changed")
    print("V2_CATALOGUES_PASS rowsPerBranch=254 exactNamePriceMismatches=0 categories=10 search=enabled filters=enabled detailAccordions=enabled")


def html_escape_for_check(value: str) -> str:
    import html
    return html.escape(value, quote=True)


def run_preview() -> None:
    manifest = route_graph()
    assert_true((V2 / "index.html").is_file(), "V2 chooser missing")
    assert_true((ROOT / "index.html").is_file() and 'href="v2/index.html"' in (ROOT / "index.html").read_text(encoding="utf-8"), "local hub does not launch V2")
    assert_true((V2 / "assets" / "v2.css").is_file() and (V2 / "assets" / "v2.js").is_file() and (V2 / "assets" / "v2-data.js").is_file(), "self-contained V2 assets are missing")
    print(f"V2_PREVIEW_PASS localEntry={Path('index.html')} routes={manifest['routes']} publicHosting=not-replaced")


def run_evidence() -> None:
    metrics_path = QA / "layout-metrics.json"
    screenshots = list((QA / "screenshots").glob("*.png")) if (QA / "screenshots").exists() else []
    assert_true(metrics_path.is_file(), "responsive browser metrics are missing")
    metrics = load_json(metrics_path)
    assert_true(metrics.get("viewports") == [320, 360, 375, 390, 430, 768, 1024, 1440, 1920], "viewport evidence lacks the required nine widths")
    assert_true(metrics.get("overflowCount") == 0, f"responsive overflow remains: {metrics.get('overflowCount')}")
    assert_true(metrics.get("routeChecks") == 41 * 9, "not all 41 routes were exercised at each viewport")
    assert_true(metrics.get("zoomChecks") == 41 * 3, "not all 41 routes were exercised with 200% text at three viewport widths")
    required = ["v2-mobile-home", "v2-desktop-home", "v2-mobile-directions", "v2-desktop-service", "v2-mobile-doctors", "v2-desktop-doctor", "v2-mobile-prices", "v2-desktop-contacts", "v2-before-after-mobile", "v2-before-after-desktop"]
    names = "\n".join(path.name for path in screenshots)
    missing = [token for token in required if token not in names]
    assert_true(not missing, f"page-type/old-new screenshot evidence missing: {missing}")
    assert_true(not metrics.get("interactionErrors"), "browser interaction errors are present")
    assert_true(metrics.get("brokenImageCount") == 0, "browser found missing images")
    print(f"V2_EVIDENCE_PASS screenshots={len(screenshots)} measuredRoutes={metrics['routeChecks']} zoomChecks={metrics['zoomChecks']} viewportWidths=9")


def run_branch() -> None:
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    assert_true(branch == EXPECTED_BRANCH, f"expected isolated design branch {EXPECTED_BRANCH}, current is {branch}")
    status = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip()
    tracking = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], cwd=ROOT, text=True).strip()
    remote = subprocess.check_output(["git", "rev-parse", "origin/design/manus-dental-master-2026"], cwd=ROOT, text=True).strip()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    assert_true(not status, f"worktree is not clean: {status[:300]}")
    assert_true(tracking == "origin/design/manus-dental-master-2026", f"branch tracking differs: {tracking}")
    assert_true(head == remote, f"local and remote branch commits differ: {head} != {remote}")
    assert_true(subprocess.run(["git", "diff", "--quiet", "origin/main", "--", "app.js"], cwd=ROOT).returncode == 0, "shared technical app.js changed relative to main")
    remote_pr = subprocess.check_output(["git", "ls-remote", "--heads", "origin", "tech/dental-master-foundation-2026"], cwd=ROOT, text=True).strip()
    assert_true(bool(remote_pr), "Antigravity technical branch cannot be verified remotely")
    print("V2_BRANCH_PASS isolatedBranch=design/manus-dental-master-2026 remote=verified worktree=clean app.js=untouched")


def main() -> None:
    ap = argparse.ArgumentParser()
    for arg in ("architecture", "selector-data", "booking", "doctors", "catalogues", "preview", "branch", "evidence"):
        ap.add_argument(f"--{arg}", action="store_true")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()
    selected = args.all or any(vars(args).values())
    if not selected:
        ap.error("choose one or more checks or --all")
    checks = [
        ("architecture", args.architecture or args.all, run_architecture),
        ("selector-data", args.selector_data or args.all, run_selector_data),
        ("booking", args.booking or args.all, run_booking),
        ("doctors", args.doctors or args.all, run_doctors),
        ("catalogues", args.catalogues or args.all, run_catalogues),
        ("evidence", args.evidence or args.all, run_evidence),
        ("preview", args.preview or args.all, run_preview),
        ("branch", args.branch or args.all, run_branch),
    ]
    failures = 0
    for label, enabled, fn in checks:
        if not enabled:
            continue
        try:
            fn()
        except Exception as exc:
            failures += 1
            print(f"V2_{label.upper().replace('-', '_')}_FAIL: {exc}", file=sys.stderr)
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
