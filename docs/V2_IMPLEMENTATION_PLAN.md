# Dental Master V2 — implementation plan

## Outcome

Replace the long-scroll landing-page model with two connected clinic minisites and a branch chooser. Build V2 beneath `v2/`; the branch's root `index.html` becomes a V2-first local entry that keeps the V1 pages reachable from its archive. Do not change public `main`/Pages sources, WordPress, Pages settings, or merge the Antigravity pull request.

## Page architecture

Each clinic receives a compact home page, an interactive all-directions page, ten category/detail routes derived from the verified catalogue, a clinician directory, individual clinician profiles, a 254-row searchable price list, a contacts page, and a shared booking-choice modal. Every page uses the same clinic-aware navigation and breadcrumb/path links so it is reachable from the chooser and related pages. Category pages share a structural template but use category-specific published price choices, sourced information, image, and layout treatment.

Planned paths:

- `v2/index.html` — chooser for both branches.
- `v2/prokshino/index.html` and `v2/ispanskie/index.html` — branch homepages.
- `v2/<branch>/directions/index.html` — interactive multi-service selector.
- `v2/<branch>/services/<category>.html` — 10 service categories for each branch.
- `v2/<branch>/doctors/index.html` and `v2/<branch>/doctors/<slug>.html` — team and doctor profiles.
- `v2/<branch>/prices/index.html` — compact 254-item catalogue.
- `v2/<branch>/contacts/index.html` — contact and booking options.

## Shared implementation contract

- `v2/assets/v2.css`: common components plus clinic-specific tokens/layout.
- `v2/assets/v2.js`: nav, selector state, modal choice, clipboard, accordions and reduced-motion behavior.
- `v2/assets/v2-data.js`: checked-in service/doctor data compiled from Antigravity's read-only foundation branch and reconciled against both production catalogues; no runtime network dependency.
- Generated static HTML uses explicit page, clinic, and category metadata. Each service route has a stable, branch-qualified canonical href.
- Booking modal presents call/copy and DentalPRO choices, shows the selected interest, and does not claim service data is passed to the booking vendor. The official Spanish Quarters link is explicitly labelled as opening Prokshino; calls are recommended for appointments at Spanish Quarters.
- The selector is patient-directed browsing, never diagnostic or treatment recommendation logic.
- Do not alter `app.js` or merge/push Antigravity's branch/PR.

## Execution sequence

1. Fetch and inspect PR #1, the referenced foundation branch, the two live sites, and the REGINA selector reference. Confirm available production source facts and current safe preview publication configuration.
2. Build the canonical service and clinician data bundle; record sources and comparison checks.
3. Implement shared navigation, clinical tokens, responsive selector, booking modal, and reusable page layouts.
4. Generate and connect all V2 routes for both branches while keeping the root V1 experience intact.
5. Verify routes, data, phone/link interactions, focus/Escape handling, compact catalogs, and nine viewport widths plus 200% text enlargement in a real browser.
6. Capture actual page-type screenshots, compare against production, and fix measured defects.
7. Publish only if an isolated preview route is available without replacing the current Pages site; otherwise provide a complete local-served build and state that public hosting remains unavailable.

## Acceptance evidence

See `GATES.md`. Runnable checks are implemented in `design/v2_verify.py` and `design/v2_visual_qa.py`; every gate must show a decisive pass marker after the full build is complete.
