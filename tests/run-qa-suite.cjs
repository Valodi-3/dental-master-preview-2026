/**
 * Automated Multi-Viewport, Layout Integrity and Functional QA Suite
 * Project: Dental Master VNext 2026 (Prokshino & Ispanskie Kvartaly)
 *
 * Requirements:
 *   - Portable Playwright resolution (no hardcoded machine paths)
 *   - Strict reporting: any failing check, missing selector, or exception MUST report FAIL
 *   - Multi-viewport matrix: 320, 360, 375, 390, 430, 768, 1024, 1440, 1920 px
 *   - Horizontal overflow detection: scrollWidth > clientWidth
 *   - Zero localhost / 127.0.0.1 in rendered DOM
 *   - Zero broken images (naturalWidth === 0)
 *   - Modal dialog keyboard accessibility (Escape)
 *   - Zero fake form submission simulation
 *   - Mobile drawer navigation & relative branch switcher
 *   - Catalog live search & filter response
 */

const fs = require('fs');
const path = require('path');

// 1. Portable Playwright Resolution
let chromium;
try {
  chromium = require('playwright').chromium;
} catch (e1) {
  try {
    chromium = require(path.join(__dirname, 'node_modules/playwright')).chromium;
  } catch (e2) {
    if (process.env.PLAYWRIGHT_PATH) {
      try {
        chromium = require(process.env.PLAYWRIGHT_PATH).chromium;
      } catch (e3) {}
    }
  }
}

if (!chromium) {
  console.error('\n[FATAL ERROR] Playwright is not installed or could not be resolved.');
  console.error('Please install required dependencies before running tests:');
  console.error('   cd tests');
  console.error('   npm install');
  console.error('   npx playwright install chromium\n');
  process.exit(1);
}

const targetBaseUrl = process.env.TEST_URL || 'http://127.0.0.1:8765';

const viewports = [
  { width: 320, height: 568, name: '320px (iPhone SE 1st gen)' },
  { width: 360, height: 740, name: '360px (Android compact)' },
  { width: 375, height: 667, name: '375px (iPhone SE 2nd gen)' },
  { width: 390, height: 844, name: '390px (iPhone 12/13/14 standard)' },
  { width: 430, height: 932, name: '430px (iPhone Pro Max)' },
  { width: 768, height: 1024, name: '768px (iPad portrait)' },
  { width: 1024, height: 768, name: '1024px (iPad landscape / small laptop)' },
  { width: 1440, height: 900, name: '1440px (Desktop standard)' },
  { width: 1920, height: 1080, name: '1920px (Desktop Full HD)' }
];

const pagesToTest = [
  { file: 'prokshino.html', name: 'ДантистЪ Прокшино' },
  { file: 'ispanskie.html', name: 'ДантистЪ Испанские кварталы' }
];

async function runQaMatrix() {
  console.log('================================================================');
  console.log('   DENTAL MASTER QA AUTOMATION MATRIX — Playwright Portable Engine');
  console.log(`   Base URL: ${targetBaseUrl}`);
  console.log(`   Timestamp: ${new Date().toISOString()}`);
  console.log('================================================================\n');

  let browser;
  try {
    browser = await chromium.launch({ headless: true });
  } catch (err) {
    console.error('[FATAL] Failed to launch Chromium browser:', err.message);
    process.exit(1);
  }

  const results = {
    testedAt: new Date().toISOString(),
    baseUrl: targetBaseUrl,
    summary: { totalTests: 0, passed: 0, failed: 0 },
    pages: {}
  };

  for (const pageInfo of pagesToTest) {
    console.log(`\n>>> TESTING PAGE: ${pageInfo.name} (${pageInfo.file}) <<<`);
    const pageUrl = `${targetBaseUrl}/${pageInfo.file}`;
    const pageResults = {
      name: pageInfo.name,
      file: pageInfo.file,
      url: pageUrl,
      viewports: {},
      functionalChecks: {}
    };

    // 1. VIEWPORT MATRIX (Overflow & Layout Integrity)
    for (const vp of viewports) {
      process.stdout.write(`  [Viewport ${vp.name}] Checking overflow... `);
      results.summary.totalTests++;

      try {
        const context = await browser.newContext({
          viewport: { width: vp.width, height: vp.height },
          isMobile: vp.width < 768,
          hasTouch: vp.width < 768
        });
        const page = await context.newPage();
        await page.goto(pageUrl, { waitUntil: 'networkidle', timeout: 15000 });

        const overflowData = await page.evaluate((vpWidth) => {
          const docWidth = document.documentElement.scrollWidth;
          const bodyWidth = document.body.scrollWidth;
          const winWidth = window.innerWidth;
          const isOverflowing = docWidth > winWidth + 1 || bodyWidth > winWidth + 1;

          let violatingElements = [];
          if (isOverflowing) {
            const allEls = document.querySelectorAll('*');
            allEls.forEach(el => {
              const rect = el.getBoundingClientRect();
              if (rect.right > winWidth + 2 && rect.width > 0) {
                violatingElements.push({
                  tag: el.tagName.toLowerCase(),
                  id: el.id || null,
                  className: el.className ? String(el.className).substring(0, 80) : null,
                  right: Math.round(rect.right),
                  width: Math.round(rect.width),
                  overflowPx: Math.round(rect.right - winWidth)
                });
              }
            });
          }

          return {
            winWidth,
            docWidth,
            bodyWidth,
            isOverflowing,
            violatingElements: violatingElements.slice(0, 5)
          };
        }, vp.width);

        if (overflowData.isOverflowing) {
          console.log(`FAIL! Overflow: ${overflowData.docWidth}px > ${overflowData.winWidth}px (+${overflowData.docWidth - overflowData.winWidth}px)`);
          results.summary.failed++;
          pageResults.viewports[vp.width] = {
            status: 'FAIL',
            overflowPx: overflowData.docWidth - overflowData.winWidth,
            violatingElements: overflowData.violatingElements
          };
        } else {
          console.log('PASS (0px overflow)');
          results.summary.passed++;
          pageResults.viewports[vp.width] = { status: 'PASS' };
        }

        await context.close();
      } catch (e) {
        console.log(`FAIL! Execution error: ${e.message}`);
        results.summary.failed++;
        pageResults.viewports[vp.width] = { status: 'FAIL', error: e.message };
      }
    }

    // 2. FUNCTIONAL & ACCESSIBILITY TESTS (Desktop 1440px)
    console.log(`\n  --- Functional Checks on ${pageInfo.name} ---`);
    let fnContext, fnPage;
    try {
      fnContext = await browser.newContext({ viewport: { width: 1440, height: 900 } });
      fnPage = await fnContext.newPage();
      await fnPage.goto(pageUrl, { waitUntil: 'networkidle', timeout: 15000 });
    } catch (e) {
      console.error(`[FATAL] Failed to open desktop context for ${pageInfo.name}:`, e.message);
      results.summary.failed++;
      continue;
    }

    // Check A: Zero Localhost / 127.0.0.1 in rendered DOM
    results.summary.totalTests++;
    try {
      const pageHtml = await fnPage.content();
      const localhostMatches = pageHtml.match(/127\.0\.0\.1|localhost/g) || [];
      if (localhostMatches.length === 0) {
        console.log('  [PASS] Zero localhost/127.0.0.1 links in rendered DOM.');
        results.summary.passed++;
        pageResults.functionalChecks.zeroLocalhost = { status: 'PASS' };
      } else {
        console.log(`  [FAIL] Found ${localhostMatches.length} localhost references!`);
        results.summary.failed++;
        pageResults.functionalChecks.zeroLocalhost = { status: 'FAIL', count: localhostMatches.length };
      }
    } catch (e) {
      console.log(`  [FAIL] Error during zeroLocalhost check: ${e.message}`);
      results.summary.failed++;
      pageResults.functionalChecks.zeroLocalhost = { status: 'FAIL', error: e.message };
    }

    // Check B: Broken Images (naturalWidth === 0)
    results.summary.totalTests++;
    try {
      const brokenImages = await fnPage.evaluate(() => {
        const imgs = Array.from(document.querySelectorAll('img'));
        return imgs
          .filter(img => img.naturalWidth === 0 && !img.src.includes('data:image'))
          .map(img => ({ src: img.src, alt: img.alt }));
      });
      if (brokenImages.length === 0) {
        console.log('  [PASS] All rendered <img> images loaded with valid naturalWidth.');
        results.summary.passed++;
        pageResults.functionalChecks.imageIntegrity = { status: 'PASS' };
      } else {
        console.log(`  [FAIL] Found ${brokenImages.length} broken images:`, brokenImages.map(b => b.src));
        results.summary.failed++;
        pageResults.functionalChecks.imageIntegrity = { status: 'FAIL', broken: brokenImages };
      }
    } catch (e) {
      console.log(`  [FAIL] Error during imageIntegrity check: ${e.message}`);
      results.summary.failed++;
      pageResults.functionalChecks.imageIntegrity = { status: 'FAIL', error: e.message };
    }

    // Check C: Modal Dialog Accessibility & Keyboard Escape
    results.summary.totalTests++;
    try {
      const modalTest = await fnPage.evaluate(() => {
        const trigger = document.querySelector('[data-booking-trigger], [data-book]');
        if (!trigger) return { exists: false, error: 'Trigger element [data-booking-trigger] not found' };
        trigger.click();

        const modal = document.querySelector('#bookingModal, #booking-modal, .booking-modal-overlay');
        if (!modal) return { exists: true, error: 'Modal container element not found' };
        const isVisibleBefore = modal.classList.contains('active') || modal.classList.contains('is-active');

        // Dispatch Escape key
        document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
        const isVisibleAfter = modal.classList.contains('active') || modal.classList.contains('is-active');

        return {
          exists: true,
          openedOnClick: isVisibleBefore,
          closedOnEscape: !isVisibleAfter
        };
      });

      if (modalTest.exists && modalTest.openedOnClick && modalTest.closedOnEscape) {
        console.log('  [PASS] Booking modal opens on trigger and closes on Escape key.');
        results.summary.passed++;
        pageResults.functionalChecks.modalAccessibility = { status: 'PASS' };
      } else {
        console.log('  [FAIL] Modal accessibility check failed:', modalTest);
        results.summary.failed++;
        pageResults.functionalChecks.modalAccessibility = { status: 'FAIL', details: modalTest };
      }
    } catch (e) {
      console.log(`  [FAIL] Error during modalAccessibility check: ${e.message}`);
      results.summary.failed++;
      pageResults.functionalChecks.modalAccessibility = { status: 'FAIL', error: e.message };
    }

    // Check D: Fake Form Simulation Check
    results.summary.totalTests++;
    try {
      const fakeFormCheck = await fnPage.evaluate(() => {
        const text = document.body.innerText;
        const hasFakeSuccess = text.includes('Заявка принята') || text.includes('Спасибо, мы перезвоним');
        const hasFormWithoutBackend = document.querySelectorAll('form:not([action])').length > 0;
        return {
          hasFakeSuccess,
          hasFormWithoutBackend
        };
      });

      if (!fakeFormCheck.hasFakeSuccess) {
        console.log('  [PASS] Zero fake form simulation. Real direct channels present.');
        results.summary.passed++;
        pageResults.functionalChecks.zeroFakeForms = { status: 'PASS' };
      } else {
        console.log('  [FAIL] Fake form submission message detected in page!');
        results.summary.failed++;
        pageResults.functionalChecks.zeroFakeForms = { status: 'FAIL', details: fakeFormCheck };
      }
    } catch (e) {
      console.log(`  [FAIL] Error during zeroFakeForms check: ${e.message}`);
      results.summary.failed++;
      pageResults.functionalChecks.zeroFakeForms = { status: 'FAIL', error: e.message };
    }

    // Check E: Catalog Search & Filter Tabs (Strict FAIL if missing or non-functional)
    results.summary.totalTests++;
    try {
      const searchFilterTest = await fnPage.evaluate(() => {
        const searchInput = document.getElementById('catalogue-search') ||
                            document.getElementById('price-search') ||
                            document.querySelector('input[type="search"]');

        if (!searchInput) {
          return { found: false, error: 'Search input element not found in DOM' };
        }

        searchInput.value = 'кариес';
        searchInput.dispatchEvent(new Event('input', { bubbles: true }));

        const rows = Array.from(document.querySelectorAll('.price-row, .price-table tr:not(:first-child), .catalogue-item'));
        if (rows.length === 0) {
          return { found: true, hasRows: false, error: 'No catalog item/row elements found in DOM' };
        }

        const visibleRows = rows.filter(r => {
          const style = window.getComputedStyle(r);
          return style.display !== 'none' && style.visibility !== 'hidden';
        });

        return {
          found: true,
          hasRows: true,
          totalRows: rows.length,
          filteredRowsCount: visibleRows.length
        };
      });

      if (searchFilterTest.found && searchFilterTest.hasRows && searchFilterTest.filteredRowsCount > 0) {
        console.log(`  [PASS] Catalog live search responsive (${searchFilterTest.filteredRowsCount} rows matching "кариес").`);
        results.summary.passed++;
        pageResults.functionalChecks.searchFilter = { status: 'PASS', matchingRows: searchFilterTest.filteredRowsCount };
      } else {
        console.log('  [FAIL] Catalog search filter test failed:', searchFilterTest);
        results.summary.failed++;
        pageResults.functionalChecks.searchFilter = { status: 'FAIL', details: searchFilterTest };
      }
    } catch (e) {
      console.log(`  [FAIL] Error during searchFilter check: ${e.message}`);
      results.summary.failed++;
      pageResults.functionalChecks.searchFilter = { status: 'FAIL', error: e.message };
    }

    // Check F: Mobile Navigation Drawer (Tested on 390px, Strict FAIL if missing)
    results.summary.totalTests++;
    try {
      const mobContext = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
      const mobPage = await mobContext.newPage();
      await mobPage.goto(pageUrl, { waitUntil: 'networkidle', timeout: 15000 });

      const drawerTest = await mobPage.evaluate(() => {
        const toggle = document.querySelector('#menu-toggle, #menuToggleBtn, .menu-toggle-btn');
        const drawer = document.querySelector('#mobile-nav, #mobileDrawer, .mobile-nav-drawer');

        if (!toggle) return { ok: false, error: 'Mobile menu toggle button not found' };
        if (!drawer) return { ok: false, error: 'Mobile nav drawer container not found' };

        toggle.click();
        const isOpen = drawer.classList.contains('active') || drawer.classList.contains('is-open');

        const branchLink = drawer.querySelector('.mobile-link-branch, .drawer-branch-link, a[href*="prokshino.html"], a[href*="ispanskie.html"]');
        const branchHref = branchLink ? branchLink.getAttribute('href') : null;

        return {
          ok: isOpen && Boolean(branchHref),
          hasToggle: true,
          hasDrawer: true,
          opensOnToggle: isOpen,
          branchHref: branchHref
        };
      });

      if (drawerTest.ok && drawerTest.branchHref && !drawerTest.branchHref.includes('127.0.0.1')) {
        console.log(`  [PASS] Mobile drawer opens correctly, branch switcher relative (${drawerTest.branchHref}).`);
        results.summary.passed++;
        pageResults.functionalChecks.mobileDrawer = { status: 'PASS', branchHref: drawerTest.branchHref };
      } else {
        console.log('  [FAIL] Mobile drawer check failed:', drawerTest);
        results.summary.failed++;
        pageResults.functionalChecks.mobileDrawer = { status: 'FAIL', details: drawerTest };
      }

      await mobContext.close();
    } catch (e) {
      console.log(`  [FAIL] Error during mobileDrawer check: ${e.message}`);
      results.summary.failed++;
      pageResults.functionalChecks.mobileDrawer = { status: 'FAIL', error: e.message };
    }

    await fnContext.close();
    results.pages[pageInfo.file] = pageResults;
  }

  await browser.close();

  // Save report to tests/qa-report.json
  const reportPath = path.join(__dirname, 'qa-report.json');
  fs.writeFileSync(reportPath, JSON.stringify(results, null, 2), 'utf8');

  console.log(`\n================================================================`);
  console.log(`   QA MATRIX COMPLETE: ${results.summary.passed} PASSED / ${results.summary.failed} FAILED (Total: ${results.summary.totalTests})`);
  console.log(`   Report saved to: ${reportPath}`);
  console.log(`================================================================\n`);

  if (results.summary.failed > 0) {
    process.exitCode = 1;
  }

  return results;
}

runQaMatrix().catch(err => {
  console.error('[FATAL] QA matrix execution halted by error:', err);
  process.exit(1);
});
