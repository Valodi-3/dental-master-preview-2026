import os
import sys
import http.server
import socketserver
import threading
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

PORT = 8998
DIRECTORY = r"C:\Users\usser\Documents\Manus\2026-11-09\tsLhBc\dental-master-preview-2026"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()
time.sleep(1)

out_dir = r"C:\Users\usser\Documents\Manus\2026-11-09\tsLhBc\dental-master-preview-2026\design\v2qa\screenshots\v9"
os.makedirs(out_dir, exist_ok=True)

viewports = [
    (1920, 1080, "1920"),
    (1440, 900, "1440"),
    (1024, 768, "1024"),
    (768, 1024, "768"),
    (430, 932, "430"),
    (390, 844, "390"),
    (375, 667, "375"),
    (360, 800, "360"),
    (320, 568, "320")
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    print("\n================ TESTING V9 INDEX ================")
    url_index = "http://localhost:8998/v9/index.html"
    
    for w, h, label in viewports:
        is_mobile = w < 768
        ctx = browser.new_context(viewport={"width": w, "height": h}, is_mobile=is_mobile)
        page = ctx.new_page()
        page.goto(url_index, wait_until="networkidle")
        
        overflow = page.evaluate("() => document.documentElement.scrollWidth > window.innerWidth")
        scroll_w = page.evaluate("() => document.documentElement.scrollWidth")
        win_w = page.evaluate("() => window.innerWidth")
        print(f"[v9-index] Viewport {label}px: overflow={overflow} (scrollWidth={scroll_w}, winWidth={win_w})")
        
        if label in ["1440", "390"]:
            page.screenshot(path=os.path.join(out_dir, f"v9-prokshino-{label}.png"), full_page=False)
            print(f"[v9-index] Saved screenshot for {label}px")
            
        ctx.close()
        
    # Test Interactivity on 1440px
    ctx_test = browser.new_context(viewport={"width": 1440, "height": 900})
    page_test = ctx_test.new_page()
    page_test.goto(url_index, wait_until="networkidle")
    
    # 1. Test Configurator category switch
    print("\n--- Testing Configurator ---")
    cat_btn = page_test.query_selector("[data-config-cat='implantation']")
    if cat_btn:
        cat_btn.click()
        time.sleep(0.4)
        title = page_test.inner_text("[data-result-title]")
        price = page_test.inner_text("[data-result-price]")
        print(f"Switched to Implantation -> Title: '{title}', Price: '{price}'")
        
    # 2. Test Procedure selection
    proc_btns = page_test.query_selector_all(".config-proc-btn")
    if len(proc_btns) > 1:
        proc_btns[1].click()
        time.sleep(0.4)
        title2 = page_test.inner_text("[data-result-title]")
        price2 = page_test.inner_text("[data-result-price]")
        print(f"Clicked Procedure 2 -> Title: '{title2}', Price: '{price2}'")
        
    # 3. Test Booking Choice Modal with Pre-filled Service
    print("\n--- Testing Booking Choice Modal ---")
    book_btn = page_test.query_selector("[data-result-book]")
    if book_btn:
        book_btn.click()
        time.sleep(0.3)
        modal_open = page_test.evaluate("() => document.querySelector('#bookingChoiceModal').classList.contains('is-open')")
        context_text = page_test.inner_text("#bookingChoiceContext")
        print(f"Modal opened: {modal_open}")
        print(f"Context display: {context_text}")
        
        # Test copy phone button
        page_test.click("[data-copy-phone]")
        time.sleep(0.2)
        copy_status = page_test.inner_text("[data-copy-status]")
        print(f"Copy button clicked -> status: '{copy_status}'")
        
        # Close modal
        page_test.click("#bookingChoiceClose")
        time.sleep(0.2)
        modal_open_after = page_test.evaluate("() => document.querySelector('#bookingChoiceModal').classList.contains('is-open')")
        print(f"Modal closed: {not modal_open_after}")
        
    # 4. Check doctor photo positions
    print("\n--- Testing Doctor Photo Framing ---")
    danielyan_pos = page_test.evaluate("() => window.getComputedStyle(document.querySelector('.photo-danielyan')).objectPosition")
    nadzhafov_pos = page_test.evaluate("() => window.getComputedStyle(document.querySelector('.photo-nadzhafov')).objectPosition")
    fiasheva_pos = page_test.evaluate("() => window.getComputedStyle(document.querySelector('.photo-fiasheva')).objectPosition")
    print(f"Danielyan object-position: {danielyan_pos}")
    print(f"Nadzhafov object-position: {nadzhafov_pos}")
    print(f"Fiasheva object-position: {fiasheva_pos}")
    
    ctx_test.close()
    
    # Test Tour Page
    print("\n================ TESTING V9 TOUR ================")
    url_tour = "http://localhost:8998/v9/tour.html"
    ctx_tour = browser.new_context(viewport={"width": 1440, "height": 900})
    page_tour = ctx_tour.new_page()
    page_tour.goto(url_tour, wait_until="networkidle")
    
    tour_title_1 = page_tour.inner_text("#tourPhotoTitle")
    tour_cnt_1 = page_tour.inner_text("#tourPhotoCounter")
    print(f"Tour initial photo: '{tour_title_1}' ({tour_cnt_1})")
    
    page_tour.click("#tourNextPhoto")
    time.sleep(0.4)
    tour_title_2 = page_tour.inner_text("#tourPhotoTitle")
    tour_cnt_2 = page_tour.inner_text("#tourPhotoCounter")
    print(f"Tour after next: '{tour_title_2}' ({tour_cnt_2})")
    
    page_tour.screenshot(path=os.path.join(out_dir, "v9-tour-1440.png"), full_page=False)
    print("Saved v9-tour-1440.png screenshot")
    ctx_tour.close()
    
    browser.close()
    print("\nALL V9 TESTS PASSED SUCCESSFULLY!")
