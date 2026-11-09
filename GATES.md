# Gates: Dental Master Design 2026

OWNS: prokshino.html, prokshino.css, ispanskie.html, ispanskie.css, prices-prokshino.html, prices-ispanskie.html, concepts.html, design/**, docs/**

Scope: Deliver two distinct, content-accurate clinic previews, three responsive Prokshino hero concepts, separate 254-item price catalogues, and measured responsive QA without changing Antigravity's technical files.

- [x] G1: both clinic previews use verified source facts and real clinic photography
  CHECK: python design/verify_design.py --static
  EXPECT: STATIC_DESIGN_PASS
  EVIDENCE: STATIC_DESIGN_PASS; official source URLs and verified content in docs/SOURCE_NOTES.md; official clinic, staff and gallery photos in design/assets/.

- [x] G2: each standalone catalogue preserves all 254 services and its live search, filters, and expandable details
  CHECK: python design/verify_design.py --catalogs
  EXPECT: CATALOG_QA_PASS
  EVIDENCE: CATALOG_QA_PASS; exact 254-row name/price comparison to both current production catalogues produced zero mismatches; row and category interaction checks pass.

- [x] G3: widths 320, 360, 375, 390, 430, 768, 1024, 1440, and 1920 have no unintended horizontal overflow or out-of-bounds content, with bounding-box evidence and section screenshots at 390px and 1440px
  CHECK: python design/visual_qa.py --all
  EXPECT: RESPONSIVE_QA_PASS
  EVIDENCE: final browser run passed; 0 overflow, 0 out-of-bounds visible elements, 0 broken images across both main pages; both catalogues pass all nine widths. Evidence: design/qa/layout-metrics.json and 28 section captures.

- [x] G4: the three saved Prokshino concepts differ materially and show mobile and desktop composition
  EVIDENCE: concepts.html and concepts.css; six concept section screenshots at 390px and 1440px, indexed in docs/SCREENSHOT_INDEX.md.

- [x] G5: screenshots show a coherent visual result from hero through footer for both clinics at 390px and 1440px
  EVIDENCE: 28 section screenshots plus full-page and header-inclusive viewport captures; docs/SCREENSHOT_INDEX.md.

- [x] G6: only the requested design branch is published; production, main, and Antigravity-owned files remain unchanged
  EVIDENCE: origin/design/manus-dental-master-2026 published and verified; working tree is clean; app.js is unchanged; no production or existing Pages settings were modified.
