# Gates: Dental Master V2 and responsive/booking regression fixes

OWNS: `index.html`, `prokshino.html`, `ispanskie.html`, `prokshino.css`, `ispanskie.css`, `design/**`, `docs/V2_*`, `v2/**`, `GATES.md`.

Scope: Preserve the complete V1 visual design, local verified media and both 254-item price lists; keep V1 pages reachable from the V2-first local hub. Resolve or verify the reported issues against the actual design branch, execute the exact 30-case QA suite from `origin/tech/dental-master-foundation-2026` without modifying that foundation, and create a Draft PR only. Do not modify `app.js`, tech-branch tests, WordPress, production sites, `main`, Pages settings, or merge/deploy.

- [x] G1: V2 chooser and both clinic sites expose a navigable multi-page information architecture; all 41 generated static routes and assets resolve.
  CHECK: `python design/v2_verify.py --architecture`
  EXPECT: `V2_ARCHITECTURE_PASS`
  EVIDENCE: `routes=41`, all required page types, `brokenLinks=0` on the final check.

- [x] G2: V2 service selector consumes the canonical 254-item data, changes direction/procedure in place, displays only sourced prices, links to category detail pages, and does not diagnose or prescribe.
  CHECK: `python design/v2_verify.py --selector-data`
  EXPECT: `V2_SELECTOR_DATA_PASS`
  EVIDENCE: `services=254`, `categories=10`, branch price differences `0`, local-catalogue mismatches `0`.

- [x] G3: booking choice flows expose real phone and verified DentalPRO links, preserve selected-interest context without claiming data transfer, and support Escape/outside close.
  CHECK: `python design/v2_verify.py --booking`
  EXPECT: `V2_BOOKING_PASS`
  EVIDENCE: Verified DentalPRO, E.164 `tel:` number, labelled WhatsApp/Telegram, no fake forms. Root headers open the real in-page modal; Spanish Quarters labels its Prokshino online destination.

- [x] G4: doctor index/profiles use sourced team facts and official/local portrait assets.
  CHECK: `python design/v2_verify.py --doctors`
  EXPECT: `V2_DOCTORS_PASS`
  EVIDENCE: `doctors=5`, `profiles=10`, official portraits/certificate links verified; root Spanish roster has five loaded local portraits.

- [x] G5: each separate full price catalogue retains all 254 exact names/prices, categories, search and accessible details.
  CHECK: `python design/v2_verify.py --catalogues`
  EXPECT: `V2_CATALOGUES_PASS`
  EVIDENCE: 254 exact rows per branch, zero name/price mismatches, ten categories, search and filters enabled.

- [x] G6: Chromium exercises the V2 selector, booking workflow and responsive routes at 320, 360, 375, 390, 430, 768, 1024, 1440 and 1920px, including 200% text scaling.
  CHECK: `python design/v2_visual_qa.py`
  EXPECT: `V2_BROWSER_QA_PASS`
  EVIDENCE: final run: `routes=41`, `routeChecks=369`, `zoomChecks=123`, `totalLayoutChecks=492`, `overflow=0`, `brokenImages=0`, `interactionErrors=0`.

- [x] G7: each major V2 page type has browser captures and old/new comparisons; source URLs/findings are recorded.
  CHECK: `python design/v2_verify.py --evidence`
  EXPECT: `V2_EVIDENCE_PASS`
  EVIDENCE: `screenshots=56` including six preserved visual-polish before-state captures, `measuredRoutes=369`, `zoomChecks=123`, nine widths; complete [screenshot index](docs/V2_SCREENSHOT_INDEX.md), source record `docs/V2_SOURCES.md`.

- [x] G8: a complete openable local preview is provided; lack of isolated public hosting is documented.
  CHECK: `python design/v2_verify.py --preview`
  EXPECT: `V2_PREVIEW_PASS`
  EVIDENCE: `index.html` local entry, 41 routes; run `python -m http.server 4173 --bind 127.0.0.1`, then open `/` or `/v2/`. Existing Pages configuration was not changed.

- [x] G9: only the requested design branch is published and a Draft PR is opened to `main`; `main`, tech foundation, WordPress, current production, Pages settings and PR #1 are unchanged; no merge/deploy occurs.
  CHECK: verify clean branch/remote SHA and `gh pr view --json isDraft,baseRefName,headRefName,url`.
  EXPECT: PR `isDraft=true`, base `main`, head `design/manus-dental-master-2026`, no merge or deployment.
  EVIDENCE: [PR #2](https://github.com/Valodi-3/dental-master-preview-2026/pull/2) is `OPEN · Draft`, base `main`, head `design/manus-dental-master-2026`; final local `HEAD` matched `git ls-remote` for that design branch after push. Remote `main` remains `9a99dc7baa6484bbec8b1823152f60a59bdbae2e`; tech remains `72ad9a3de2668eb2fa7e3f3034a844f0d085fe69`; PR #1 remains open/draft/unmerged; no `app.js` or test files are in the diff.

- [x] G10: the exact 30-check Playwright suite from the updated tech branch passes against both root clinic pages; all nine widths include the requested 390, 768, 1024, 1440 and 1920px checks, every rendered image is loaded, each header trigger opens/closes a real booking dialog, and quick search returns sourced treatment rows.
  CHECK: `python .work/dental_regression/run_tech_qa.py --expect-30`
  EXPECT: `TECH_QA_SUMMARY total=30 passed=30 failed=0`.
  EVIDENCE: the unmodified suite passes 30/30; separate responsive smoke passes 10/10 requested page-width checks, 2/2 branch booking flows, six search states and 5/5 official local doctor portraits. Reports/screenshots: `design/v2qa/tech-root-qa-30-30.json`, `regression-validation.json`, `regression-comparison.json` and `screenshots/regression-*`.

## Iteration: visual finish after client feedback

- [x] G11: Prokshino and Spanish Quarters homepages have distinct, finished visual compositions at desktop and mobile, improve text hierarchy/legibility, and use varied authentic clinic images rather than repeating the same visual treatment.
  CHECK: inspect refreshed screenshots `design/v2qa/screenshots/v2-mobile-home-prokshino-390.png`, `v2-mobile-home-ispanskie-390.png`, `v2-desktop-home-prokshino-1440.png`, and `v2-desktop-home-ispanskie-1440.png`; inspect full-page mobile pair.
  EXPECT: visible branch-specific composition, readable body text and controls at phone size, stable hero/cards, no repeated-homepage clone; save visual review and changed-section evidence in `docs/V2_DESIGN_REPORT.md`.
  EVIDENCE: desktop/mobile before-and-after screenshots and full mobile pages are indexed in `docs/V2_SCREENSHOT_INDEX.md`; Prokshino now has a deep-green clinical hero and nonrepeating treatment/gallery imagery, while Spanish Quarters has an independently composed warm arch collage.

- [x] G12: polish does not regress the route/data/booking architecture or responsive contract.
  CHECK: `python design/build_v2.py`; `python design/v2_verify.py --architecture --selector-data --booking --doctors --catalogues --preview --evidence`; `python design/v2_visual_qa.py`; `python design/verify_design.py --static`; `python design/verify_design.py --catalogs`; `python design/polish_currency_qa.py`.
  EXPECT: all named commands exit zero; 41 routes, 254 correct services per branch, and browser checks stay at `overflow=0`, `brokenImages=0`, `interactionErrors=0`.
  EVIDENCE: final Chromium run `routeChecks=369`, `zoomChecks=123`, `totalLayoutChecks=492`, all error counters zero; source/catalogue gates pass; currency regression passes `cases=6`, `categoryChipPriceLabels=168`, `failures=0` (`design/v2qa/polish-currency-results.json`).


## Iteration: client reference — premium atmosphere, transitions, three-way appointment

- [x] G13: the new premium interaction layer uses authentic local clinic assets and lightweight CSS only; transitions honor reduced-motion preferences and no heavy 3D/runtime dependency is added.
  CHECK: `python design/new_direction_qa.py --motion`
  EXPECT: `NEW_DIRECTION_MOTION_PASS`
  EVIDENCE: `NEW_DIRECTION_MOTION_PASS localAssets=true css3d=true heavyRuntime=false reducedMotion=true`; local media/assets only, CSS perspective/rotateY disabled in reduced-motion mode.

- [x] G14: clicking any primary “Записаться” control opens an in-page choice dialog first, with explicit DentalPRO, phone and official messaging choices; no method is started until the visitor chooses its final action.
  CHECK: `python design/new_direction_qa.py --booking`
  EXPECT: `NEW_DIRECTION_BOOKING_PASS`
  EVIDENCE: `NEW_DIRECTION_BOOKING_PASS explicitChoices=3 branches=2 widths=320,390,1440 earlyRedirects=0`; call/copy controls, official WhatsApp/Telegram URLs, Spanish-to-Prokshino disclosure, Escape and all unscrolled phone-sheet actions verified at 844px.

- [x] G15: every generated route and the interactive UX remain responsive after rebuilding the premium visual system.
  CHECK: `python design/build_v2.py` followed by `python design/v2_visual_qa.py` and `python design/new_direction_qa.py --motion --booking`
  EXPECT: `V2_BROWSER_QA_PASS` and `NEW_DIRECTION_UX_PASS`
  EVIDENCE: `V2_BROWSER_QA_PASS routes=41 viewports=9 routeChecks=369 zoomChecks=123 totalLayoutChecks=492 screenshots=41 overflow=0 brokenImages=0 interactionErrors=0`; static/evidence gate sees 58 screenshots; 254 exact catalogue rows per branch; 168 selector prices without wraps.

- [ ] G16: the project remains an unmerged Draft on the isolated design branch; main and technical foundation SHAs remain unchanged.
  CHECK: `python design/draft_safety_qa.py`
  EXPECT: `DRAFT_SAFETY_PASS`
  EVIDENCE: pending

- [x] G17: mobile/desktop design feels polished, inspired by the supplied editorial emerald reference without copying its portfolio layout or introducing irrelevant imagery.
  EVIDENCE: final Prokshino emerald/champagne mobile and desktop, distinct warm Spanish Quarters collage, and both 390px three-choice phone dialogs were visually reviewed; genuine clinic assets and responsive controls confirmed.


Final artifacts for this iteration: [`layout-metrics.json`](design/v2qa/layout-metrics.json), [`premium-booking-choice-prokshino-390.png`](design/v2qa/screenshots/premium-booking-choice-prokshino-390.png), [`premium-booking-choice-ispanskie-390.png`](design/v2qa/screenshots/premium-booking-choice-ispanskie-390.png), and [`V2_SCREENSHOT_INDEX.md`](docs/V2_SCREENSHOT_INDEX.md).

Design review and before/after comparisons are documented in `docs/V2_DESIGN_REPORT.md` and `docs/V2_SCREENSHOT_INDEX.md`.
Publication integrity remains a separate check under G16 and has not yet been certified in this ledger.


Design review and before/after comparisons are documented in `docs/V2_DESIGN_REPORT.md` and `docs/V2_SCREENSHOT_INDEX.md`.
Publication integrity remains a separate check under G16 and has not yet been certified in this ledger.
