from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "v2"
QA = ROOT / "design" / "v2qa"
SHOTS = QA / "screenshots"
WIDTHS = (320, 360, 375, 390, 430, 768, 1024, 1440, 1920)
BRANCHES = ("prokshino", "ispanskie")
sys.path.insert(0, str(ROOT))
from playwright.sync_api import sync_playwright
from design.v2_visual_qa import HEIGHT, start_server


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def assert_true(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)


def check_profile(page, branch: str, doctor: dict) -> None:
    profile_href = page.locator(f'[data-doctor-slug="{doctor["slug"]}"] .doctor-card-profile').get_attribute("href")
    expected_fragment = "#certificates" if doctor["certificates"] else "#doctor-education"
    assert_true(bool(profile_href and profile_href.endswith(expected_fragment)), f"{branch}/{doctor['slug']}: profile shortcut does not lead to actual sourced details")
    page.goto(urljoin(page.url, profile_href), wait_until="networkidle")
    assert_true(page.locator("h1").inner_text().strip() == doctor["name"], f"{branch}/{doctor['slug']}: profile title does not match the official roster")
    education = page.locator("#doctor-education").inner_text()
    assert_true(doctor["education"][:28] in education, f"{branch}/{doctor['slug']}: sourced education is missing")
    cert_links = page.locator("#certificates .certificate-link")
    assert_true(cert_links.count() == len(doctor["certificates"]), f"{branch}/{doctor['slug']}: certificate count differs from verified source")
    for index, certificate in enumerate(doctor["certificates"]):
        link = cert_links.nth(index)
        assert_true(certificate["title"] in link.inner_text(), f"{branch}/{doctor['slug']}: certificate label differs")
        assert_true(link.get_attribute("href") == certificate["url"], f"{branch}/{doctor['slug']}: certificate does not point to the published source document")
    assert_true(doctor["experience"] in page.locator(".experience-stamp").inner_text(), f"{branch}/{doctor['slug']}: experience missing from profile")


def check_branch(browser, base: str, branch: str, clinic: dict, doctors: list[dict]) -> dict:
    context = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1, has_touch=True, is_mobile=True)
    page = context.new_page()
    url = f"{base}/v2/{branch}/index.html"
    response = page.goto(url, wait_until="networkidle", timeout=45000)
    assert_true(response is not None and response.status == 200, f"{branch}: homepage request failed")
    page.wait_for_function("window.DENTAL_V2 && document.readyState === 'complete'")

    hero = page.locator(".home-welcome")
    assert_true(hero.count() == 1, f"{branch}: welcoming first screen is missing")
    assert_true("Добро пожаловать" in hero.locator("h1").inner_text(), f"{branch}: homepage does not greet the visitor first")
    assert_true(hero.locator("[data-open-booking]").count() == 0, f"{branch}: booking CTA is pushed into the welcome hero")
    assert_true(hero.locator(".doctor-carousel-card, .doctor-mini").count() == 0, f"{branch}: staff portraits leak into the welcome hero")
    assert_true(hero.locator(".service-selector, .selected-procedure, [data-price-item], .price-stat").count() == 0, f"{branch}: service/catalogue promotion appears in the welcome hero")
    assert_true(hero.locator(".welcome-photo").count() == 1, f"{branch}: clinic welcome photo is missing")
    image_src = hero.locator(".welcome-photo img").get_attribute("src") or ""
    assert_true(image_src.endswith(clinic["welcomeImage"]), f"{branch}: wrong clinic photo in welcome image: {image_src}")
    assert_true(all(not image_src.endswith(doctor["portrait"]) for doctor in doctors), f"{branch}: a specialist headshot was used as the welcome image")
    assert_true(hero.locator(".welcome-photo img").get_attribute("alt") == clinic["welcomeImageAlt"], f"{branch}: welcome photo alt text differs from the sourced data")
    assert_true(page.locator(".primary-nav [data-open-booking], .nav-book").count() == 0, f"{branch}: booking remains promoted in the main navigation")
    order = page.evaluate("() => ['clinic-space','clinic-team','service-selection'].map(id => [...document.querySelectorAll('main section')].findIndex(s => s.id === id))")
    assert_true(order == sorted(order) and min(order) >= 0, f"{branch}: clinic/story, team and services are in the wrong order: {order}")

    track = page.locator("[data-doctor-track]")
    cards = page.locator("[data-doctor-card]")
    assert_true(cards.count() == len(doctors) == 5, f"{branch}: expected five browsable doctor profiles")
    for index, doctor in enumerate(doctors):
        card = cards.nth(index)
        assert_true(card.get_attribute("data-doctor-slug") == doctor["slug"], f"{branch}: doctor order differs from verified roster")
        for text in (doctor["name"], doctor["role"], doctor["experience"]):
            assert_true(text in card.inner_text(), f"{branch}/{doctor['slug']}: card is missing published detail {text}")
        portrait = ROOT / doctor["portrait"]
        assert_true(portrait.is_file(), f"{branch}/{doctor['slug']}: local official portrait is missing")
        assert_true((card.locator("img").get_attribute("src") or "").endswith(doctor["portrait"]), f"{branch}/{doctor['slug']}: incorrect local portrait")

    position = page.locator("[data-doctor-position]")
    previous = page.locator("[data-doctor-prev]")
    next_button = page.locator("[data-doctor-next]")
    assert_true(position.inner_text().strip() == "01 / 05", f"{branch}: carousel initial position is wrong")
    assert_true(previous.is_disabled() and not next_button.is_disabled(), f"{branch}: carousel first-page controls have incorrect state")
    next_button.click()
    page.wait_for_function("document.querySelector('[data-doctor-track]').scrollLeft > 2", timeout=3500)
    page.wait_for_timeout(150)
    assert_true(position.inner_text().strip() != "01 / 05", f"{branch}: next arrow did not update carousel position")

    # The native touch gesture checks swipe navigation on a phone-size viewport, not just arrow clicks.
    page.locator("[data-doctor-track]").evaluate("el => el.scrollTo({left:0, behavior:'instant'})")
    page.wait_for_timeout(120)
    page.locator("[data-doctor-track]").scroll_into_view_if_needed()
    box = page.locator("[data-doctor-track]").bounding_box()
    assert_true(box is not None, f"{branch}: doctor carousel has no mobile geometry")
    session = page.context.new_cdp_session(page)
    x = int(box["x"] + box["width"] * .74)
    y = int(box["y"] + min(90, box["height"] / 2))
    session.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": x, "y": y, "id": 1, "radiusX": 4, "radiusY": 4, "force": 1, "rotationAngle": 0}]})
    session.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": x - 90, "y": y, "id": 1, "radiusX": 4, "radiusY": 4, "force": 1, "rotationAngle": 0}]})
    session.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": x - 190, "y": y, "id": 1, "radiusX": 4, "radiusY": 4, "force": 1, "rotationAngle": 0}]})
    session.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
    page.wait_for_timeout(350)
    swipe_offset = track.evaluate("el => el.scrollLeft")
    session.detach()
    assert_true(swipe_offset > 1, f"{branch}: touch swipe did not horizontally browse doctor cards")

    profile_results = []
    for doctor in doctors:
        # Put the homepage back in the document before reading a card's actual profile route.
        page.goto(url, wait_until="networkidle")
        page.wait_for_function("window.DENTAL_V2 && document.readyState === 'complete'")
        check_profile(page, branch, doctor)
        profile_results.append({"slug": doctor["slug"], "education": True, "certificates": len(doctor["certificates"])})

    floating_bounds = []
    for width in WIDTHS:
        height = 844 if width <= 430 else HEIGHT
        page.set_viewport_size({"width": width, "height": height})
        page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
        page.wait_for_timeout(50)
        fab = page.locator(".booking-fab")
        assert_true(fab.count() == 1 and fab.is_visible(), f"{branch}/{width}: persistent booking control disappeared while scrolling")
        rect = fab.evaluate("e => {const r=e.getBoundingClientRect(),s=getComputedStyle(e);return {position:s.position,left:r.left,right:r.right,bottom:r.bottom,width:r.width,height:r.height,documentWidth:document.documentElement.scrollWidth,viewportWidth:innerWidth,viewportHeight:innerHeight}}")
        assert_true(rect["position"] == "fixed" and rect["left"] >= -.5 and rect["right"] <= width + .5 and rect["bottom"] <= height + .5, f"{branch}/{width}: floating booking button clips: {rect}")
        assert_true(rect["documentWidth"] <= width + 1, f"{branch}/{width}: homepage overflows horizontally: {rect}")
        floating_bounds.append({"width": width, "height": height, "left": round(rect["left"], 1), "right": round(rect["right"], 1), "bottom": round(rect["bottom"], 1)})

    # Real full-page 1440px PC images are produced by the main Playwright evidence runner.
    desktop_full = SHOTS / f"v2-full-home-{branch}-1440.png"
    assert_true(desktop_full.is_file(), f"{branch}: missing complete 1440px desktop homepage screenshot")
    try:
        from PIL import Image
        with Image.open(desktop_full) as image:
            dimensions = image.size
            assert_true(dimensions[0] == 1440 and dimensions[1] > HEIGHT, f"{branch}: desktop proof is not a full-page capture: {dimensions}")
    except ImportError:
        dimensions = None
    context.close()
    return {"branch": branch, "welcomePhoto": clinic["welcomeImage"], "homeSectionOrder": ["clinic-space", "clinic-team", "service-selection"], "doctorCards": 5, "touchSwipe": True, "profileDetails": profile_results, "floatingButtonAtNineWidths": floating_bounds, "fullDesktopScreenshot": desktop_full.relative_to(ROOT).as_posix(), "fullDesktopDimensions": dimensions}


def main() -> None:
    clinics = read_json(V2 / "data" / "clinic-content.json")["branches"]
    doctors = read_json(V2 / "data" / "doctors.json")
    QA.mkdir(parents=True, exist_ok=True)
    server, base = start_server()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            results = [check_branch(browser, base, branch, clinics[branch], doctors) for branch in BRANCHES]
            browser.close()
    finally:
        server.shutdown()
    report = {"status": "PASS", "acceptance": {"welcomeFirst": True, "noBookingInHeroOrNav": True, "floatingBooking": True, "doctorCards": 5, "touchSwipe": True, "sourceLinkedEducationAndCertificates": True, "fullDesktopScreenshots": True}, "branches": results}
    out = QA / "v5-homepage-check.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"V5_HOMEPAGE_PASS branches=2 widths={len(WIDTHS)} doctorCards=10 profiles=10 swipe=2 floatingBookingBounds={len(WIDTHS)*2} desktopFullPage=2 report={out.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
