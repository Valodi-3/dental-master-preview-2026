from playwright.sync_api import sync_playwright
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(BASE_DIR, "index.html")
url = f"file:///{HTML_PATH.replace(os.sep, '/')}"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto(url + '?branch=ispanskie&view=doctors&id=danielyan')
    page.wait_for_load_state('domcontentloaded')
    
    # Check is-selected-doctor class and badge
    card = page.locator('#doctor-danielyan')
    has_sel_class = 'is-selected-doctor' in card.get_attribute('class')
    badge_text = card.locator('.doctor-selected-badge').text_content()
    print('Doctor danielyan selected class:', has_sel_class, 'badge:', badge_text)
    
    # Click procedure chip
    chip = card.locator('[data-proc-link]').first
    chip_text = chip.text_content().strip()
    chip.click()
    page.wait_for_timeout(100)
    
    view_after_chip = page.evaluate("() => document.querySelector('.atlas-view.is-visible')?.id")
    url_after_chip = page.evaluate("() => window.location.search")
    proc_title = page.locator('#stageProcTitle').text_content().strip()
    print('After chip click:', 'view:', view_after_chip, 'URL:', url_after_chip, 'title:', proc_title)
    
    # Check mobile float is-hidden on modal
    page_m = browser.new_page(viewport={'width': 390, 'height': 844})
    page_m.goto(url)
    page_m.wait_for_load_state('domcontentloaded')
    page_m.locator('#stageBookBtn').click()
    page_m.wait_for_timeout(100)
    
    float_hidden = page_m.evaluate("() => document.querySelector('.mobile-action-float')?.classList.contains('is-hidden')")
    print('Mobile float has is-hidden when modal open:', float_hidden)
    
    page_m.keyboard.press('Escape')
    page_m.wait_for_timeout(100)
    float_restored = page_m.evaluate("() => !document.querySelector('.mobile-action-float')?.classList.contains('is-hidden')")
    print('Mobile float restored when modal closed:', float_restored)

    browser.close()
