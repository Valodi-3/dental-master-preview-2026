"""
Automated verification and screenshot capture for GATE 3 ART DIRECTIONS.
Tests both 'editorial' and 'clinical' themes across all viewports with overflow-x: visible.
Captures comparison screenshots.
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

THEMES = ["editorial", "clinical"]

def run_art_direction_tests():
    print("=== DENTAL ATLAS: GATE 3 ART DIRECTIONS VERIFICATION ===")
    all_passed = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for theme in THEMES:
            print(f"\n--- Testing Theme: {theme.upper()} (overflow-x: visible) ---")
            for vp in VIEWPORTS:
                page = browser.new_page(viewport={"width": vp["width"], "height": vp["height"]})
                page.goto(f"{FILE_URL}?theme={theme}&branch=ispanskie&view=services", wait_until="domcontentloaded")
                
                page.evaluate("""() => {
                    const style = document.createElement('style');
                    style.textContent = '* { overflow-x: visible !important; }';
                    document.head.appendChild(style);
                }""")
                
                scroll_w = page.evaluate("() => document.documentElement.scrollWidth")
                inner_w = page.evaluate("() => window.innerWidth")
                ok = scroll_w <= inner_w
                status = "PASS" if ok else f"FAIL (scrollWidth={scroll_w}px > {inner_w}px)"
                print(f"[{status}] {theme.upper()} @ {vp['name']}: innerWidth={inner_w}px, scrollWidth={scroll_w}px")
                if not ok:
                    all_passed = False
                page.close()

        # Test interactive switching
        print("\n--- Testing Interactive Theme Switcher Button ---")
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(f"{FILE_URL}?theme=editorial", wait_until="domcontentloaded")
        
        # Click clinical button
        page.locator("#themeBtnClinical").click()
        time.sleep(0.1)
        has_clinical = page.evaluate("() => document.body.classList.contains('theme-clinical')")
        url_search = page.evaluate("() => window.location.search")
        print(f"After click Clinical: body has theme-clinical = {has_clinical}, URL search = '{url_search}'")
        assert has_clinical, "Body should have theme-clinical class"
        assert "theme=clinical" in url_search, "URL search should contain theme=clinical"

        # Click editorial button
        page.locator("#themeBtnEditorial").click()
        time.sleep(0.1)
        has_editorial = page.evaluate("() => document.body.classList.contains('theme-editorial')")
        url_search2 = page.evaluate("() => window.location.search")
        print(f"After click Editorial: body has theme-editorial = {has_editorial}, URL search = '{url_search2}'")
        assert has_editorial, "Body should have theme-editorial class"
        assert "theme=editorial" in url_search2, "URL search should contain theme=editorial"
        page.close()

        # Capture high-res comparison screenshots
        print("\n--- Capturing High-Res Art Direction Comparison Screenshots ---")
        shots = [
            # Direction 1: Editorial
            {"theme": "editorial", "view": "services", "vp": {"width": 1440, "height": 900}, "file": "atlas-art-editorial-services-1440.png"},
            {"theme": "editorial", "view": "services", "vp": {"width": 390, "height": 844}, "file": "atlas-art-editorial-services-390.png"},
            {"theme": "editorial", "view": "doctors", "vp": {"width": 1440, "height": 900}, "file": "atlas-art-editorial-doctors-1440.png"},
            # Direction 2: Clinical
            {"theme": "clinical", "view": "services", "vp": {"width": 1440, "height": 900}, "file": "atlas-art-clinical-services-1440.png"},
            {"theme": "clinical", "view": "services", "vp": {"width": 390, "height": 844}, "file": "atlas-art-clinical-services-390.png"},
            {"theme": "clinical", "view": "doctors", "vp": {"width": 1440, "height": 900}, "file": "atlas-art-clinical-doctors-1440.png"}
        ]

        for s in shots:
            page = browser.new_page(viewport=s["vp"])
            page.goto(f"{FILE_URL}?theme={s['theme']}&branch=ispanskie&view={s['view']}", wait_until="domcontentloaded")
            time.sleep(0.3)
            out_file = os.path.join(SCREENSHOTS_DIR, s["file"])
            page.screenshot(path=out_file)
            print(f"[Screenshot] Saved {s['file']} ({s['vp']['width']}x{s['vp']['height']})")
            page.close()

        browser.close()

    print(f"\nFinal status: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    return all_passed

if __name__ == "__main__":
    success = run_art_direction_tests()
    sys.exit(0 if success else 1)
