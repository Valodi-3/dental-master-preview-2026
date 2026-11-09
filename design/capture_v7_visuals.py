import sys
import json
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "design" / "v2qa" / "screenshots" / "v7"
SHOTS.mkdir(parents=True, exist_ok=True)

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

def start_server():
    server = ThreadingHTTPServer(("127.0.0.1", 0), lambda *args, **kwargs: QuietHandler(*args, directory=str(ROOT), **kwargs))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, f"http://127.0.0.1:{server.server_port}/"

def capture_all():
    server, base = start_server()
    print(f"Testing server running at: {base}")
    
    viewports = [320, 360, 375, 390, 430, 768, 1024, 1280, 1440, 1920]
    results = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # 1. Desktop captures (1440px)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        
        # Prokshino Home
        page.goto(f"{base}v2/prokshino/index.html", wait_until="networkidle")
        page.screenshot(path=str(SHOTS / "v7-desktop-home-prokshino-1440.png"), full_page=False)
        page.screenshot(path=str(SHOTS / "v7-full-home-prokshino-1440.png"), full_page=True)
        print("Captured Prokshino Desktop 1440px")
        
        # Interactive selector action on Prokshino
        page.locator('#service-selection').scroll_into_view_if_needed()
        page.wait_for_timeout(400)
        page.screenshot(path=str(SHOTS / "v7-selector-prokshino-1440.png"))
        print("Captured Prokshino Selector 1440px")
        
        # Click on another category in selector, e.g. "hygiene"
        hygiene_btn = page.locator('button.selector-category[data-category-id="hygiene"]')
        if hygiene_btn.count():
            hygiene_btn.click()
            page.wait_for_timeout(300)
            page.screenshot(path=str(SHOTS / "v7-selector-hygiene-active-1440.png"))
            print("Captured Prokshino Hygiene Selector Active 1440px")
            
        # Doctors section
        page.locator('#clinic-team').scroll_into_view_if_needed()
        page.wait_for_timeout(400)
        page.screenshot(path=str(SHOTS / "v7-doctors-prokshino-1440.png"))
        print("Captured Prokshino Doctors 1440px")
        
        # Booking Modal on Prokshino
        page.locator('[data-open-booking]').first.click()
        page.wait_for_timeout(350)
        page.screenshot(path=str(SHOTS / "v7-booking-modal-desktop-1440.png"))
        print("Captured Prokshino Booking Modal 1440px")
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        
        # Ispanskie Kvartaly Home
        page.goto(f"{base}v2/ispanskie/index.html", wait_until="networkidle")
        page.screenshot(path=str(SHOTS / "v7-desktop-home-ispanskie-1440.png"), full_page=False)
        page.screenshot(path=str(SHOTS / "v7-full-home-ispanskie-1440.png"), full_page=True)
        print("Captured Ispanskie Desktop 1440px")
        
        # Booking Modal on Ispanskie (shows Prokshino disclaimer)
        page.locator('[data-open-booking]').first.click()
        page.wait_for_timeout(350)
        page.screenshot(path=str(SHOTS / "v7-booking-modal-ispanskie-1440.png"))
        print("Captured Ispanskie Booking Modal 1440px")
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        
        # Chooser Hub
        page.goto(f"{base}v2/index.html", wait_until="networkidle")
        page.screenshot(path=str(SHOTS / "v7-desktop-chooser-1440.png"), full_page=True)
        print("Captured Chooser Hub 1440px")

        # Prices Page Prokshino
        page.goto(f"{base}v2/prokshino/prices/index.html", wait_until="networkidle")
        page.screenshot(path=str(SHOTS / "v7-desktop-prices-prokshino-1440.png"), full_page=False)
        print("Captured Prices Desktop 1440px")

        # 2. Mobile captures (390px)
        mobile_page = browser.new_page(viewport={"width": 390, "height": 844})
        
        # Prokshino Mobile Home
        mobile_page.goto(f"{base}v2/prokshino/index.html", wait_until="networkidle")
        mobile_page.screenshot(path=str(SHOTS / "v7-mobile-home-prokshino-390.png"), full_page=False)
        mobile_page.screenshot(path=str(SHOTS / "v7-full-home-prokshino-390.png"), full_page=True)
        print("Captured Prokshino Mobile 390px")
        
        # Mobile Menu Open
        menu_toggle = mobile_page.locator('[data-menu-toggle]')
        if menu_toggle.is_visible():
            menu_toggle.click()
            mobile_page.wait_for_timeout(300)
            mobile_page.screenshot(path=str(SHOTS / "v7-mobile-menu-prokshino-390.png"))
            print("Captured Prokshino Mobile Menu 390px")
            menu_toggle.click()
            mobile_page.wait_for_timeout(200)
            
        # Mobile Services Selector
        mobile_page.locator('#service-selection').scroll_into_view_if_needed()
        mobile_page.wait_for_timeout(350)
        mobile_page.screenshot(path=str(SHOTS / "v7-mobile-selector-prokshino-390.png"))
        print("Captured Prokshino Mobile Selector 390px")
        
        # Mobile Booking Modal
        mobile_page.locator('[data-open-booking]').first.click()
        mobile_page.wait_for_timeout(350)
        mobile_page.screenshot(path=str(SHOTS / "v7-mobile-booking-prokshino-390.png"))
        print("Captured Prokshino Mobile Booking Modal 390px")
        mobile_page.keyboard.press("Escape")
        mobile_page.wait_for_timeout(200)
        
        # Ispanskie Mobile Home
        mobile_page.goto(f"{base}v2/ispanskie/index.html", wait_until="networkidle")
        mobile_page.screenshot(path=str(SHOTS / "v7-mobile-home-ispanskie-390.png"), full_page=False)
        mobile_page.screenshot(path=str(SHOTS / "v7-full-home-ispanskie-390.png"), full_page=True)
        print("Captured Ispanskie Mobile 390px")

        # 3. Responsive Measurement Matrix across 10 viewports
        overflow_issues = []
        for vp in viewports:
            meas_page = browser.new_page(viewport={"width": vp, "height": 900})
            for branch in ["prokshino", "ispanskie"]:
                meas_page.goto(f"{base}v2/{branch}/index.html", wait_until="networkidle")
                doc_width = meas_page.evaluate("Math.max(document.documentElement.scrollWidth, document.body.scrollWidth)")
                win_width = meas_page.evaluate("window.innerWidth")
                if doc_width > win_width + 1:
                    overflow_issues.append({"branch": branch, "viewport": vp, "doc_width": doc_width, "win_width": win_width})
            meas_page.close()
            
        print("RESPONSIVE_CHECK:", "PASSED (0 overflows)" if not overflow_issues else f"ISSUES: {overflow_issues}")
        
        browser.close()
        
    server.shutdown()
    print("ALL VISUAL CAPTURES FINISHED SUCCESSFULLY!")

if __name__ == "__main__":
    capture_all()
