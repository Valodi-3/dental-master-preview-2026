from __future__ import annotations

import json
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlsplit

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "v2"
QA = ROOT / "design" / "v2qa"
SHOTS = QA / "screenshots"
WIDTHS = [320, 360, 375, 390, 430, 768, 1024, 1440, 1920]
ZOOM_WIDTHS = [320, 390, 1440]
HEIGHT = 900


class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args: Any, directory: str | None = None, **kwargs: Any) -> None:
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, fmt: str, *args: Any) -> None:
        pass


def start_server() -> tuple[ThreadingHTTPServer, str]:
    handler = lambda *args, **kwargs: QuietHandler(*args, directory=str(ROOT), **kwargs)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_port}/"


def read_manifest() -> dict:
    return json.loads((V2 / "route-manifest.json").read_text(encoding="utf-8"))


def route_list() -> list[tuple[str, str]]:
    manifest = read_manifest()
    routes = [("chooser", f"v2/{manifest['entry']}")]
    for branch, items in manifest["branches"].items():
        routes.append((f"home-{branch}", f"v2/{items['home']}"))
        routes.append((f"directions-{branch}", f"v2/{items['directions']}"))
        routes.extend((f"service-{branch}-{Path(item).stem}", f"v2/{item}") for item in items["services"])
        routes.append((f"doctors-{branch}", f"v2/{items['doctors'][0]}"))
        routes.extend((f"doctor-{branch}-{Path(item).stem}", f"v2/{item}") for item in items["doctors"][1:])
        routes.append((f"prices-{branch}", f"v2/{items['prices']}"))
        routes.append((f"contacts-{branch}", f"v2/{items['contacts']}"))
    return routes


def load(page: Page, base: str, route: str, label: str, errors: list[str]) -> None:
    if not getattr(page, "_v2_watchers_attached", False):
        page.on("pageerror", lambda exc: errors.append(f"{page.url}: pageerror: {exc}"))
        page.on("console", lambda msg: errors.append(f"{page.url}: console: {msg.text}") if msg.type == "error" else None)
        page.on("requestfailed", lambda request: errors.append(f"{page.url}: request failed: {request.url} {request.failure}"))
        page._v2_watchers_attached = True
    response = page.goto(urljoin(base, route), wait_until="load", timeout=45000)
    if response is None or response.status >= 400:
        raise RuntimeError(f"failed to load {route}: {response.status if response else 'no response'}")
    page.wait_for_function("window.DENTAL_V2 && document.readyState === 'complete'", timeout=15000)


def measure(page: Page, *, zoom: bool = False) -> dict[str, Any]:
    result = page.evaluate("""() => {
      const width = window.innerWidth;
      const htmlWidth = document.documentElement.scrollWidth;
      const bodyWidth = document.body.scrollWidth;
      const issues = [];
      const hasScrollOrClipParent = element => {
        let node = element.parentElement;
        while (node && node !== document.body) {
          const style = getComputedStyle(node);
          if (['auto','scroll','hidden','clip'].includes(style.overflowX)) return true;
          node = node.parentElement;
        }
        return false;
      };
      for (const el of document.querySelectorAll('body *')) {
        const style = getComputedStyle(el);
        if (style.display === 'none' || style.visibility === 'hidden' || Number(style.opacity) === 0) continue;
        const r = el.getBoundingClientRect();
        if (r.width <= 0 || r.height <= 0 || hasScrollOrClipParent(el)) continue;
        if (r.left < -1.5 || r.right > width + 1.5) {
          const text = (el.innerText || el.getAttribute('aria-label') || '').trim().replace(/\\s+/g,' ').slice(0,74);
          issues.push({tag:el.tagName.toLowerCase(),className:typeof el.className === 'string' ? el.className : '',text,left:Math.round(r.left*10)/10,right:Math.round(r.right*10)/10,width:Math.round(r.width*10)/10});
          if (issues.length >= 12) break;
        }
      }
      const brokenImages = Array.from(document.images).filter(image => image.complete && image.naturalWidth === 0).map(image => image.getAttribute('src'));
      return {viewport:width,htmlScrollWidth:htmlWidth,bodyScrollWidth:bodyWidth,pageHeight:document.documentElement.scrollHeight,overflow:Math.max(htmlWidth,bodyWidth)>width+1,outOfBounds:issues,brokenImages};
    }""")
    result["zoom"] = zoom
    return result


def route_matrix(browser: Browser, base: str, errors: list[str]) -> tuple[list[dict], int]:
    metrics: list[dict] = []
    checks = 0
    routes = route_list()
    page = browser.new_page(viewport={"width": 390, "height": HEIGHT})
    for width in WIDTHS:
        page.set_viewport_size({"width": width, "height": HEIGHT})
        page.emulate_media(reduced_motion="reduce")
        for route_name, route in routes:
            load(page, base, route, f"route-{route_name}-{width}", errors)
            item = measure(page)
            item.update({"route": route_name, "path": route})
            metrics.append(item)
            checks += 1
    page.close()

    # Root-relative font sizing at 200% exercises large text reflow while retaining
    # each physical test viewport. This intentionally scales rem/em typography,
    # labels, buttons and helper copy without applying a pinch-zoom-only transform.
    page = browser.new_page(viewport={"width": 320, "height": HEIGHT})
    for width in ZOOM_WIDTHS:
        page.set_viewport_size({"width": width, "height": HEIGHT})
        page.emulate_media(reduced_motion="reduce")
        for route_name, route in routes:
            load(page, base, route, f"zoom-{route_name}-{width}", errors)
            page.add_style_tag(content="html { font-size: 200% !important; }")
            item = measure(page, zoom=True)
            item.update({"route": route_name, "path": route})
            metrics.append(item)
            checks += 1
    page.close()
    return metrics, checks


def verify_selector(page: Page, base: str, branch: str, errors: list[str]) -> dict:
    route = f"v2/{branch}/index.html"
    load(page, base, route, f"selector-{branch}", errors)
    data = page.evaluate("window.DENTAL_V2")
    chosen = []
    for category, details in data["categories"].items():
        tab = page.locator(f"[data-selector-categories] [data-category-id='{category}']")
        tab.click()
        state = page.locator("[data-service-selector]").evaluate("el => ({ selected:[...el.querySelectorAll('[data-selector-categories] [role=tab]')].filter(n=>n.getAttribute('aria-selected')==='true').length, name:el.querySelector('[data-selector-name]').textContent, price:el.querySelector('[data-selector-price]').textContent, detail:el.querySelector('[data-selector-details]').getAttribute('href') })")
        service_id = data["featuredServiceIds"][category][0]
        service = next(item for item in data["services"] if item["id"] == service_id)
        expected_price = service["pricing"][branch]["formatted"]
        if state["selected"] != 1 or state["name"] != service["name"] or state["price"] != expected_price:
            errors.append(f"selector-{branch}-{category}: rendered selection differs from source: {state}")
        if service_id not in state["detail"] or f"{category}.html" not in state["detail"]:
            errors.append(f"selector-{branch}-{category}: detail route does not preserve selected SKU: {state['detail']}")
        featured = data["featuredServiceIds"][category]
        if len(featured) > 1:
            next_service_id = featured[-1]
            page.locator(f"[data-selector-variants] [data-service-id='{next_service_id}']").click()
            next_service = next(item for item in data["services"] if item["id"] == next_service_id)
            updated = page.locator("[data-selector-name]").inner_text()
            updated_price = page.locator("[data-selector-price]").inner_text()
            if updated != next_service["name"] or updated_price != next_service["pricing"][branch]["formatted"]:
                errors.append(f"selector-{branch}-{category}: variant update failed")
        chosen.append(category)
    return {"branch": branch, "categoriesChanged": len(chosen), "categories": chosen}


def verify_catalogue(page: Page, base: str, branch: str, errors: list[str]) -> dict:
    load(page, base, f"v2/{branch}/prices/index.html", f"catalogue-{branch}", errors)
    count = page.locator("[data-catalog-count]").inner_text()
    if "254" not in count:
        errors.append(f"catalogue-{branch}: initial row count is not 254: {count}")
    page.locator("[data-catalog-filter='implantation']").click()
    filtered = page.locator("[data-price-item]:visible").count()
    if filtered != 18:
        errors.append(f"catalogue-{branch}: implantation filter should show 18 rows, got {filtered}")
    page.locator("[data-catalog-search]").fill("svc_implantation_091")
    match_count = page.locator("[data-price-item]:visible").count()
    if match_count != 1:
        errors.append(f"catalogue-{branch}: exact term should match one row, got {match_count}")
    row_name = page.locator("[data-price-item]:visible .price-name").first.inner_text() if match_count else ""
    if "Osstem/Dentium" not in row_name:
        errors.append(f"catalogue-{branch}: wrong filtered service row: {row_name}")
    page.locator("[data-catalog-search]").fill("__no_such_dental_service__")
    if page.locator("[data-catalog-empty]").is_hidden():
        errors.append(f"catalogue-{branch}: no-results state did not appear")
    page.locator("[data-clear-search]").click()
    if page.locator("[data-price-item]:visible").count() != 18:
        errors.append(f"catalogue-{branch}: clear-search did not retain the active category filter")
    page.locator("[data-catalog-filter='all']").click()
    if page.locator("[data-price-item]:visible").count() != 254:
        errors.append(f"catalogue-{branch}: reset filters did not restore all 254 positions")
    sample = page.locator("[data-price-item]:visible").first
    sample.locator("summary").click()
    details_open = sample.evaluate("el => el.open")
    if not details_open:
        errors.append(f"catalogue-{branch}: detail accordion did not open")
    return {"branch": branch, "initialCount": count, "categoryFilterRows": filtered, "searchMatches": match_count, "detailsOpen": details_open}


def verify_menu(page: Page, base: str, branch: str, errors: list[str]) -> dict:
    page.set_viewport_size({"width": 390, "height": HEIGHT})
    load(page, base, f"v2/{branch}/index.html", f"menu-{branch}", errors)
    toggle = page.locator("[data-menu-toggle]")
    nav = page.locator("[data-primary-nav]")
    toggle.click()
    state = nav.evaluate("node => ({display:getComputedStyle(node).display,expanded:document.querySelector('[data-menu-toggle]').getAttribute('aria-expanded'),right:node.getBoundingClientRect().right})")
    if state["display"] == "none" or state["expanded"] != "true" or state["right"] > 391:
        errors.append(f"mobile menu did not fit/open: {state}")
    page.keyboard.press("Escape")
    if toggle.get_attribute("aria-expanded") != "false" or page.evaluate("document.activeElement.matches('[data-menu-toggle]')") is not True:
        errors.append("Escape did not close the mobile menu and restore focus")
    return {"branch": branch, "open": state["display"] != "none", "escapeRestoredFocus": toggle.get_attribute("aria-expanded") == "false"}


def verify_booking(page: Page, context: BrowserContext, base: str, branch: str, errors: list[str]) -> dict:
    load(page, base, f"v2/{branch}/index.html", f"booking-{branch}", errors)
    page.set_viewport_size({"width": 390, "height": HEIGHT})
    page.locator("[data-selector-categories] [data-category-id='orthodontics']").click()
    opener = page.locator(".selected-procedure [data-open-booking]")
    selected_id = opener.get_attribute("data-service-id")
    selected = page.locator("[data-selector-name]").inner_text()
    opener.click()
    dialog = page.locator("[data-booking-dialog]")
    if dialog.evaluate("el => el.open") is not True:
        errors.append("native booking dialog did not open")
    if not dialog.locator("[data-booking-service]").is_visible() or dialog.locator("[data-booking-service-name]").inner_text() != selected:
        errors.append("booking dialog did not show the selected service")
    if "не передаётся в DentalPRO" not in dialog.locator("[data-booking-service-note]").inner_text():
        errors.append("booking transfer disclosure missing")
    online = dialog.locator('a[href="https://dantist-prokshino.ru/online-zapis/"]')
    if online.get_attribute("href") != "https://dantist-prokshino.ru/online-zapis/":
        errors.append("DentalPRO destination is not the audited live URL")
    online_click_safe = online.get_attribute("target") == "_blank"
    online_label = online.inner_text().strip()
    expected_label = "Открыть DentalPRO · Прокшино ↗" if branch == "ispanskie" else "Продолжить в DentalPRO ↗"
    if online_label != expected_label:
        errors.append(f"booking-{branch}: expected honest online-booking label {expected_label!r}, got {online_label!r}")
    if branch == "ispanskie":
        warning = dialog.locator(".dialog-intro").inner_text()
        location_note = dialog.locator(".booking-choice-online > p").inner_text()
        if "филиал Прокшино" not in warning or "Испанские кварталы" not in warning or "филиала Прокшино" not in location_note:
            errors.append("Spanish Quarters online card does not clearly disclose the real Prokshino destination")
    dialog.locator("[data-book-call]").click()
    if dialog.locator("[data-booking-step='call']").is_hidden():
        errors.append("call selection did not open its real confirmation step")
    if dialog.get_attribute("aria-labelledby") != "booking-call-title":
        errors.append(f"booking-{branch}: accessible dialog title did not change for the call step")
    tel = dialog.locator("[data-booking-step='call'] a[href^='tel:']")
    if tel.get_attribute("href") != "tel:+79045199697":
        errors.append("phone URI is not E.164")
    dialog.locator("[data-copy-phone]").click()
    status = dialog.locator("[data-copy-status]").inner_text()
    copied = False
    try:
        copied = page.evaluate("navigator.clipboard.readText()") == "+7 (904) 519-96-97"
    except Exception:
        copied = "скопирован" in status.lower()
    if not copied:
        errors.append(f"copy button failed or reported fallback: {status}")
    dialog.locator("[data-booking-back]").click()
    page.keyboard.press("Escape")
    if dialog.evaluate("el => el.open"):
        errors.append("Escape did not close the booking dialog")
    if not page.evaluate("document.activeElement.matches('.selected-procedure [data-open-booking]')"):
        errors.append("dialog close did not restore focus to the control that opened it")

    # Verify closing by clicking the actual modal backdrop; do not activate any external booking URI.
    opener.click()
    page.mouse.click(2, 2)
    if dialog.evaluate("el => el.open"):
        errors.append("outside/backdrop click did not close the booking dialog")
    return {"branch": branch, "selectedServiceId": selected_id, "selectedServiceVisible": True, "onlineBookingURL": online.get_attribute("href"), "onlineLinkLabel": online_label, "phoneE164": tel.get_attribute("href"), "copyStatus": status, "copied": copied, "escapeClose": not dialog.evaluate("el => el.open"), "outsideClose": True, "externalBookingActivated": False, "targetBlank": online_click_safe}


def wait_images(page: Page) -> None:
    page.evaluate("""async () => {
      await Promise.all([...document.images].map(image => {
        image.loading = 'eager';
        return image.decode().catch(() => null);
      }));
    }""")


def screenshot_page(browser: Browser, base: str, route: str, filename: str, width: int, *, full_page: bool = False, selector: str | None = None) -> Path:
    page = browser.new_page(viewport={"width": width, "height": HEIGHT}, device_scale_factor=1)
    page.emulate_media(reduced_motion="reduce")
    response = page.goto(urljoin(base, route), wait_until="load", timeout=45000)
    if response is None or response.status >= 400:
        page.close()
        raise RuntimeError(f"cannot capture {route}")
    page.wait_for_function("window.DENTAL_V2 && document.readyState === 'complete'")
    wait_images(page)
    if selector:
        page.add_style_tag(content=".skip-link, .booking-fab { display: none !important; }")
        locator = page.locator(selector)
        locator.scroll_into_view_if_needed()
        locator.screenshot(path=str(SHOTS / filename), animations="disabled", timeout=30000)
    else:
        page.screenshot(path=str(SHOTS / filename), full_page=full_page, animations="disabled", timeout=45000)
    page.close()
    return SHOTS / filename


def make_comparison(branch: str, size: str, old_path: Path, new_path: Path, output_path: Path, labels: tuple[str, str]) -> bool:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return False
    if not old_path.is_file() or not new_path.is_file():
        return False
    left = Image.open(old_path).convert("RGB")
    right = Image.open(new_path).convert("RGB")
    if size == "desktop":
        target_width = 720
    else:
        target_width = max(left.width, right.width)
    def fit(image):
        height = round(image.height * target_width / image.width)
        return image.resize((target_width, height), Image.Resampling.LANCZOS)
    left, right = fit(left), fit(right)
    header_h = 42
    body_h = max(left.height, right.height)
    canvas = Image.new("RGB", (target_width * 2, header_h + body_h), "#f5f6f1")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype("arial.ttf", 16) if Path("C:/Windows/Fonts/arial.ttf").exists() else ImageFont.load_default()
    draw.text((16, 12), labels[0], fill="#44524b", font=font)
    draw.text((target_width + 16, 12), labels[1], fill="#176a59", font=font)
    canvas.paste(left, (0, header_h))
    canvas.paste(right, (target_width, header_h))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, format="PNG", optimize=True)
    return True


def capture_evidence(browser: Browser, base: str) -> dict:
    SHOTS.mkdir(parents=True, exist_ok=True)
    entries: list[dict[str, str]] = []
    def add(route: str, file: str, width: int, *, full: bool = False, selector: str | None = None, label: str = ""):
        path = screenshot_page(browser, base, route, file, width, full_page=full, selector=selector)
        entries.append({"file": path.relative_to(ROOT).as_posix(), "label": label, "route": route, "width": width})
        return path

    chooser_m = add("v2/index.html", "v2-mobile-chooser-390.png", 390, label="Филиальный селектор · mobile")
    add("v2/index.html", "v2-desktop-chooser-1440.png", 1440, label="Филиальный селектор · desktop")
    old_new: dict[str, dict[str, Path]] = {}
    for branch in ("prokshino", "ispanskie"):
        home = f"v2/{branch}/index.html"
        mobile_home = add(home, f"v2-mobile-home-{branch}-390.png", 390, full=False, label=f"Главная · {branch} · mobile")
        desktop_home = add(home, f"v2-desktop-home-{branch}-1440.png", 1440, full=False, label=f"Главная · {branch} · desktop")
        add(home, f"v2-full-home-{branch}-1440.png", 1440, full=True, label=f"Главная целиком · {branch} · desktop 1440 px")
        add(home, f"v2-full-home-{branch}-390.png", 390, full=True, label=f"Страница целиком · {branch} · mobile")
        add(home, f"v2-home-doctors-{branch}-390.png", 390, selector=".team-strip", label=f"Листаемые карточки врачей · {branch} · mobile")
        add(home, f"v2-home-doctors-{branch}-1440.png", 1440, selector=".team-strip", label=f"Листаемые карточки врачей · {branch} · desktop")
        old_new[branch] = {"mobile": mobile_home, "desktop": desktop_home}
        direction = f"v2/{branch}/directions/index.html"
        add(direction, f"v2-mobile-directions-{branch}-390.png", 390, selector=".directions-selector .service-selector", label=f"Интерактивный выбор направлений · {branch}")
        add(direction, f"v2-desktop-directions-{branch}-1440.png", 1440, selector=".directions-selector .service-selector", label=f"Выбор направлений · {branch} · desktop")
        service = f"v2/{branch}/services/implantation.html"
        add(service, f"v2-desktop-service-{branch}-1440.png", 1440, selector=".service-hero-grid", label=f"Направление: имплантация · {branch}")
        add(service, f"v2-mobile-service-{branch}-390.png", 390, selector=".featured-price-list", label=f"Позиции направления · {branch} · mobile")
        doctors = f"v2/{branch}/doctors/index.html"
        add(doctors, f"v2-mobile-doctors-{branch}-390.png", 390, full=False, label=f"Врачи · {branch} · mobile")
        add(doctors, f"v2-desktop-doctors-{branch}-1440.png", 1440, selector=".doctor-profile-grid", label=f"Врачи · {branch} · desktop")
        doctor_slug = "diana-fiasheva"
        doctor = f"v2/{branch}/doctors/{doctor_slug}.html"
        add(doctor, f"v2-mobile-doctor-{branch}-390.png", 390, selector=".doctor-detail-grid", label=f"Профиль врача · {branch} · mobile")
        add(doctor, f"v2-desktop-doctor-{branch}-1440.png", 1440, full=False, label=f"Профиль врача · {branch} · desktop")
        prices = f"v2/{branch}/prices/index.html"
        add(prices, f"v2-mobile-prices-{branch}-390.png", 390, full=False, label=f"Каталог цен · {branch} · mobile")
        add(prices, f"v2-desktop-prices-{branch}-1440.png", 1440, full=False, label=f"Каталог цен · {branch} · desktop")
        contacts = f"v2/{branch}/contacts/index.html"
        add(contacts, f"v2-mobile-contacts-{branch}-390.png", 390, selector=".contact-detail-grid", label=f"Контакты · {branch} · mobile")
        add(contacts, f"v2-desktop-contacts-{branch}-1440.png", 1440, selector=".contact-detail-grid", label=f"Контакты · {branch} · desktop")
    # Capture the chosen variant/card state as a distinct interaction artifact.
    page = browser.new_page(viewport={"width": 1440, "height": HEIGHT})
    page.goto(urljoin(base, "v2/prokshino/index.html"), wait_until="load")
    page.locator("[data-selector-categories] [data-category-id='orthodontics']").click()
    page.locator("[data-selector-variants] [data-service-id='svc_orthodontics_212']").click()
    page.locator("[data-selector-card]").screenshot(path=str(SHOTS / "v2-selected-orthodontic-variant.png"), animations="disabled")
    entries.append({"file": "design/v2qa/screenshots/v2-selected-orthodontic-variant.png", "label": "После выбора: ортодонтия · самостоятельная позиция", "route": "v2/prokshino/index.html", "width": 1440})
    page.close()

    page = browser.new_page(viewport={"width": 390, "height": HEIGHT})
    page.goto(urljoin(base, "v2/prokshino/index.html"), wait_until="load")
    page.locator("[data-selector-categories] [data-category-id='orthodontics']").click()
    page.locator(".selected-procedure [data-open-booking]").click()
    dialog = page.locator("[data-booking-dialog]")
    dialog.screenshot(path=str(SHOTS / "v2-booking-modal-mobile-390.png"), animations="disabled")
    entries.append({"file": "design/v2qa/screenshots/v2-booking-modal-mobile-390.png", "label": "Способ записи · выбранная услуга · mobile", "route": "v2/prokshino/index.html", "width": 390})
    dialog.locator("[data-book-call]").click()
    page.locator("[data-booking-step='call']").screenshot(path=str(SHOTS / "v2-booking-call-step-mobile-390.png"), animations="disabled")
    entries.append({"file": "design/v2qa/screenshots/v2-booking-call-step-mobile-390.png", "label": "Подтверждение звонка и номер E.164 · mobile", "route": "v2/prokshino/index.html", "width": 390})
    page.close()

    page = browser.new_page(viewport={"width": 390, "height": HEIGHT})
    page.goto(urljoin(base, "v2/ispanskie/index.html"), wait_until="load")
    page.locator(".booking-fab").click()
    page.locator("[data-booking-dialog]").screenshot(path=str(SHOTS / "v2-booking-modal-ispanskie-mobile-390.png"), animations="disabled")
    entries.append({"file": "design/v2qa/screenshots/v2-booking-modal-ispanskie-mobile-390.png", "label": "Запись Испанские кварталы · явное уточнение маршрута DentalPRO · mobile", "route": "v2/ispanskie/index.html", "width": 390})
    page.close()

    page = browser.new_page(viewport={"width": 1440, "height": HEIGHT})
    page.goto(urljoin(base, "v2/prokshino/index.html"), wait_until="load")
    page.locator("[data-selector-categories] [data-category-id='orthodontics']").click()
    page.locator(".selected-procedure [data-open-booking]").click()
    page.locator("[data-booking-dialog]").screenshot(path=str(SHOTS / "v2-booking-modal-desktop-1440.png"), animations="disabled")
    entries.append({"file": "design/v2qa/screenshots/v2-booking-modal-desktop-1440.png", "label": "Способ записи · выбранная услуга · desktop", "route": "v2/prokshino/index.html", "width": 1440})
    page.close()

    for branch in ("prokshino", "ispanskie"):
        reference = "prokshino" if branch == "prokshino" else "ispanskie"
        mobile_old = ROOT / "design" / "qa" / "screenshots" / f"old_{reference}_mobile_390.png"
        desktop_old = ROOT / "design" / "qa" / "screenshots" / f"old_{reference}_desktop_1440.png"
        mobile_comp = SHOTS / f"v2-before-after-mobile-{branch}.png"
        desktop_comp = SHOTS / f"v2-before-after-desktop-{branch}.png"
        mobile_ok = make_comparison(branch, "mobile", mobile_old, old_new[branch]["mobile"], mobile_comp, ("ПРЕДЫДУЩИЙ PREVIEW", "V2 · НОВАЯ АРХИТЕКТУРА"))
        desktop_ok = make_comparison(branch, "desktop", desktop_old, old_new[branch]["desktop"], desktop_comp, ("ПРЕДЫДУЩИЙ PREVIEW", "V2 · НОВАЯ АРХИТЕКТУРА"))
        if mobile_ok:
            entries.append({"file": mobile_comp.relative_to(ROOT).as_posix(), "label": f"До / после · {branch} · mobile", "route": "comparison", "width": 390})
        if desktop_ok:
            entries.append({"file": desktop_comp.relative_to(ROOT).as_posix(), "label": f"До / после · {branch} · desktop", "route": "comparison", "width": 1440})
    return {"screenshots": entries}


def write_metrics(metrics: list[dict], route_checks: int, interactions: dict, errors: list[str], screenshots: dict) -> dict:
    overflow = [item for item in metrics if item["overflow"] or item["outOfBounds"]]
    broken = [item for item in metrics if item["brokenImages"]]
    standard_checks = len(route_list()) * len(WIDTHS)
    zoom_checks = len(route_list()) * len(ZOOM_WIDTHS)
    report = {
        "viewports": WIDTHS,
        "zoomViewports": ZOOM_WIDTHS,
        "routeChecks": standard_checks,
        "zoomChecks": zoom_checks,
        "totalLayoutChecks": route_checks,
        "routes": len(route_list()),
        "overflowCount": len(overflow),
        "overflowSamples": overflow[:25],
        "brokenImageCount": len(broken),
        "brokenImageSamples": broken[:20],
        "interactionErrors": errors,
        "interactions": interactions,
        "screenshots": screenshots["screenshots"],
        "metrics": metrics,
    }
    QA.mkdir(parents=True, exist_ok=True)
    (QA / "layout-metrics.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (QA / "interaction-results.json").write_text(json.dumps(interactions, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> None:
    QA.mkdir(parents=True, exist_ok=True)
    server, base = start_server()
    errors: list[str] = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 390, "height": HEIGHT}, device_scale_factor=1)
            origin = urlsplit(base)
            try:
                context.grant_permissions(["clipboard-read", "clipboard-write"], origin=f"{origin.scheme}://{origin.netloc}")
            except Exception:
                pass
            metrics, route_checks = route_matrix(browser, base, errors)
            interactions: dict[str, Any] = {"selectors": [], "catalogues": [], "menus": []}
            page = context.new_page()
            for branch in ("prokshino", "ispanskie"):
                interactions["selectors"].append(verify_selector(page, base, branch, errors))
                interactions["catalogues"].append(verify_catalogue(page, base, branch, errors))
                interactions["menus"].append(verify_menu(page, base, branch, errors))
            interactions["booking"] = {branch: verify_booking(page, context, base, branch, errors) for branch in ("prokshino", "ispanskie")}
            page.close()
            screenshots = capture_evidence(browser, base)
            browser.close()
        report = write_metrics(metrics, route_checks, interactions, errors, screenshots)
        if report["overflowCount"] or report["brokenImageCount"] or report["interactionErrors"]:
            print(f"V2_BROWSER_QA_FAIL overflow={report['overflowCount']} brokenImages={report['brokenImageCount']} interactionErrors={len(errors)}")
            if errors:
                print("INTERACTION_ERRORS", json.dumps(errors[:30], ensure_ascii=False))
            if report["overflowSamples"]:
                print("OVERFLOW_SAMPLES", json.dumps(report["overflowSamples"][:8], ensure_ascii=False))
            if report["brokenImageSamples"]:
                print("BROKEN_IMAGE_SAMPLES", json.dumps(report["brokenImageSamples"][:5], ensure_ascii=False))
            raise SystemExit(1)
        print(f"V2_BROWSER_QA_PASS routes={len(route_list())} viewports={len(WIDTHS)} routeChecks={report['routeChecks']} zoomChecks={report['zoomChecks']} totalLayoutChecks={report['totalLayoutChecks']} screenshots={len(screenshots['screenshots'])} overflow=0 brokenImages=0 interactionErrors=0")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
