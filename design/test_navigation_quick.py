import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

def test_quick():
    server = ThreadingHTTPServer(("127.0.0.1", 0), lambda *args, **kwargs: QuietHandler(*args, directory=str(ROOT), **kwargs))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}/"
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # --- 1. Desktop 1440px ---
        d_page = browser.new_page(viewport={"width": 1440, "height": 900})
        d_page.goto(f"{base}v2/prokshino/index.html", wait_until="networkidle")
        
        # Test navigation
        assert d_page.locator("nav.primary-nav a[href*='prices']").count() == 1, "nav link missing"
        
        # Test selector switching
        d_page.locator("#service-selection").scroll_into_view_if_needed()
        hygiene = d_page.locator('button.selector-category[data-category-id="hygiene"]')
        hygiene.click()
        d_page.wait_for_timeout(200)
        assert d_page.locator("[data-selector-category]").inner_text().strip().startswith("ПРОФЕССИОНАЛЬНАЯ"), "category not updated"
        
        # Test booking modal
        d_page.locator("[data-open-booking]").first.click()
        d_page.wait_for_timeout(200)
        assert d_page.locator("dialog.booking-dialog").evaluate("d => d.open") == True, "dialog not open"
        assert d_page.locator("a[href*='online-zapis']").is_visible(), "online button not visible"
        d_page.keyboard.press("Escape")
        d_page.wait_for_timeout(200)
        assert d_page.locator("dialog.booking-dialog").evaluate("d => d.open") == False, "dialog not closed"
        d_page.close()
        print("DESKTOP_1440_CHECK: PASSED")
        
        # --- 2. Mobile 390px ---
        m_page = browser.new_page(viewport={"width": 390, "height": 844})
        m_page.goto(f"{base}v2/prokshino/index.html", wait_until="networkidle")
        
        # Check hero CTA visible & smart FAB hidden
        assert m_page.locator("[data-hero-cta]").is_visible(), "hero CTA not visible"
        m_page.wait_for_timeout(300)
        fab_hidden = m_page.locator(".booking-fab").evaluate("el => el.classList.contains('is-hidden')")
        assert fab_hidden == True, "FAB not hidden when hero CTA is visible"
        
        # Test mobile menu toggle
        m_page.locator("[data-menu-toggle]").click()
        assert m_page.locator("nav.primary-nav").evaluate("nav => nav.classList.contains('is-open')") == True, "menu not opened"
        m_page.locator("[data-menu-toggle]").click()
        
        # Test mobile selector switching
        m_page.locator("#service-selection").scroll_into_view_if_needed()
        consult = m_page.locator('button.selector-category[data-category-id="consultations"]')
        consult.click()
        m_page.wait_for_timeout(200)
        assert m_page.locator("[data-selector-category]").inner_text().strip().startswith("КОНСУЛЬТАЦИИ"), "mobile category not updated"
        
        # Test mobile bottom sheet booking dialog
        m_page.locator(".selected-actions [data-open-booking]").click()
        m_page.wait_for_timeout(200)
        assert m_page.locator("dialog.booking-dialog").evaluate("d => d.open") == True, "mobile dialog not open"
        # Verify pre-selected service display in dialog
        service_display = m_page.locator("[data-booking-service]")
        assert service_display.is_visible() == True, "pre-selected service not displayed in dialog"
        m_page.keyboard.press("Escape")
        m_page.wait_for_timeout(200)
        assert m_page.locator("dialog.booking-dialog").evaluate("d => d.open") == False, "mobile dialog not closed"
        m_page.close()
        print("MOBILE_390_CHECK: PASSED")
        
        browser.close()
    server.shutdown()
    print("QUICK_VERIFICATION_COMPLETE: ALL PASSED")

if __name__ == "__main__":
    test_quick()
