import sys
import os
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(BASE_DIR, "index.html")
FILE_URL = f"file:///{HTML_PATH.replace(os.sep, '/')}"

test_width = int(sys.argv[1]) if len(sys.argv) > 1 else 320

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": test_width, "height": 640})
    page.goto(FILE_URL)
    page.wait_for_load_state("domcontentloaded")
    
    # Disable overflow-x
    page.evaluate("""() => {
        const style = document.createElement('style');
        style.textContent = '* { overflow-x: visible !important; }';
        document.head.appendChild(style);
    }""")
    
    scroll_w = page.evaluate("() => document.documentElement.scrollWidth")
    print(f"Viewport: {test_width}px, scrollWidth: {scroll_w}px")
    
    culprits = page.evaluate("""() => {
        const docWidth = window.innerWidth;
        const res = [];
        for (const el of document.querySelectorAll('*')) {
            const rect = el.getBoundingClientRect();
            if (rect.right > docWidth + 1 || rect.width > docWidth + 1) {
                res.push({
                    tag: el.tagName,
                    cls: el.className,
                    id: el.id,
                    w: Math.round(rect.width),
                    r: Math.round(rect.right),
                    text: el.innerText ? el.innerText.slice(0, 30).replace(/\\n/g, ' ') : ''
                });
            }
        }
        return res;
    }""")
    
    print(f"Found {len(culprits)} overflowing elements:")
    for c in culprits[:20]:
        print(f" - <{c['tag']} class='{c['cls']}' id='{c['id']}'> w={c['w']}px, r={c['r']}px: '{c['text']}'")
        
    browser.close()
