/**
 * DENTAL MASTER X — INTERACTIVE CLIENT RUNTIME
 * Built on REGINA V16 interaction principles:
 * - 3-step tactile service configuration
 * - Non-disruptive choice booking dialog
 * - Zero fake simulated calendars
 * - Pure vanilla JS, accessible & keyboard friendly
 */

(function () {
  'use strict';

  const currentBranch = document.documentElement.dataset.branch || 'ispanskie';

  // --- 1. Service Configurator Logic ---
  function initConfigurator() {
    const root = document.querySelector('[data-dx-configurator]');
    if (!root) return;

    const catalog = window.DX_CATALOG;
    if (!catalog || !catalog.categories) return;

    const catNav = root.querySelector('[data-cat-nav]');
    const procList = root.querySelector('[data-proc-list]');
    const stageImg = root.querySelector('[data-stage-img]');
    const stageBadge = root.querySelector('[data-stage-badge]');
    const stageTitle = root.querySelector('[data-stage-title]');
    const stageDesc = root.querySelector('[data-stage-desc]');
    const stagePrice = root.querySelector('[data-stage-price]');
    const stageStatus = root.querySelector('[data-stage-status]');
    const stageBookBtn = root.querySelector('[data-stage-book]');

    let activeCatIndex = 0;
    let activeProcIndex = 0;

    // Render Category Tabs
    if (catNav) {
      catNav.innerHTML = '';
      catalog.categories.forEach((cat, idx) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = `config-cat-btn ${idx === 0 ? 'is-active' : ''}`;
        btn.setAttribute('role', 'tab');
        btn.setAttribute('aria-selected', String(idx === 0));
        btn.innerHTML = `<span>${cat.icon}</span> <span>${cat.name}</span>`;

        btn.addEventListener('click', () => {
          if (activeCatIndex === idx) return;
          activeCatIndex = idx;
          activeProcIndex = 0;
          catNav.querySelectorAll('.config-cat-btn').forEach((b, i) => {
            const active = i === idx;
            b.classList.toggle('is-active', active);
            b.setAttribute('aria-selected', String(active));
          });
          renderProcedures(catalog.categories[activeCatIndex]);
        });

        catNav.appendChild(btn);
      });
    }

    function renderProcedures(category) {
      if (!procList || !category || !category.procedures) return;

      procList.innerHTML = '';
      category.procedures.forEach((proc, idx) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = `config-proc-btn ${idx === activeProcIndex ? 'is-active' : ''}`;
        btn.setAttribute('role', 'tab');
        btn.setAttribute('aria-selected', String(idx === activeProcIndex));
        
        const price = (proc.prices && proc.prices[currentBranch]) || Object.values(proc.prices || {})[0] || 'По запросу';

        btn.innerHTML = `
          <div class="proc-btn-info">
            <strong>${proc.name}</strong>
            <small>${proc.tag}</small>
          </div>
          <span class="proc-btn-price">${price}</span>
        `;

        btn.addEventListener('click', () => {
          activeProcIndex = idx;
          procList.querySelectorAll('.config-proc-btn').forEach((b, i) => {
            const active = i === idx;
            b.classList.toggle('is-active', active);
            b.setAttribute('aria-selected', String(active));
          });
          updateStage(proc, category);
        });

        procList.appendChild(btn);
      });

      if (category.procedures.length > 0) {
        updateStage(category.procedures[activeProcIndex], category);
      }
    }

    function resolveAssetPath(path) {
      if (!path) return '';
      const isSubfolder = window.location.pathname.includes('/prokshino') || window.location.pathname.includes('/gallery');
      if (isSubfolder && path.startsWith('../design/')) {
        return '../' + path;
      }
      return path;
    }

    function updateStage(proc, category) {
      if (!proc) return;

      const price = (proc.prices && proc.prices[currentBranch]) || Object.values(proc.prices || {})[0] || 'По запросу';
      const rawImg = (proc.images && proc.images[currentBranch]) || Object.values(proc.images || {})[0];
      const imgSrc = resolveAssetPath(rawImg);

      if (stageImg && imgSrc) {
        stageImg.classList.add('is-fading');
        stageImg.src = imgSrc;
        stageImg.alt = proc.name;
        stageImg.onload = () => stageImg.classList.remove('is-fading');
      }

      if (stageBadge) stageBadge.textContent = proc.tag || category.badge || 'Процедура';
      if (stageTitle) stageTitle.textContent = proc.name;
      if (stageDesc) stageDesc.textContent = proc.shortDesc;
      if (stagePrice) stagePrice.textContent = price;
      if (stageStatus) stageStatus.textContent = 'Утвержденный тариф';

      if (stageBookBtn) {
        stageBookBtn.dataset.serviceName = proc.name;
        stageBookBtn.dataset.servicePrice = price;
      }
    }

    // Initial render
    if (catalog.categories.length > 0) {
      renderProcedures(catalog.categories[0]);
    }
  }

  // --- 2. Booking Choice Dialog Logic ---
  function initBookingModal() {
    const modal = document.querySelector('#dxBookingModal');
    if (!modal) return;

    const contextEl = modal.querySelector('#dxBookingContext');
    const closeBtn = modal.querySelector('#dxBookingClose');
    const copyBtn = modal.querySelector('[data-copy-phone]');
    const copyStatus = modal.querySelector('[data-copy-status]');

    let returnFocusEl = null;

    function open(serviceName = null, servicePrice = null, triggerEl = null) {
      returnFocusEl = triggerEl || document.activeElement;

      if (serviceName && contextEl) {
        contextEl.innerHTML = `
          <div>
            <span style="font-size:0.7rem; color:var(--dx-dim); text-transform:uppercase; letter-spacing:0.08em; display:block; font-weight:700;">Выбранная процедура:</span>
            <strong>${serviceName}</strong>
          </div>
          ${servicePrice ? `<span>${servicePrice}</span>` : ''}
        `;
        contextEl.hidden = false;
      } else if (contextEl) {
        contextEl.hidden = true;
        contextEl.innerHTML = '';
      }

      if (copyStatus) copyStatus.textContent = '';

      modal.classList.add('is-open');
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';

      const firstAction = modal.querySelector('button:not([disabled]), a:not([disabled])');
      if (firstAction) firstAction.focus();
    }

    function close() {
      modal.classList.remove('is-open');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';

      if (returnFocusEl && typeof returnFocusEl.focus === 'function') {
        returnFocusEl.focus({ preventScroll: true });
      }
      returnFocusEl = null;
    }

    // Global click delegation for open triggers
    document.addEventListener('click', (e) => {
      const openTrigger = e.target.closest('[data-open-booking]');
      if (openTrigger) {
        e.preventDefault();
        const sName = openTrigger.dataset.serviceName || null;
        const sPrice = openTrigger.dataset.servicePrice || null;
        open(sName, sPrice, openTrigger);
        return;
      }

      if (e.target.closest('#dxBookingClose')) {
        e.preventDefault();
        close();
        return;
      }

      // Backdrop click
      if (e.target === modal) {
        close();
      }
    });

    // Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('is-open')) {
        close();
      }
    });

    // Phone copy to clipboard
    if (copyBtn) {
      copyBtn.addEventListener('click', async () => {
        const phone = '+79045199697';
        try {
          await navigator.clipboard.writeText(phone);
          if (copyStatus) copyStatus.textContent = '✓ Номер скопирован';
        } catch (err) {
          const input = document.createElement('input');
          input.value = phone;
          document.body.appendChild(input);
          input.select();
          document.execCommand('copy');
          input.remove();
          if (copyStatus) copyStatus.textContent = '✓ Номер скопирован';
        }
      });
    }
  }

  // --- 3. Smart Mobile Bottom Bar Visibility ---
  function initMobileBar() {
    const bar = document.querySelector('.dx-mobile-bar');
    const heroCta = document.querySelector('[data-hero-cta]');
    const footer = document.querySelector('.dx-footer');
    if (!bar) return;

    if ('IntersectionObserver' in window) {
      let heroVisible = false;
      let footerVisible = false;

      function update() {
        bar.classList.toggle('is-hidden', heroVisible || footerVisible);
      }

      const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.target === heroCta) heroVisible = entry.isIntersecting;
          if (entry.target === footer) footerVisible = entry.isIntersecting;
        });
        update();
      }, { threshold: 0.1 });

      if (heroCta) observer.observe(heroCta);
      if (footer) observer.observe(footer);
    }
  }

  // Initialize runtime on DOM ready
  document.addEventListener('DOMContentLoaded', () => {
    initConfigurator();
    initBookingModal();
    initMobileBar();
  });
})();
