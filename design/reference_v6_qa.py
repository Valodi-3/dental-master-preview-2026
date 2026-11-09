from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "design" / "v2qa"
SHOTS = QA / "screenshots"
WIDTHS = (320, 360, 375, 390, 430, 768, 1024, 1440, 1920)
HEIGHT = 900
sys.path.insert(0, str(ROOT))
from playwright.sync_api import sync_playwright
from design.v2_visual_qa import route_list, start_server


def fail(message: str) -> None:
    raise AssertionError(message)


def static_check() -> dict:
    css_path = ROOT / "v2" / "assets" / "reference-v6.css"
    if not css_path.is_file():
        fail("V6 stylesheet is missing")
    css = css_path.read_text(encoding="utf-8")
    forbidden = ("@import", "fonts.googleapis.com", "fonts.gstatic.com", "cdnjs.cloudflare.com", "unpkg.com")
    if any(token in css for token in forbidden):
        fail("V6 stylesheet contains an external font/library dependency")
    if "--paper: #e8dfd1" not in css or "--leaf-dark: #173a30" not in css:
        fail("warm paper / forest palette tokens are missing")
    generator = (ROOT / "design" / "build_v2.py").read_text(encoding="utf-8")
    if 'reference-v6.css' not in generator:
        fail("generator does not include the V6 stylesheet")
    manifest = json.loads((ROOT / "v2" / "route-manifest.json").read_text(encoding="utf-8"))
    routes = route_list()
    if len(routes) != 41:
        fail(f"expected 41 V2 routes, found {len(routes)}")
    missing = []
    for label, rel in routes:
        page = ROOT / "v2" / rel.removeprefix("v2/")
        if not page.is_file():
            missing.append(f"{label}: missing {page.relative_to(ROOT)}")
            continue
        text = page.read_text(encoding="utf-8")
        if "reference-v6.css" not in text:
            missing.append(f"{label}: no V6 stylesheet link")
        for match in __import__("re").findall(r'<link[^>]+href="([^"]*reference-v6\.css)"', text):
            css_rel = match.replace("\\", "/")
            if not (page.parent / css_rel).resolve().is_file():
                missing.append(f"{label}: CSS path broken: {match}")
    if missing:
        fail("; ".join(missing[:15]))
    hub = (ROOT / "index.html").read_text(encoding="utf-8")
    if "reference-v6.css" not in hub or "v2/prokshino/index.html" not in hub or "v2/ispanskie/index.html" not in hub:
        fail("root preview hub does not load V6 or link both branches")
    clinics = json.loads((ROOT / "v2" / "data" / "clinic-content.json").read_text(encoding="utf-8"))["branches"]
    for branch, info in clinics.items():
        home = (ROOT / "v2" / branch / "index.html").read_text(encoding="utf-8")
        hero = home.split('<section class="section-shell clinic-strip"', 1)[0]
        if 'id="welcome-title"' not in hero or "Добро пожаловать" not in hero:
            fail(f"{branch}: welcome-first hero is missing")
        if "data-open-booking" in hero or "data-selector" in hero or "doctor-carousel-card" in hero:
            fail(f"{branch}: the welcome hero contains a booking pitch, selector or staff cards")
        expected_order = [home.find('id="clinic-space"'), home.find('id="clinic-team"'), home.find('id="service-selection"')]
        if min(expected_order) < 0 or expected_order != sorted(expected_order):
            fail(f"{branch}: section order should be clinic → team → services")
        if info["welcomeImage"] not in hero:
            fail(f"{branch}: the official clinic photo is missing from welcome hero")
        for asset in [info["welcomeImage"], *(item["src"] for item in info["gallery"])]:
            if not (ROOT / asset).is_file():
                fail(f"{branch}: missing local official image {asset}")
    diff = __import__("subprocess").run(["git", "diff", "--quiet", "HEAD", "--", "app.js"], cwd=ROOT)
    if diff.returncode != 0:
        fail("shared app.js must remain untouched")
    return {"routes": len(routes), "stylesheet": "v2/assets/reference-v6.css", "externalDependencies": 0, "localOfficialClinicImages": True, "appJsUntouched": True}


def responsive_check(make_screens: bool = True) -> dict:
    SHOTS.mkdir(parents=True, exist_ok=True)
    server, base = start_server()
    errors: list[str] = []
    metrics: list[dict] = []
    screenshot_dimensions: dict[str, list[int]] = {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 390, "height": HEIGHT}, device_scale_factor=1)
            for width in WIDTHS:
                page.set_viewport_size({"width": width, "height": HEIGHT})
                page.emulate_media(reduced_motion="reduce")
                for label, route in route_list():
                    response = page.goto(urljoin(base, route), wait_until="load", timeout=45000)
                    if response is None or response.status >= 400:
                        errors.append(f"{label}/{width}: response={response.status if response else 'none'}")
                        continue
                    try:
                        page.wait_for_function("window.DENTAL_V2 && document.readyState==='complete'", timeout=12000)
                    except Exception:
                        errors.append(f"{label}/{width}: app data did not initialize")
                    style_state = page.evaluate("""() => {
                      const body = getComputedStyle(document.body);
                      const css = [...document.styleSheets].some(s => (s.href || '').includes('reference-v6.css'));
                      const paper = getComputedStyle(document.documentElement).getPropertyValue('--paper').trim();
                      const home=!!document.querySelector('.home-welcome');
                      const selector=document.querySelector('.selector-section');
                      const title=document.querySelector('.selector-section .section-heading-row h2');
                      const welcome=document.querySelector('.home-welcome');
                      const welcomeTitle=document.querySelector('.home-welcome h1');
                      const track=document.querySelector('.doctor-carousel-track');
                      return {css, paper, bg:body.backgroundColor, width:Math.max(document.documentElement.scrollWidth,document.body.scrollWidth), viewport:innerWidth,
                        selectorBg:selector?getComputedStyle(selector).backgroundColor:null, selectorText:title?getComputedStyle(title).color:null,
                        welcomeBg:welcome?getComputedStyle(welcome).backgroundImage:null, welcomeText:welcomeTitle?getComputedStyle(welcomeTitle).color:null,
                        carousel:track?getComputedStyle(track).display:null,
                        hero:!!document.querySelector('.home-welcome'), fab:!!document.querySelector('.booking-fab'),
                        fabBox:(()=>{const e=document.querySelector('.booking-fab'); if(!e)return null;const r=e.getBoundingClientRect(); return {position:getComputedStyle(e).position,left:r.left,right:r.right,bottom:r.bottom}})()};
                    }""")
                    if not style_state["css"] or style_state["paper"] != "#e8dfd1":
                        errors.append(f"{label}/{width}: V6 stylesheet or warm paper token did not load: {style_state}")
                    if style_state["width"] > width + 1:
                        errors.append(f"{label}/{width}: horizontal overflow {style_state['width']}")
                    if label.startswith("home-"):
                        if style_state["selectorBg"] != "rgb(39, 69, 54)" or style_state["selectorText"] != "rgb(244, 236, 223)":
                            errors.append(f"{label}/{width}: selector contrast/theme regression: bg={style_state['selectorBg']} text={style_state['selectorText']}")
                        if style_state["carousel"] != "flex":
                            errors.append(f"{label}/{width}: doctor carousel is not a horizontal flex track")
                        if label == "home-ispanskie" and ("112deg" not in (style_state["welcomeBg"] or "") or style_state["welcomeText"] != "rgb(48, 40, 32)"):
                            errors.append(f"{label}/{width}: warm welcome hero contrast regression")
                    branch_route = "/v2/prokshino/" in f"/{route}" or "/v2/ispanskie/" in f"/{route}"
                    if branch_route:
                        fab = style_state["fabBox"]
                        if not fab or fab["position"] != "fixed" or fab["left"] < -1 or fab["right"] > width + 1 or fab["bottom"] > HEIGHT + 1:
                            errors.append(f"{label}/{width}: booking FAB not visible inside viewport: {fab}")
                    if style_state["hero"]:
                        hero_state = page.locator(".home-welcome").evaluate("e=>{const r=e.getBoundingClientRect();return {left:r.left,right:r.right,width:r.width}}")
                        if hero_state["left"] < -.5 or hero_state["right"] > width + .5:
                            errors.append(f"{label}/{width}: hero bounding box escapes viewport: {hero_state}")
                    broken = page.evaluate("() => [...document.images].filter(i=>i.complete && i.naturalWidth===0).map(i=>i.currentSrc)")
                    if broken:
                        errors.append(f"{label}/{width}: broken images {broken[:3]}")
                    metrics.append({"route": label, "width": width, "scrollWidth": style_state["width"], "paperToken": style_state["paper"], "bookingBounds": style_state["fabBox"] if branch_route else None})
                    if make_screens and width in (390, 1440) and label.startswith("home-"):
                        branch = "prokshino" if label.endswith("prokshino") else "ispanskie"
                        page.evaluate("""() => {for(const im of document.images){im.loading='eager'; if(!im.complete) im.setAttribute('fetchpriority','high');} }""")
                        page.wait_for_timeout(350)
                        try:
                            page.evaluate("() => document.fonts.ready")
                        except Exception:
                            pass
                        if width == 390:
                            full = SHOTS / f"v6-full-home-{branch}-390.png"
                            page.screenshot(path=str(full), full_page=True, animations="disabled")
                            screenshot_dimensions[full.name] = [390, page.evaluate("document.documentElement.scrollHeight")]
                        else:
                            top = SHOTS / f"v6-home-{branch}-desktop-1440.png"
                            full = SHOTS / f"v6-full-home-{branch}-1440.png"
                            page.screenshot(path=str(top), full_page=False, animations="disabled")
                            page.screenshot(path=str(full), full_page=True, animations="disabled")
                            height = page.evaluate("document.documentElement.scrollHeight")
                            screenshot_dimensions[top.name] = [1440, HEIGHT]
                            screenshot_dimensions[full.name] = [1440, height]
            browser.close()
    finally:
        server.shutdown()
    failed = [x for x in metrics if x["scrollWidth"] > x["width"] + 1]
    if errors:
        out = QA / "reference-v6-responsive-errors.json"
        out.write_text(json.dumps({"status":"FAIL","errors":errors,"metrics":metrics},ensure_ascii=False,indent=2),encoding="utf-8")
        raise AssertionError("; ".join(errors[:20]))
    report = {"status":"PASS","routes":len(route_list()),"widths":list(WIDTHS),"checks":len(metrics),"horizontalOverflow":0,"brokenImages":0,"v6Stylesheet":True,"bookingButtonBounds":"inside viewport on every clinic page","screenshots":screenshot_dimensions,"metrics":metrics}
    out = QA / "reference-v6-responsive.json"
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    return {"checks":len(metrics),"routes":report["routes"],"widths":len(WIDTHS),"screenshots":screenshot_dimensions,"report":out.relative_to(ROOT).as_posix()}


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--static", action="store_true")
    parser.add_argument("--responsive", action="store_true")
    parser.add_argument("--all", action="store_true")
    args=parser.parse_args()
    static = args.static or args.all or not (args.responsive or args.static)
    responsive = args.responsive or args.all
    if static:
        result=static_check()
        print(f"V6_STYLE_PASS routes={result['routes']} externalDependencies=0 localOfficialClinicImages=true appJsUntouched=true")
    if responsive:
        result=responsive_check()
        print(f"V6_RESPONSIVE_PASS routes={result['routes']} widths={result['widths']} checks={result['checks']} screenshots={len(result['screenshots'])} report={result['report']}")


if __name__ == "__main__":
    main()
