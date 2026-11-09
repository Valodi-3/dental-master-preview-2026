from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from playwright.sync_api import sync_playwright
from design.v2_visual_qa import start_server

WIDTHS = (320, 360, 390)
BRANCHES = ("prokshino", "ispanskie")


def main() -> None:
    server, base = start_server()
    results = []
    failures = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            for branch in BRANCHES:
                for width in WIDTHS:
                    page = browser.new_page(viewport={"width": width, "height": 920})
                    page.goto(f"{base}/v2/{branch}/directions/index.html", wait_until="networkidle")
                    page.wait_for_function("window.DENTAL_V2 && document.querySelectorAll('[data-selector-categories] button').length === 10")
                    all_chips = []
                    for category in page.locator("[data-selector-categories] button").all():
                        category.click()
                        page.wait_for_timeout(20)
                        chips = page.locator(".procedure-option").evaluate_all("els => els.map(b => { const p=b.querySelector('b'); const r=p.getBoundingClientRect(); const s=getComputedStyle(p); return {text:p.textContent, height:r.height, lineHeight:parseFloat(s.lineHeight)||parseFloat(s.fontSize)*1.2, whiteSpace:s.whiteSpace, currency:p.textContent.includes('₽')}; })")
                        all_chips.extend(chips)
                    broken = [x for x in all_chips if x["whiteSpace"] != "nowrap" or x["height"] > x["lineHeight"] * 1.35 or not x["currency"]]
                    record = {"branch": branch, "width": width, "chips": len(all_chips), "brokenPriceLabels": broken}
                    results.append(record)
                    if broken:
                        failures.append(record)
                    page.close()
            browser.close()
    finally:
        server.shutdown()
    output = ROOT / "design" / "v2qa" / "polish-currency-results.json"
    output.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(x["chips"] for x in results)
    print(f"SELECTOR_CURRENCY_QA {'FAIL' if failures else 'PASS'} cases={len(results)} categoryChipPriceLabels={total} failures={len(failures)}")
    if failures:
        print(json.dumps(failures, ensure_ascii=False, indent=2))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
