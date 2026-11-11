import os
import sys
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(BASE_DIR, "index.html")
FILE_URL = f"file:///{HTML_PATH.replace(os.sep, '/')}"

def run_deep_audit():
    print(f"Auditing Dental Atlas: {FILE_URL}")
    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # 1. Edge Case: Invalid URL params fallback
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(f"{FILE_URL}?branch=unknown123&view=alienView&cat=ghostCat&id=nonExistentProc")
        page.wait_for_load_state("domcontentloaded")
        
        search_after_invalid = page.evaluate("() => window.location.search")
        branch_badge = page.locator("#brandBranchBadge").text_content().strip()
        active_tab = page.locator(".pathway-btn.is-active").text_content().strip()
        stage_title = page.locator("#stageProcTitle").text_content().strip()
        
        print("\n--- Test 1: Fallback for Invalid URL parameters ---")
        print(f"URL search on invalid param: '{search_after_invalid}'")
        print(f"Branch badge: '{branch_badge}'")
        print(f"Active tab: '{active_tab}'")
        print(f"Stage procedure title: '{stage_title}'")
        results['fallback_invalid_params'] = {
            'branch': branch_badge,
            'tab': active_tab,
            'title': stage_title
        }

        # Check if URL was normalized via replaceState as stated in docs (PRODUCT_BLUEPRINT.md line 82: 'URL нормализуется через history.replaceState')
        # In engine, parseUrlState() sets state, but does it call syncUrl(true)?
        print(f"Did URL replaceState normalize invalid params in address bar? Current search: '{search_after_invalid}'")
        results['url_normalized_on_load'] = (search_after_invalid != "?branch=unknown123&view=alienView&cat=ghostCat&id=nonExistentProc")

        # 2. Browser History (pushState & popstate)
        print("\n--- Test 2: Browser History (pushState & popstate) ---")
        page.goto(FILE_URL)
        page.wait_for_load_state("domcontentloaded")
        
        page.locator('[data-pathway="doctors"]').click()
        url_after_doctors = page.evaluate("() => window.location.search")
        
        page.locator('[data-pathway="booking"]').click()
        url_after_booking = page.evaluate("() => window.location.search")
        
        page.go_back()
        url_after_back1 = page.evaluate("() => window.location.search")
        visible_view1 = page.evaluate("() => document.querySelector('.atlas-view.is-visible')?.id")
        
        page.go_back()
        url_after_back2 = page.evaluate("() => window.location.search")
        visible_view2 = page.evaluate("() => document.querySelector('.atlas-view.is-visible')?.id")
        
        print(f"Step 1 (Doctors): {url_after_doctors}")
        print(f"Step 2 (Booking): {url_after_booking}")
        print(f"Back 1: URL={url_after_back1}, visibleView={visible_view1}")
        print(f"Back 2: URL={url_after_back2}, visibleView={visible_view2}")
        results['history'] = {
            'back1_view': visible_view1,
            'back2_view': visible_view2
        }

        # 3. Doctors View: Deep Link & Dossier
        print("\n--- Test 3: Doctor Deep Link & Dossier Focus ---")
        page.goto(f"{FILE_URL}?branch=ispanskie&view=doctors&id=danielyan")
        page.wait_for_load_state("domcontentloaded")
        
        # Check if any doctor is highlighted, focused or dossier expanded
        doctor_cards = page.locator(".doctor-card")
        doc_count = doctor_cards.count()
        print(f"Total doctor cards rendered: {doc_count}")
        
        # Check if cards contain education, certificates, or clickable procedure tags
        card_html = doctor_cards.first.inner_html()
        has_education = "AVS school" in card_html or "РНИМУ" in card_html or "МГМСУ" in card_html or "образовани" in card_html.lower()
        has_certificates = "сертификат" in card_html.lower() or "osstem" in card_html.lower()
        has_proc_chips = page.locator(".doctor-card [data-proc-link]").count()
        print(f"First doctor card has education: {has_education}")
        print(f"First doctor card has certificates: {has_certificates}")
        print(f"Doctor cards clickable procedure chips count: {has_proc_chips}")

        # 4. Service Scene -> Doctor Dossier Transition
        print("\n--- Test 4: Service Scene -> Doctor Dossier Transition ---")
        page.goto(f"{FILE_URL}?branch=ispanskie&view=services&cat=implants&id=straumann-implant")
        page.wait_for_load_state("domcontentloaded")
        
        doc_profile_btn = page.locator("#stageDocProfileBtn")
        if doc_profile_btn.count() > 0:
            doc_profile_btn.click()
            url_after_doc_click = page.evaluate("() => window.location.search")
            visible_view_doc = page.evaluate("() => document.querySelector('.atlas-view.is-visible')?.id")
            print(f"After click 'Профиль врача': URL={url_after_doc_click}, visibleView={visible_view_doc}")
            results['doc_profile_click'] = {
                'url': url_after_doc_click,
                'view': visible_view_doc
            }
        else:
            print("ERROR: #stageDocProfileBtn not found!")

        # 5. Mobile Tap Target Sizes (390px)
        print("\n--- Test 5: Mobile Tap Targets & UI metrics (390px) ---")
        page_m = browser.new_page(viewport={"width": 390, "height": 844})
        page_m.goto(f"{FILE_URL}?branch=ispanskie&view=services")
        page_m.wait_for_load_state("domcontentloaded")

        interactive_selectors = [
            "#switchBranchIspanskie",
            "#switchBranchProkshino",
            ".pathway-btn",
            ".nav-cat-btn",
            ".nav-proc-btn",
            "#stageBookBtn",
            "#mobileFloatCall",
            "#mobileFloatBook"
        ]

        tap_target_report = []
        for sel in interactive_selectors:
            locs = page_m.locator(sel)
            for i in range(min(locs.count(), 3)):
                box = locs.nth(i).bounding_box()
                if box:
                    w, h = box["width"], box["height"]
                    ok = w >= 40 and h >= 36 # Minimum guideline for touch targets
                    tap_target_report.append({"selector": f"{sel}[{i}]", "width": round(w, 1), "height": round(h, 1), "pass": ok})
        
        for t in tap_target_report:
            print(f"[{'PASS' if t['pass'] else 'WARN'}] {t['selector']}: {t['width']}x{t['height']}px")

        # 6. Check Mobile Floating Bar overlap
        print("\n--- Test 6: Mobile Floating Bar Overlap Check ---")
        body_padding_bottom = page_m.evaluate("() => parseFloat(window.getComputedStyle(document.body).paddingBottom)")
        float_bar_height = page_m.evaluate("() => document.querySelector('.mobile-action-float')?.offsetHeight || 0")
        print(f"document.body padding-bottom: {body_padding_bottom}px, float bar height: {float_bar_height}px")
        results['float_bar_overlap'] = {
            'body_padding_bottom': body_padding_bottom,
            'float_bar_height': float_bar_height,
            'protected': body_padding_bottom >= float_bar_height
        }
        print(f"Protected against content masking: {results['float_bar_overlap']['protected']}")

        # 7. Accessibility Audit
        print("\n--- Test 7: Accessibility Elements & Attributes ---")
        modal_role = page.evaluate("() => document.querySelector('#bookingModal')?.getAttribute('role')")
        modal_aria_modal = page.evaluate("() => document.querySelector('#bookingModal')?.getAttribute('aria-modal')")
        tablist_count = page.evaluate("() => document.querySelectorAll('[role=\"tablist\"]').length")
        tab_count = page.evaluate("() => document.querySelectorAll('[role=\"tab\"]').length")
        main_role = page.evaluate("() => document.querySelector('main')?.tagName")
        h1_count = page.evaluate("() => document.querySelectorAll('h1').length")
        
        print(f"Modal role={modal_role}, aria-modal={modal_aria_modal}")
        print(f"tablists count: {tablist_count}, tabs count: {tab_count}")
        print(f"Main tag: {main_role}, H1 tag count: {h1_count}")

        browser.close()

if __name__ == "__main__":
    run_deep_audit()


def check_aria_and_focus():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(FILE_URL)
        
        cat_btns = page.evaluate("""() => {
            const catList = document.querySelector('#categoryList');
            const btns = Array.from(catList.querySelectorAll('button'));
            return btns.map(b => ({
                role: b.getAttribute('role'),
                ariaSelected: b.getAttribute('aria-selected')
            }));
        }""")
        print("\n--- Test 8: ARIA tablist/tab structure ---")
        print("Category buttons ARIA:", cat_btns[:3])

        proc_btns = page.evaluate("""() => {
            const procList = document.querySelector('#procedureList');
            const btns = Array.from(procList.querySelectorAll('button'));
            return btns.map(b => ({
                role: b.getAttribute('role'),
                ariaSelected: b.getAttribute('aria-selected')
            }));
        }""")
        print("Procedure buttons ARIA:", proc_btns[:3])

        # Modal focus trapping
        print("\n--- Test 9: Modal Focus Trap ---")
        page.locator("#stageBookBtn").click()
        page.wait_for_timeout(200)

        tabs_outside = False
        tab_trail = []
        for _ in range(12):
            page.keyboard.press("Tab")
            is_inside_modal = page.evaluate("() => { const el = document.activeElement; return el ? Boolean(el.closest('#bookingModal')) : false; }")
            el_desc = page.evaluate("() => document.activeElement ? (document.activeElement.tagName + '#' + document.activeElement.id + '.' + document.activeElement.className) : 'none'")
            tab_trail.append((el_desc, is_inside_modal))
            if not is_inside_modal:
                tabs_outside = True

        print("Focus leaked outside modal:", tabs_outside)
        print("Tab trail (first 5):", tab_trail[:5])
        browser.close()

if __name__ == "__main__":
    check_aria_and_focus()


def check_images():
    import re
    data_js = os.path.join(BASE_DIR, "assets", "js", "atlas-data.js")
    with open(data_js, "r", encoding="utf-8") as f:
        content = f.read()
    
    paths = re.findall(r'[\'"](\.\./design/[^\'"]+)[\'"]', content)
    print("\n--- Test 10: Asset Path Verification ---")
    print(f"Total image references found: {len(paths)}")
    missing = []
    for p in set(paths):
        full_p = os.path.normpath(os.path.join(BASE_DIR, p))
        if not os.path.exists(full_p):
            missing.append(p)
    print(f"Missing image files: {len(missing)}")
    if missing:
        for m in missing:
            print("  404 FILE NOT FOUND:", m)
    else:
        print("  All referenced image assets exist on disk.")

if __name__ == "__main__":
    check_images()
