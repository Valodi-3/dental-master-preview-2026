from __future__ import annotations

import argparse
import json
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from playwright.sync_api import Browser, Page, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "design" / "qa"
SCREENSHOTS = OUT / "screenshots"
WIDTHS = [320, 360, 375, 390, 430, 768, 1024, 1440, 1920]
CAPTURE_WIDTHS = (390, 1440)
PAGES = {
    "prokshino": "prokshino.html",
    "ispanskie": "ispanskie.html",
}
CATALOGS = {
    "prokshino": "prices-prokshino.html",
    "ispanskie": "prices-ispanskie.html",
}
OLD_REFERENCE = {
    "prokshino": "https://valodi-3.github.io/dental-master-preview-2026/prokshino.html",
    "ispanskie": "https://valodi-3.github.io/dental-master-preview-2026/ispanskie.html",
}


class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, directory: str | None = None, **kwargs: Any) -> None:
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, format: str, *args: Any) -> None:
        pass


def local_server() -> tuple[ThreadingHTTPServer, str]:
    handler = lambda *args, **kwargs: QuietHandler(*args, directory=str(ROOT), **kwargs)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, f"http://127.0.0.1:{server.server_port}/"


def page_errors(page: Page, errors: list[str], label: str) -> None:
    page.on("pageerror", lambda exc: errors.append(f"{label}: {exc}"))


def load_local(page: Page, base_url: str, route: str, label: str, errors: list[str]) -> None:
    page_errors(page, errors, label)
    response = page.goto(urljoin(base_url, route), wait_until="load", timeout=45000)
    if response is None or response.status >= 400:
        raise RuntimeError(f"could not load {route}: status={response.status if response else 'no response'}")
    page.evaluate("""async () => {
      await Promise.all(Array.from(document.images, image => {
        image.loading = 'eager';
        return image.decode().catch(() => null);
      }));
    }""")


def measure_layout(page: Page) -> dict[str, Any]:
    return page.evaluate("""() => {
      const width = window.innerWidth;
      const htmlWidth = document.documentElement.scrollWidth;
      const bodyWidth = document.body.scrollWidth;
      const bad = [];
      for (const el of document.querySelectorAll('body *')) {
        const style = getComputedStyle(el);
        if (style.display === 'none' || style.visibility === 'hidden' || Number(style.opacity) === 0) continue;
        const r = el.getBoundingClientRect();
        if (r.width <= 0 || r.height <= 0) continue;
        if (r.left < -1.5 || r.right > width + 1.5) {
          const text = (el.innerText || el.getAttribute('aria-label') || '').trim().replace(/\\s+/g, ' ').slice(0, 72);
          bad.push({tag: el.tagName.toLowerCase(), className: typeof el.className === 'string' ? el.className : '', text, left: Math.round(r.left*10)/10, right: Math.round(r.right*10)/10, width: Math.round(r.width*10)/10});
          if (bad.length >= 20) break;
        }
      }
      const sections = Array.from(document.querySelectorAll('[data-qa-section]')).map(el => {
        const r = el.getBoundingClientRect();
        return {name: el.getAttribute('data-qa-section'), left: Math.round(r.left*10)/10, right: Math.round(r.right*10)/10, width: Math.round(r.width*10)/10};
      });
      const brokenImages = Array.from(document.images).filter(img => img.complete && img.naturalWidth === 0).map(img => img.getAttribute('src'));
      return {viewport: width, htmlScrollWidth: htmlWidth, bodyScrollWidth: bodyWidth, pageHeight: document.documentElement.scrollHeight, overflow: Math.max(htmlWidth,bodyWidth) > width + 1, outOfBounds: bad, sections, brokenImages};
    }""")


def set_viewport(page: Page, width: int) -> None:
    page.set_viewport_size({"width": width, "height": 900})
    page.emulate_media(reduced_motion="reduce")


def screenshot_sections(page: Page, prefix: str) -> list[str]:
    saved: list[str] = []
    sections = page.locator("[data-qa-section]")
    for index in range(sections.count()):
        section = sections.nth(index)
        name = section.get_attribute("data-qa-section") or f"section-{index+1}"
        target = SCREENSHOTS / f"{prefix}_{name}.png"
        section.screenshot(path=str(target), animations="disabled", timeout=30000)
        saved.append(str(target.relative_to(ROOT)))
    return saved


def test_mobile_menu(page: Page, base_url: str, route: str, label: str, errors: list[str], width: int) -> None:
    set_viewport(page, width)
    load_local(page, base_url, route, f"menu-{label}-{width}", errors)
    toggle = page.locator("#menu-toggle")
    nav = page.locator("#mobile-nav")
    toggle.click()
    page.wait_for_timeout(80)
    state = nav.evaluate("el => ({display:getComputedStyle(el).display, aria:el.getAttribute('aria-hidden'), expanded:document.querySelector('#menu-toggle').getAttribute('aria-expanded'), right:el.getBoundingClientRect().right, bottom:el.getBoundingClientRect().bottom})")
    if state["display"] == "none" or state["aria"] != "false" or state["expanded"] != "true" or state["right"] > width + 1 or state["bottom"] > page.viewport_size["height"] + 1:
        errors.append(f"menu-{label}-{width}: mobile nav did not open within viewport: {state}")
    page.keyboard.press("Escape")
    page.wait_for_timeout(50)
    if nav.get_attribute("aria-hidden") != "true":
        errors.append(f"menu-{label}-{width}: Escape did not close mobile nav")


def test_catalog(page: Page, base_url: str, route: str, label: str, errors: list[str]) -> None:
    set_viewport(page, 390)
    load_local(page, base_url, route, f"catalog-{label}", errors)
    if page.locator(".price-row").count() != 254:
        errors.append(f"catalog-{label}: expected 254 DOM rows")
    count = page.locator("#price-catalog-count")
    page.wait_for_timeout(100)
    if "254" not in count.inner_text():
        errors.append(f"catalog-{label}: initial visible count is not 254: {count.inner_text()}")

    page.locator('[data-cat-filter="implantation"]').click()
    page.wait_for_timeout(80)
    if "18" not in count.inner_text():
        errors.append(f"catalog-{label}: implantation filter should show 18: {count.inner_text()}")

    search = page.locator("#price-search")
    search.fill("брекет")
    page.wait_for_timeout(80)
    if "0" not in count.inner_text():
        errors.append(f"catalog-{label}: category and search should intersect to zero: {count.inner_text()}")
    if not page.locator("#price-catalog-empty").is_visible():
        errors.append(f"catalog-{label}: empty-result message did not appear")

    search.fill("")
    page.locator('[data-cat-filter="all"]').click()
    page.wait_for_timeout(80)
    if "254" not in count.inner_text():
        errors.append(f"catalog-{label}: reset did not restore all 254 rows: {count.inner_text()}")

    search.fill("Osstem")
    page.wait_for_timeout(80)
    search_count = int("".join(ch for ch in count.inner_text() if ch.isdigit()) or "0")
    if not 0 < search_count < 254:
        errors.append(f"catalog-{label}: Osstem search result count is implausible: {count.inner_text()}")
    search.fill("")
    page.wait_for_timeout(60)

    first_row = page.locator(".price-row:visible").first
    trigger = first_row.locator("[data-price-toggle]")
    detail = first_row.locator("[data-price-detail]")
    trigger.click()
    if trigger.get_attribute("aria-expanded") != "true" or detail.get_attribute("hidden") is not None:
        errors.append(f"catalog-{label}: price-detail accordion did not open")
    trigger.click()
    if trigger.get_attribute("aria-expanded") != "false" or detail.get_attribute("hidden") is None:
        errors.append(f"catalog-{label}: price-detail accordion did not close")

    links = page.locator(".direct-booking-link")
    if links.count() != 254 or not links.first.get_attribute("href"):
        errors.append(f"catalog-{label}: direct per-service booking links are missing")


def capture_old_reference(browser: Browser, label: str, url: str, errors: list[str]) -> str | None:
    page = browser.new_page(viewport={"width": 390, "height": 900})
    page_errors(page, errors, f"old-reference-{label}")
    try:
        response = page.goto(url, wait_until="domcontentloaded", timeout=45000)
        if response is None or response.status >= 400:
            raise RuntimeError(f"HTTP {response.status if response else 'no response'}")
        page.wait_for_timeout(1600)
        screenshot = SCREENSHOTS / f"old_{label}_mobile_390.png"
        page.screenshot(path=str(screenshot), full_page=False, animations="disabled", timeout=30000)
        page.set_viewport_size({"width": 1440, "height": 900})
        page.wait_for_timeout(400)
        screenshot_desktop = SCREENSHOTS / f"old_{label}_desktop_1440.png"
        page.screenshot(path=str(screenshot_desktop), full_page=False, animations="disabled", timeout=30000)
        return f"captured: {screenshot.name}, {screenshot_desktop.name}"
    except Exception as exc:  # Public reference capture is supplemental to local acceptance gates.
        print(f"OLD_REFERENCE_WARNING {label}: {exc}")
        return None
    finally:
        page.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Responsive and interaction QA for the two clinic previews")
    parser.add_argument("--all", action="store_true", help="run all responsive, interaction and screenshot checks")
    parser.add_argument("--skip-old-reference", action="store_true", help="skip optional screenshots of the currently published preview")
    args = parser.parse_args()
    if not args.all:
        parser.error("choose --all")

    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    metrics: dict[str, Any] = {"viewports": WIDTHS, "pages": {}, "catalogs": {}, "old_reference": {}}
    server, base_url = local_server()
    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(channel="msedge", headless=True)
            except Exception:
                browser = p.chromium.launch(headless=True)
            try:
                for label, route in PAGES.items():
                    page = browser.new_page(viewport={"width": WIDTHS[0], "height": 900}, device_scale_factor=1)
                    all_metrics: list[dict[str, Any]] = []
                    for width in WIDTHS:
                        set_viewport(page, width)
                        load_local(page, base_url, route, f"{label}-{width}", failures)
                        data = measure_layout(page)
                        all_metrics.append(data)
                        if data["overflow"]:
                            failures.append(f"{label}@{width}: document horizontal scrollWidth {max(data['htmlScrollWidth'], data['bodyScrollWidth'])} exceeds viewport")
                        if data["outOfBounds"]:
                            failures.append(f"{label}@{width}: visible element extends beyond viewport: {data['outOfBounds'][:4]}")
                        if data["brokenImages"]:
                            failures.append(f"{label}@{width}: broken image(s): {data['brokenImages']}")
                        for section in data["sections"]:
                            if section["left"] < -1.5 or section["right"] > width + 1.5:
                                failures.append(f"{label}@{width}: {section['name']} section out of bounds: {section}")

                        if width in CAPTURE_WIDTHS:
                            page.screenshot(path=str(SCREENSHOTS / f"{label}_{'mobile' if width == 390 else 'desktop'}_{width}_full.png"), full_page=True, animations="disabled", timeout=60000)
                            page.screenshot(path=str(SCREENSHOTS / f"{label}_{'mobile' if width == 390 else 'desktop'}_{width}_top.png"), full_page=False, animations="disabled", timeout=30000)
                            saved = screenshot_sections(page, f"{label}_{'mobile' if width == 390 else 'desktop'}_{width}")
                            metrics.setdefault("section_screenshots", []).extend(saved)
                    metrics["pages"][label] = all_metrics
                    page.close()

                for label, route in CATALOGS.items():
                    page = browser.new_page(viewport={"width": 390, "height": 900}, device_scale_factor=1)
                    test_catalog(page, base_url, route, label, failures)
                    for width in WIDTHS:
                        set_viewport(page, width)
                        load_local(page, base_url, route, f"catalog-shot-{label}-{width}", failures)
                        data = measure_layout(page)
                        if data["overflow"] or data["outOfBounds"]:
                            failures.append(f"catalog-{label}@{width}: viewport bounds failure {data['outOfBounds'][:4]}")
                        if width in CAPTURE_WIDTHS:
                            page.screenshot(path=str(SCREENSHOTS / f"catalog_{label}_{'mobile' if width == 390 else 'desktop'}_{width}_top.png"), full_page=False, animations="disabled", timeout=30000)
                        if not metrics["catalogs"].get(label):
                            metrics["catalogs"][label] = []
                        metrics["catalogs"][label].append({"viewport": width, "scrollWidth": data["htmlScrollWidth"], "pageHeight": data["pageHeight"], "overflow": data["overflow"]})
                    page.close()

                for label, route in PAGES.items():
                    page = browser.new_page(viewport={"width": 390, "height": 900})
                    for width in (320, 360, 375, 390, 430):
                        test_mobile_menu(page, base_url, route, label, failures, width)
                    page.close()

                page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
                load_local(page, base_url, "concepts.html", "concepts", failures)
                for width in CAPTURE_WIDTHS:
                    set_viewport(page, width)
                    load_local(page, base_url, "concepts.html", f"concepts-{width}", failures)
                    data = measure_layout(page)
                    if data["overflow"] or data["outOfBounds"]:
                        failures.append(f"concepts@{width}: viewport bounds failure {data['outOfBounds'][:4]}")
                    if width in CAPTURE_WIDTHS:
                        screenshot_sections(page, f"concepts_{'mobile' if width == 390 else 'desktop'}_{width}")
                page.close()

                if not args.skip_old_reference:
                    for label, url in OLD_REFERENCE.items():
                        metrics["old_reference"][label] = capture_old_reference(browser, label, url, failures)
                browser.close()
            finally:
                try:
                    browser.close()
                except Exception:
                    pass
    finally:
        server.shutdown()
        server.server_close()

    report_path = OUT / "layout-metrics.json"
    report_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print(f"RESPONSIVE_QA_FAIL: see {report_path.relative_to(ROOT)}")
        return 1

    print(f"RESPONSIVE_QA_PASS: 9 widths {WIDTHS}; mobile menu, search/filter intersection, price accordions and {len(metrics.get('section_screenshots', []))} section screenshots checked")
    print(f"EVIDENCE: {report_path.relative_to(ROOT)}; screenshots={SCREENSHOTS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
