"""
Verification script for DENTAL ATLAS Wireframe Prototype.
Runs Playwright automated checks on viewports, interaction flows, and captures screenshots.
"""

import sys
import os
import time
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(BASE_DIR, "index.html")
FILE_URL = f"file:///{HTML_PATH.replace(os.sep, '/')}"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

VIEWPORTS = [
    {"width": 320, "height": 640, "name": "320px"},
    {"width": 360, "height": 740, "name": "360px"},
    {"width": 375, "height": 667, "name": "375px"},
    {"width": 390, "height": 844, "name": "390px"},
    {"width": 430, "height": 932, "name": "430px"},
    {"width": 768, "height": 1024, "name": "768px"},
    {"width": 1024, "height": 768, "name": "1024px"},
    {"width": 1280, "height": 800, "name": "1280px"},
    {"width": 1440, "height": 900, "name": "1440px"},
    {"width": 1920, "height": 1080, "name": "1920px"}
]

def run_checks():
    print(f"=== DENTAL ATLAS PROTOTYPE VERIFICATION ===")
    print(f"Target: {FILE_URL}")
    all_passed = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # 1. Viewport Overflow Check
        print("\n--- 1. Testing Viewport Geometric Overflow (overflow-x: visible) ---")
        for vp in VIEWPORTS:
            page = browser.new_page(viewport={"width": vp["width"], "height": vp["height"]})
            page.goto(FILE_URL)
            page.wait_for_load_state("domcontentloaded")
            
            # Disable any overflow hidden to find true document width
            page.evaluate("""() => {
                const style = document.createElement('style');
                style.textContent = '* { overflow-x: visible !important; }';
                document.head.appendChild(style);
            }""")
            
            scroll_width = page.evaluate("() => document.documentElement.scrollWidth")
            inner_width = page.evaluate("() => window.innerWidth")
            
            status = "PASS" if scroll_width <= inner_width else f"FAIL (scrollWidth={scroll_width}px > {inner_width}px)"
            print(f"[{status}] Viewport {vp['name']}: innerWidth={inner_width}px, scrollWidth={scroll_width}px")
            if scroll_width > inner_width:
                all_passed = False
            page.close()

        # 2. Interactive User Pathways Test
        print("\n--- 2. Testing Interactive User Pathways ---")
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(FILE_URL)
        page.wait_for_load_state("domcontentloaded")

        # Pathway A: Select category 'Имплантация'
        cat_btns = page.locator(".nav-cat-btn")
        cat_btns.nth(2).click() # Implants
        time.sleep(0.1)

        # Select Straumann procedure
        proc_btns = page.locator(".nav-proc-btn")
        proc_btns.nth(1).click() # Straumann
        time.sleep(0.1)

        proc_title = page.locator("#stageProcTitle").text_content()
        price_val = page.locator("#stagePriceVal").text_content()
        print(f"[Check] Selected: '{proc_title}', Price: '{price_val}'")
        assert "Straumann" in proc_title, f"Expected Straumann, got {proc_title}"
        assert "66 000" in price_val, f"Expected 66 000, got {price_val}"

        # Open Booking Modal from stage
        page.locator("#stageBookBtn").click()
        time.sleep(0.1)
        modal_visible = page.locator("#bookingModal").is_visible()
        context_text = page.locator("#modalContextNotice").text_content()
        print(f"[Check] Modal opened: {modal_visible}, Context: '{context_text}'")
        assert modal_visible, "Modal should be open"
        assert "Straumann" in context_text, "Context notice should contain Straumann"

        # Close Modal with Escape
        page.keyboard.press("Escape")
        time.sleep(0.1)
        modal_visible = page.locator("#bookingModal").is_visible()
        print(f"[Check] Modal closed via Escape: {not modal_visible}")
        assert not modal_visible, "Modal should be closed"

        # Pathway B: Switch to Doctors
        page.locator('[data-pathway="doctors"]').click()
        time.sleep(0.1)
        doc_cards = page.locator(".doctor-card").count()
        print(f"[Check] Pathway B (Doctors) count: {doc_cards} cards")
        assert doc_cards >= 5, f"Expected at least 5 doctors, got {doc_cards}"

        # Pathway C: Switch to Booking
        page.locator('[data-pathway="booking"]').click()
        time.sleep(0.1)
        channel_items = page.locator(".gateway-channel-item").count()
        print(f"[Check] Pathway C (Booking Gateway) channels: {channel_items}")
        assert channel_items == 4, f"Expected 4 channels, got {channel_items}"

        # Branch Switching: Switch to Prokshino
        page.locator("#switchBranchProkshino").click()
        time.sleep(0.1)
        badge_text = page.locator("#brandBranchBadge").text_content()
        print(f"[Check] Switched to Prokshino: badge='{badge_text}'")
        assert "Прокшино" in badge_text, "Badge should reflect Prokshino"

        # Switch back to Ispanskie
        page.locator("#switchBranchIspanskie").click()
        time.sleep(0.1)
        badge_text = page.locator("#brandBranchBadge").text_content()
        print(f"[Check] Switched back to Ispanskie: badge='{badge_text}'")
        assert "Испанские" in badge_text, "Badge should reflect Ispanskie"

        page.close()

        # 3. Capture Screenshots (390px and 1440px)
        print("\n--- 3. Capturing Verification Screenshots ---")
        shots = [
            {"pathway": "services", "vp": {"width": 1440, "height": 900}, "file": "atlas-wireframe-services-1440.png"},
            {"pathway": "services", "vp": {"width": 390, "height": 844}, "file": "atlas-wireframe-services-390.png"},
            {"pathway": "doctors", "vp": {"width": 1440, "height": 900}, "file": "atlas-wireframe-doctors-1440.png"},
            {"pathway": "doctors", "vp": {"width": 390, "height": 844}, "file": "atlas-wireframe-doctors-390.png"},
            {"pathway": "booking", "vp": {"width": 1440, "height": 900}, "file": "atlas-wireframe-booking-1440.png"},
            {"pathway": "booking", "vp": {"width": 390, "height": 844}, "file": "atlas-wireframe-booking-390.png"}
        ]

        for s in shots:
            page = browser.new_page(viewport=s["vp"])
            page.goto(f"{FILE_URL}?branch=ispanskie&view={s['pathway']}")
            page.wait_for_load_state("domcontentloaded")
            time.sleep(0.2)
            out_path = os.path.join(SCREENSHOTS_DIR, s["file"])
            page.screenshot(path=out_path)
            print(f"[Screenshot] Saved {s['file']} ({s['vp']['width']}x{s['vp']['height']})")
            page.close()

        browser.close()

    print(f"\nVerification summary: {'ALL PASSED' if all_passed else 'SOME CHECKS FAILED'}")
    return all_passed

if __name__ == "__main__":
    success = run_checks()
    sys.exit(0 if success else 1)
