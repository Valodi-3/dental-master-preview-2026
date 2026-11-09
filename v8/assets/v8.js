(function () {
  'use strict';

  // --- 1. Modern Booking Modal Handling ---
  function initBookingModal() {
    const dialog = document.querySelector('[data-booking-modal]');
    if (!dialog || typeof dialog.showModal !== 'function') return;

    const serviceDisplay = dialog.querySelector('[data-modal-service-display]');
    const serviceName = dialog.querySelector('[data-modal-service-name]');
    const servicePrice = dialog.querySelector('[data-modal-service-price]');
    const copyButton = dialog.querySelector('[data-copy-phone]');
    const copyStatus = dialog.querySelector('[data-copy-status]');

    let returnFocus = null;

    function open(trigger) {
      returnFocus = trigger;
      const name = trigger.dataset.serviceName;
      const price = trigger.dataset.servicePrice;

      if (name && serviceDisplay && serviceName) {
        serviceName.textContent = name;
        if (servicePrice && price) servicePrice.textContent = price;
        serviceDisplay.hidden = false;
      } else if (serviceDisplay) {
        serviceDisplay.hidden = true;
      }

      if (copyStatus) copyStatus.textContent = '';
      if (!dialog.open) dialog.showModal();
    }

    document.addEventListener('click', (event) => {
      const openTrigger = event.target.closest('[data-open-booking]');
      if (openTrigger) {
        event.preventDefault();
        open(openTrigger);
        return;
      }

      if (event.target.closest('[data-close-modal]')) {
        dialog.close('user-close');
        return;
      }

      if (event.target.closest('[data-copy-phone]')) {
        copyPhone();
        return;
      }
    });

    // Light-dismiss click outside dialog box
    dialog.addEventListener('click', (event) => {
      if (event.target === dialog) {
        dialog.close('backdrop-click');
      }
    });

    dialog.addEventListener('close', () => {
      if (returnFocus && document.contains(returnFocus)) {
        returnFocus.focus({ preventScroll: true });
      }
      returnFocus = null;
    });

    async function copyPhone() {
      const phone = '+79045199697';
      const formatted = '+7 (904) 519-96-97';
      try {
        await navigator.clipboard.writeText(phone);
        if (copyStatus) copyStatus.textContent = 'Номер скопирован в буфер';
      } catch (err) {
        const input = document.createElement('input');
        input.value = phone;
        document.body.appendChild(input);
        input.select();
        document.execCommand('copy');
        input.remove();
        if (copyStatus) copyStatus.textContent = 'Номер скопирован';
      }
    }
  }

  // --- 2. Concept A (Cinematic) Configurator ---
  function initConceptA() {
    const root = document.querySelector('[data-concept="cinematic"]');
    if (!root) return;

    const stageImg = root.querySelector('[data-stage-image]');
    const stageKicker = root.querySelector('[data-stage-kicker]');
    const stageTitle = root.querySelector('[data-stage-title]');
    const stageDesc = root.querySelector('[data-stage-desc]');
    const stagePrice = root.querySelector('[data-stage-price]');
    const stageBadge = root.querySelector('[data-stage-badge]');
    const bookBtn = root.querySelector('[data-stage-book]');
    const tabs = root.querySelectorAll('[data-cinematic-tab]');

    tabs.forEach((tab) => {
      tab.addEventListener('click', () => {
        tabs.forEach((t) => t.classList.remove('is-active'));
        tab.classList.add('is-active');

        const { img, kicker, title, desc, price, badge, serviceName } = tab.dataset;

        if (stageImg && img) {
          stageImg.classList.add('is-fading');
          stageImg.src = img;
          stageImg.onload = () => stageImg.classList.remove('is-fading');
        }
        if (stageKicker && kicker) stageKicker.textContent = kicker;
        if (stageTitle && title) stageTitle.textContent = title;
        if (stageDesc && desc) stageDesc.textContent = desc;
        if (stagePrice && price) stagePrice.textContent = price;
        if (stageBadge && badge) stageBadge.textContent = badge;
        if (bookBtn) {
          bookBtn.dataset.serviceName = serviceName || title;
          bookBtn.dataset.servicePrice = price;
        }
      });
    });
  }

  // --- 3. Concept B (Editorial) Configurator ---
  function initConceptB() {
    const root = document.querySelector('[data-concept="editorial"]');
    if (!root) return;

    const portraitImg = root.querySelector('[data-editorial-portrait]');
    const portraitCaption = root.querySelector('[data-editorial-caption]');
    const entries = root.querySelectorAll('[data-editorial-entry]');

    entries.forEach((entry) => {
      function activate() {
        entries.forEach((e) => e.classList.remove('is-active'));
        entry.classList.add('is-active');

        const { img, caption } = entry.dataset;
        if (portraitImg && img) {
          portraitImg.style.opacity = '0.5';
          portraitImg.src = img;
          portraitImg.onload = () => (portraitImg.style.opacity = '1');
        }
        if (portraitCaption && caption) {
          portraitCaption.textContent = caption;
        }
      }

      entry.addEventListener('mouseenter', activate);
      entry.addEventListener('click', activate);
    });
  }

  // --- 4. Concept C (Interactive Experience) Configurator ---
  function initConceptC() {
    const root = document.querySelector('[data-concept="interactive"]');
    if (!root) return;

    const chips = root.querySelectorAll('[data-goal-chip]');
    const cardTitle = root.querySelector('[data-goal-title]');
    const cardDesc = root.querySelector('[data-goal-desc]');
    const cardPrice = root.querySelector('[data-goal-price]');
    const cardDoctor = root.querySelector('[data-goal-doctor]');
    const cardDoctorRole = root.querySelector('[data-goal-doctor-role]');
    const cardDoctorImg = root.querySelector('[data-goal-doctor-img]');
    const cardDuration = root.querySelector('[data-goal-duration]');
    const cardImage = root.querySelector('[data-goal-image]');
    const bookBtn = root.querySelector('[data-goal-book]');

    chips.forEach((chip) => {
      chip.addEventListener('click', () => {
        chips.forEach((c) => c.classList.remove('is-active'));
        chip.classList.add('is-active');

        const { title, desc, price, doctor, role, doctorImg, duration, img, serviceName } = chip.dataset;

        if (cardTitle && title) cardTitle.textContent = title;
        if (cardDesc && desc) cardDesc.textContent = desc;
        if (cardPrice && price) cardPrice.textContent = price;
        if (cardDoctor && doctor) cardDoctor.textContent = doctor;
        if (cardDoctorRole && role) cardDoctorRole.textContent = role;
        if (cardDoctorImg && doctorImg) cardDoctorImg.src = doctorImg;
        if (cardDuration && duration) cardDuration.textContent = duration;
        if (cardImage && img) {
          cardImage.style.opacity = '0.4';
          cardImage.src = img;
          cardImage.onload = () => (cardImage.style.opacity = '1');
        }
        if (bookBtn) {
          bookBtn.dataset.serviceName = serviceName || title;
          bookBtn.dataset.servicePrice = price;
        }
      });
    });
  }

  // --- 5. Mobile Navigation & Smart FAB ---
  function initMobileMenu() {
    const toggle = document.querySelector('[data-menu-toggle]');
    const nav = document.querySelector('[data-mobile-menu]');
    if (!toggle || !nav) return;

    toggle.addEventListener('click', () => {
      const open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
    });
  }

  function initSmartFab() {
    const fab = document.querySelector('.v8-fab');
    const heroCta = document.querySelector('[data-hero-cta]');
    const footer = document.querySelector('footer');
    if (!fab) return;

    if (typeof IntersectionObserver === 'function') {
      let heroVisible = false;
      let footerVisible = false;

      function update() {
        fab.classList.toggle('is-hidden', heroVisible || footerVisible);
      }

      const obs = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.target === heroCta) heroVisible = entry.isIntersecting;
            if (entry.target === footer) footerVisible = entry.isIntersecting;
          });
          update();
        },
        { threshold: 0.1 }
      );

      if (heroCta) obs.observe(heroCta);
      if (footer) obs.observe(footer);
    }
  }

  // Initialize all components
  initBookingModal();
  initConceptA();
  initConceptB();
  initConceptC();
  initMobileMenu();
  initSmartFab();
})();
