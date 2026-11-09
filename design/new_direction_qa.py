from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from playwright.sync_api import sync_playwright
from design.v2_visual_qa import start_server

BRANCHES = ("prokshino", "ispanskie")
OFFICIAL = {
    "online": "https://dantist-prokshino.ru/online-zapis/",
    "whatsapp": "https://wa.me/message/2WBFWCZJGHQDG1",
    "telegram": "https://t.me/Stomatologiya1108",
    "phone": "tel:+79045199697",
}


def motion_checks(browser, base: str) -> None:
    for branch in BRANCHES:
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(f"{base}/v2/{branch}/index.html", wait_until="networkidle")
        loaded = page.evaluate(r"""() => ({
          localScripts: [...document.scripts].filter(s => s.src).map(s => new URL(s.src).origin === location.origin),
          heavyScripts: [...document.scripts].some(s => /three(?:\.min)?\.js|gsap|lottie/i.test(s.src)),
          imageLocal: [...document.images].every(i => new URL(i.currentSrc || i.src, location.href).origin === location.origin),
          heroPerspective: getComputedStyle(document.querySelector('.home-hero-image, .family-photo-stack')).perspective,
          transitionEnabled: getComputedStyle(document.querySelector('.home-hero-image img, .family-photo-main img')).transitionDuration,
          routeTransitionSupported: CSS.supports('view-transition-name: root')
        })""")
        if not all(loaded["localScripts"]) or loaded["heavyScripts"] or not loaded["imageLocal"]:
            raise AssertionError(f"{branch}: remote or heavy visual dependency found: {loaded}")
        if loaded["heroPerspective"] in ("none", "0px"):
            raise AssertionError(f"{branch}: no CSS depth/perspective treatment: {loaded}")
        if branch == "prokshino":
            image = page.locator(".home-hero-image img")
            page.locator(".home-hero-image").hover()
            transform = image.evaluate("e => getComputedStyle(e).transform")
            if not transform.startswith("matrix3d("):
                raise AssertionError(f"Prokshino pointer interaction does not create lightweight CSS depth: {transform}")
        else:
            page.locator(".family-photo-main").hover()
            transform = page.locator(".family-photo-main").evaluate("e => getComputedStyle(e).transform")
            if not transform.startswith("matrix3d("):
                raise AssertionError(f"Spanish Quarters photo stack lacks a CSS-only 3D hover: {transform}")
        page.emulate_media(reduced_motion="reduce")
        reduced = page.evaluate("""() => ({
          scroll: getComputedStyle(document.documentElement).scrollBehavior,
          duration: getComputedStyle(document.querySelector('.home-hero-image img, .family-photo-main img')).transitionDuration,
          heroTransform: getComputedStyle(document.querySelector('.home-hero-image img, .family-photo-main img')).transform
        })""")
        if reduced["scroll"] != "auto" or float(reduced["duration"].split(",")[0].replace("s", "")) > 0.001:
            raise AssertionError(f"{branch}: reduced-motion preference not respected: {reduced}")
        page.close()
    print("NEW_DIRECTION_MOTION_PASS localAssets=true css3d=true heavyRuntime=false reducedMotion=true")


def booking_checks(browser, base: str, screenshots: bool) -> None:
    for branch in BRANCHES:
        for width in (320, 390, 1440):
            page_height = 844 if width < 600 else 900
            page = browser.new_page(viewport={"width": width, "height": page_height})
            url = f"{base}/v2/{branch}/index.html"
            page.goto(url, wait_until="networkidle")
            before_url = page.url
            cta = page.locator(".home-hero .hero-actions [data-open-booking]")
            cta.click()
            dialog = page.locator("[data-booking-dialog]")
            if not dialog.is_visible() or page.url != before_url:
                raise AssertionError(f"{branch}/{width}: appointment CTA navigated instead of opening the choice dialog")
            page.wait_for_timeout(420)
            online = dialog.locator(f'a[href="{OFFICIAL["online"]}"]')
            call_route = dialog.locator('[data-book-call]')
            whatsapp = dialog.locator(f'a[href="{OFFICIAL["whatsapp"]}"]')
            telegram = dialog.locator(f'a[href="{OFFICIAL["telegram"]}"]')
            for locator, label in ((online, "DentalPRO"), (call_route, "phone choice"), (whatsapp, "WhatsApp"), (telegram, "Telegram")):
                if locator.count() != 1 or not locator.is_visible():
                    raise AssertionError(f"{branch}/{width}: missing {label} choice")
            for link in (online, whatsapp, telegram):
                if link.get_attribute("target") != "_blank" or link.get_attribute("rel") is None:
                    raise AssertionError(f"{branch}/{width}: final external choice must be explicit and safely opened")
            if branch == "ispanskie" and "Прокшино" not in dialog.inner_text():
                raise AssertionError("Spanish Quarters must disclose that DentalPRO opens Prokshino")
            if width < 600:
                dims = dialog.evaluate("e=>({left:e.getBoundingClientRect().left,right:e.getBoundingClientRect().right,bottom:e.getBoundingClientRect().bottom,top:e.getBoundingClientRect().top,height:e.getBoundingClientRect().height,scroll:e.scrollHeight,viewport:innerHeight,lastActionBottom:e.querySelector('.booking-message-actions a:last-child').getBoundingClientRect().bottom})")
                if dims["left"] < -0.5 or dims["right"] > width + 0.5 or dims["bottom"] > dims["viewport"] + 0.5 or dims["height"] > 820 or dims["lastActionBottom"] > dims["bottom"] - 4:
                    raise AssertionError(f"{branch}/{width}: bottom sheet outside safe viewport: {dims}")
            if screenshots and width == 390:
                out = ROOT / "design" / "v2qa" / "screenshots" / f"premium-booking-choice-{branch}-390.png"
                dialog.screenshot(path=str(out))
            call_route.click()
            call_step = dialog.locator('[data-booking-step="call"]')
            if not call_step.is_visible() or call_step.locator(f'a[href="{OFFICIAL["phone"]}"]').count() != 1 or call_step.locator('[data-copy-phone]').count() != 1:
                raise AssertionError(f"{branch}/{width}: call choice must reveal a real tel link and copy control")
            if page.url != before_url:
                raise AssertionError(f"{branch}/{width}: phone review step caused an unexpected navigation")
            page.keyboard.press("Escape")
            if dialog.is_visible():
                raise AssertionError(f"{branch}/{width}: Escape did not close the choice dialog")
            page.close()
    print("NEW_DIRECTION_BOOKING_PASS explicitChoices=3 branches=2 widths=320,390,1440 earlyRedirects=0")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--motion", action="store_true")
    parser.add_argument("--booking", action="store_true")
    parser.add_argument("--screenshots", action="store_true")
    args = parser.parse_args()
    motion = args.motion or not args.booking
    booking = args.booking or not args.motion
    server, base = start_server()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            if motion:
                motion_checks(browser, base)
            if booking:
                booking_checks(browser, base, args.screenshots)
            browser.close()
    finally:
        server.shutdown()
    print("NEW_DIRECTION_UX_PASS")


if __name__ == "__main__":
    main()
