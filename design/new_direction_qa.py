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
        photo = page.locator(".welcome-photo")
        if photo.count() != 1:
            raise AssertionError(f"{branch}: missing the non-specialist clinic welcome photo")
        loaded = page.evaluate(r"""() => ({
          localScripts: [...document.scripts].filter(s => s.src).every(s => new URL(s.src).origin === location.origin),
          heavyScripts: [...document.scripts].some(s => /three(?:\.min)?\.js|gsap|lottie/i.test(s.src)),
          imageLocal: [...document.images].every(i => new URL(i.currentSrc || i.src, location.href).origin === location.origin),
          initialTransform: getComputedStyle(document.querySelector('.welcome-photo')).transform,
          transitionEnabled: getComputedStyle(document.querySelector('.welcome-photo')).transitionDuration
        })""")
        if not loaded["localScripts"] or loaded["heavyScripts"] or not loaded["imageLocal"]:
            raise AssertionError(f"{branch}: remote or heavyweight visual dependency found: {loaded}")
        if not loaded["initialTransform"].startswith("matrix3d("):
            raise AssertionError(f"{branch}: local CSS perspective treatment missing: {loaded}")
        page.mouse.move(10, 10)
        before = photo.evaluate("e => getComputedStyle(e).transform")
        photo.hover()
        page.wait_for_timeout(760)
        after = photo.evaluate("e => getComputedStyle(e).transform")
        if not after.startswith("matrix3d(") or after == before:
            raise AssertionError(f"{branch}: welcome photo has no gentle pointer-depth response: {before} -> {after}")
        page.emulate_media(reduced_motion="reduce")
        reduced = photo.evaluate("e => ({duration:getComputedStyle(e).transitionDuration,transform:getComputedStyle(e).transform})")
        if float(reduced["duration"].split(",")[0].replace("s", "")) > .001 or reduced["transform"] != "none":
            raise AssertionError(f"{branch}: reduced-motion preference was not respected: {reduced}")
        page.close()
    print("V5_MOTION_PASS localClinicPhotos=true cssOnly3d=true heavyweightRuntime=false reducedMotion=true")


def booking_checks(browser, base: str, screenshots: bool) -> None:
    for branch in BRANCHES:
        for width in (320, 390, 1440):
            height = 844 if width < 600 else 900
            page = browser.new_page(viewport={"width": width, "height": height})
            url = f"{base}/v2/{branch}/index.html"
            page.goto(url, wait_until="networkidle")
            before_url = page.url
            fab = page.locator(".booking-fab")
            if not fab.is_visible() or fab.count() != 1:
                raise AssertionError(f"{branch}/{width}: persistent appointment button is missing")
            if page.locator(".home-welcome [data-open-booking], .primary-nav [data-open-booking]").count():
                raise AssertionError(f"{branch}/{width}: appointment action is still embedded in the welcome/header")
            geometry = fab.evaluate("e => {const r=e.getBoundingClientRect(),s=getComputedStyle(e);return {position:s.position,left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height,viewportWidth:innerWidth,viewportHeight:innerHeight}}")
            if geometry["position"] != "fixed" or geometry["left"] < 0 or geometry["right"] > width + .5 or geometry["bottom"] > height + .5 or width - geometry["right"] > 28 or height - geometry["bottom"] > 30:
                raise AssertionError(f"{branch}/{width}: booking control is not safely fixed at lower right: {geometry}")
            fab.click()
            dialog = page.locator("[data-booking-dialog]")
            if not dialog.is_visible() or page.url != before_url:
                raise AssertionError(f"{branch}/{width}: clicking appointment navigated before the visitor chose a method")
            if dialog.get_attribute("id") != fab.get_attribute("aria-controls"):
                raise AssertionError(f"{branch}/{width}: booking trigger does not reference its dialog")
            page.wait_for_timeout(430)  # let the native CSS bottom-sheet entrance animation settle
            online = dialog.locator(f'a[href="{OFFICIAL["online"]}"]')
            phone_choice = dialog.locator("[data-book-call]")
            whatsapp = dialog.locator(f'a[href="{OFFICIAL["whatsapp"]}"]')
            telegram = dialog.locator(f'a[href="{OFFICIAL["telegram"]}"]')
            for locator, label in ((online, "DentalPRO"), (phone_choice, "phone"), (whatsapp, "WhatsApp"), (telegram, "Telegram")):
                if locator.count() != 1 or not locator.is_visible():
                    raise AssertionError(f"{branch}/{width}: missing visible {label} choice")
            for link in (online, whatsapp, telegram):
                if link.get_attribute("target") != "_blank" or not link.get_attribute("rel"):
                    raise AssertionError(f"{branch}/{width}: external route is not a deliberate safe link")
            if branch == "ispanskie" and ("Прокшино" not in dialog.inner_text() or "Испанские кварталы" not in dialog.inner_text()):
                raise AssertionError("Spanish Quarters must disclose the actual Prokshino DentalPRO destination")
            if width < 600:
                geometry = dialog.evaluate("e=>({left:e.getBoundingClientRect().left,right:e.getBoundingClientRect().right,bottom:e.getBoundingClientRect().bottom,top:e.getBoundingClientRect().top,height:e.getBoundingClientRect().height,scroll:e.scrollHeight,viewport:innerHeight,lastActionBottom:e.querySelector('.booking-message-actions a:last-child').getBoundingClientRect().bottom})")
                if geometry["left"] < -.5 or geometry["right"] > width + .5 or geometry["bottom"] > height + .5 or geometry["height"] > 820 or geometry["lastActionBottom"] > geometry["bottom"] - 4:
                    raise AssertionError(f"{branch}/{width}: mobile booking sheet is clipped: {geometry}")
            if screenshots and width == 390:
                target = ROOT / "design" / "v2qa" / "screenshots" / f"premium-booking-choice-{branch}-390.png"
                dialog.screenshot(path=str(target), animations="disabled")
            phone_choice.click()
            call_step = dialog.locator('[data-booking-step="call"]')
            if not call_step.is_visible() or call_step.locator(f'a[href="{OFFICIAL["phone"]}"]').count() != 1 or call_step.locator("[data-copy-phone]").count() != 1:
                raise AssertionError(f"{branch}/{width}: phone option did not reveal the actual number/copy step")
            if page.url != before_url:
                raise AssertionError(f"{branch}/{width}: phone preview caused an unexpected redirect")
            page.keyboard.press("Escape")
            if dialog.is_visible() or page.locator(":focus").get_attribute("class") != "booking-fab":
                raise AssertionError(f"{branch}/{width}: close or focus restore failed")
            page.close()
    print("V5_BOOKING_PASS persistentLowerRight=true explicitChoices=phone+DentalPRO+WhatsApp+Telegram earlyRedirects=0 widths=320,390,1440")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--motion", action="store_true")
    parser.add_argument("--booking", action="store_true")
    parser.add_argument("--screenshots", action="store_true")
    args = parser.parse_args()
    run_motion = args.motion or not args.booking
    run_booking = args.booking or not args.motion
    server, base = start_server()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            if run_motion:
                motion_checks(browser, base)
            if run_booking:
                booking_checks(browser, base, args.screenshots)
            browser.close()
    finally:
        server.shutdown()
    print("V5_HOMEPAGE_UX_PASS")


if __name__ == "__main__":
    main()
