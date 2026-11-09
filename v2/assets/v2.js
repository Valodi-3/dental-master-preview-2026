(function () {
  'use strict';

  const DATA = window.DENTAL_V2;
  if (!DATA) return;

  const body = document.body;
  const clinicKey = body.dataset.clinic;
  const clinic = DATA.branches[clinicKey];
  const repoRoot = document.documentElement.dataset.repoRoot || '';
  const serviceById = new Map(DATA.services.map((service) => [service.id, service]));
  const categoryCodes = Object.keys(DATA.categories);
  const categorySlug = {
    consultations: 'consultations',
    diagnostics: 'diagnostics',
    anesthesia: 'anesthesia',
    hygiene: 'hygiene',
    treatment: 'treatment',
    endodontics: 'endodontics',
    surgery: 'surgery',
    implantation: 'implantation',
    prosthetics: 'prosthetics',
    orthodontics: 'orthodontics',
  };

  function byRole(root, role) {
    return root.querySelector(`[data-${role}]`);
  }

  function servicePrice(service) {
    const branchPrice = service && service.pricing && service.pricing[clinicKey];
    return branchPrice ? branchPrice.formatted : '';
  }

  function selectorUrl(base, category, service) {
    const path = `${base.replace(/\/$/, '')}/${categorySlug[category]}.html`;
    return `${path}?service=${encodeURIComponent(service.id)}#selected-procedure`;
  }

  function initializeSelector(selector) {
    const categoryBox = selector.querySelector('[data-selector-categories]');
    const variantsBox = selector.querySelector('[data-selector-variants]');
    const serviceBase = selector.dataset.serviceBase || 'services';
    const image = selector.querySelector('[data-selector-image]');
    const categoryLabel = selector.querySelector('[data-selector-category]');
    const serviceName = selector.querySelector('[data-selector-name]');
    const description = selector.querySelector('[data-selector-description]');
    const price = selector.querySelector('[data-selector-price]');
    const detailLink = selector.querySelector('[data-selector-details]');
    const bookButton = selector.querySelector('[data-open-booking][data-service-id]');
    if (!categoryBox || !variantsBox || !clinic) return;

    let activeCategory = 'implantation';
    let activeServiceId = DATA.featuredServiceIds[activeCategory][0];
    const categoryButtons = new Map();
    const serviceButtons = new Map();

    function selectedService() {
      return serviceById.get(activeServiceId) || serviceById.get(DATA.featuredServiceIds[activeCategory][0]);
    }

    function makeCategoryTabs() {
      categoryBox.textContent = '';
      categoryCodes.forEach((category, index) => {
        const summary = DATA.categories[category];
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'selector-category';
        button.setAttribute('role', 'tab');
        button.setAttribute('aria-selected', String(category === activeCategory));
        button.setAttribute('aria-controls', selector.querySelector('[data-selector-card]')?.id || 'selected-procedure');
        button.dataset.categoryId = category;
        const number = document.createElement('span');
        number.textContent = String(index + 1).padStart(2, '0');
        const title = document.createElement('span');
        title.textContent = summary.title;
        const count = document.createElement('span');
        count.textContent = String(summary.count);
        count.setAttribute('aria-label', `${summary.count} позиций`);
        button.append(number, title, count);
        button.addEventListener('click', () => setCategory(category));
        button.addEventListener('keydown', (event) => handleTabKey(event, categoryBox, button));
        categoryBox.append(button);
        categoryButtons.set(category, button);
      });
    }

    function handleTabKey(event, container, currentButton) {
      const tabs = [...container.querySelectorAll('[role="tab"]')];
      const currentIndex = tabs.indexOf(currentButton);
      let nextIndex = currentIndex;
      if (event.key === 'ArrowRight' || event.key === 'ArrowDown') nextIndex = (currentIndex + 1) % tabs.length;
      if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') nextIndex = (currentIndex - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') nextIndex = 0;
      if (event.key === 'End') nextIndex = tabs.length - 1;
      if (nextIndex !== currentIndex) {
        event.preventDefault();
        tabs[nextIndex].focus();
        tabs[nextIndex].click();
      }
    }

    function makeVariants() {
      variantsBox.textContent = '';
      serviceButtons.clear();
      const featured = DATA.featuredServiceIds[activeCategory] || [];
      featured.forEach((serviceId) => {
        const service = serviceById.get(serviceId);
        if (!service) return;
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'procedure-option';
        button.setAttribute('role', 'tab');
        button.setAttribute('aria-selected', String(serviceId === activeServiceId));
        button.dataset.serviceId = serviceId;
        const text = document.createElement('span');
        text.textContent = service.name;
        const amount = document.createElement('b');
        amount.textContent = servicePrice(service);
        button.append(text, amount);
        button.addEventListener('click', () => setService(serviceId));
        button.addEventListener('keydown', (event) => handleTabKey(event, variantsBox, button));
        variantsBox.append(button);
        serviceButtons.set(serviceId, button);
      });
    }

    function setCategory(category) {
      if (!DATA.categories[category]) return;
      activeCategory = category;
      activeServiceId = DATA.featuredServiceIds[category][0];
      categoryButtons.forEach((button, key) => button.setAttribute('aria-selected', String(key === category)));
      makeVariants();
      renderPanel();
    }

    function setService(serviceId) {
      const service = serviceById.get(serviceId);
      if (!service || service.category !== activeCategory) return;
      activeServiceId = serviceId;
      serviceButtons.forEach((button, key) => button.setAttribute('aria-selected', String(key === serviceId)));
      renderPanel();
    }

    function renderPanel() {
      const service = selectedService();
      if (!service) return;
      const category = service.category;
      if (categoryLabel) categoryLabel.textContent = DATA.categories[category].title.toLocaleUpperCase('ru');
      if (serviceName) serviceName.textContent = service.name;
      if (description) description.textContent = DATA.categoryDescriptions[category];
      if (price) price.textContent = servicePrice(service);
      if (image) {
        const imageWrap = image.closest('.selected-procedure-image');
        imageWrap?.classList.add('is-changing');
        image.alt = `Стоматологический приём в филиале ${clinic.name}`;
        image.src = new URL(`${repoRoot}${clinic.selectorImages[category]}`, location.href).href;
        image.addEventListener('load', () => imageWrap?.classList.remove('is-changing'), { once: true });
        image.addEventListener('error', () => imageWrap?.classList.remove('is-changing'), { once: true });
      }
      if (detailLink) detailLink.href = selectorUrl(serviceBase, category, service);
      if (bookButton) bookButton.dataset.serviceId = service.id;
      const nameNode = selector.querySelector('[data-selector-card]');
      if (nameNode) nameNode.setAttribute('aria-label', `${service.name}, ${servicePrice(service)}`);
    }

    makeCategoryTabs();
    makeVariants();
    renderPanel();
  }

  function initializeServiceDeepLink() {
    if (body.dataset.page !== 'service') return;
    const container = document.querySelector('[data-service-detail]');
    if (!container) return;
    container.hidden = true;
    const serviceId = new URLSearchParams(location.search).get('service');
    const service = serviceId ? serviceById.get(serviceId) : null;
    if (!service || service.category !== body.dataset.category) return;
    const name = container.querySelector('[data-detail-name]');
    const price = container.querySelector('[data-detail-price]');
    const booking = container.querySelector('[data-detail-booking]');
    if (name) name.textContent = service.name;
    if (price) price.textContent = servicePrice(service);
    if (booking) booking.dataset.serviceId = service.id;
    container.hidden = false;
    const firstFeatured = document.querySelector(`[data-service-id="${CSS.escape(service.id)}"]`);
    if (firstFeatured) firstFeatured.setAttribute('aria-current', 'true');
  }

  function initializeBookingDialog() {
    const dialog = document.querySelector('[data-booking-dialog]');
    if (!dialog || typeof dialog.showModal !== 'function') return;
    const choices = dialog.querySelector('[data-booking-step="choices"]');
    const callStep = dialog.querySelector('[data-booking-step="call"]');
    const summary = dialog.querySelector('[data-booking-service]');
    const serviceName = dialog.querySelector('[data-booking-service-name]');
    const serviceAmount = dialog.querySelector('[data-booking-service-price]');
    const serviceNote = dialog.querySelector('[data-booking-service-note]');
    const status = dialog.querySelector('[data-copy-status]');
    let returnFocus = null;

    function useStep(step) {
      const showCall = step === 'call';
      choices.hidden = showCall;
      callStep.hidden = !showCall;
      dialog.setAttribute('aria-labelledby', showCall ? 'booking-call-title' : 'booking-title');
      if (showCall) dialog.querySelector('#booking-call-title')?.focus({ preventScroll: true });
      else dialog.querySelector('[data-book-call]')?.focus({ preventScroll: true });
    }

    function open(target) {
      returnFocus = target;
      const service = serviceById.get(target.dataset.serviceId || '');
      if (service && summary && serviceName && serviceAmount && serviceNote) {
        serviceName.textContent = service.name;
        serviceAmount.textContent = `Позиция в прайсе: ${servicePrice(service)}`;
        summary.hidden = false;
        serviceNote.hidden = false;
      } else {
        summary.hidden = true;
        serviceNote.hidden = true;
      }
      if (status) status.textContent = '';
      useStep('choices');
      if (!dialog.open) dialog.showModal();
    }

    document.addEventListener('click', (event) => {
      const opener = event.target.closest('[data-open-booking]');
      if (opener) {
        event.preventDefault();
        open(opener);
        return;
      }
      if (event.target.closest('[data-close-booking]')) {
        dialog.close('close-button');
        return;
      }
      if (event.target.closest('[data-book-call]')) {
        useStep('call');
        return;
      }
      if (event.target.closest('[data-booking-back]')) {
        useStep('choices');
        return;
      }
      const copy = event.target.closest('[data-copy-phone]');
      if (copy) copyNumber(copy);
    });

    async function copyNumber(button) {
      const text = DATA.shared.phone;
      try {
        await navigator.clipboard.writeText(text);
        if (status) status.textContent = 'Номер скопирован.';
      } catch (_error) {
        const scratch = document.createElement('textarea');
        scratch.value = text;
        scratch.setAttribute('readonly', '');
        scratch.setAttribute('aria-label', 'Номер для копирования');
        scratch.style.position = 'fixed';
        scratch.style.left = '-10000px';
        document.body.append(scratch);
        scratch.select();
        const copied = document.execCommand('copy');
        scratch.remove();
        if (status) status.textContent = copied ? 'Номер скопирован.' : 'Не удалось скопировать. Выделите номер и скопируйте его вручную.';
      }
      button.setAttribute('aria-label', status?.textContent || 'Скопировать номер');
    }

    dialog.addEventListener('click', (event) => {
      if (event.target === dialog) dialog.close('backdrop');
    });
    dialog.addEventListener('close', () => {
      useStep('choices');
      if (returnFocus && document.contains(returnFocus)) returnFocus.focus({ preventScroll: true });
      returnFocus = null;
    });
  }

  function initializeMenu() {
    const button = document.querySelector('[data-menu-toggle]');
    const nav = document.querySelector('[data-primary-nav]');
    if (!button || !nav) return;
    const closeMenu = (restoreFocus = false) => {
      nav.classList.remove('is-open');
      button.setAttribute('aria-expanded', 'false');
      button.querySelector('.sr-only').textContent = 'Открыть меню';
      if (restoreFocus) button.focus({ preventScroll: true });
    };
    button.addEventListener('click', () => {
      const isOpen = button.getAttribute('aria-expanded') !== 'true';
      button.setAttribute('aria-expanded', String(isOpen));
      nav.classList.toggle('is-open', isOpen);
      button.querySelector('.sr-only').textContent = isOpen ? 'Закрыть меню' : 'Открыть меню';
    });
    nav.addEventListener('click', (event) => {
      if (event.target.closest('a')) closeMenu();
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') closeMenu(true);
    });
    document.addEventListener('click', (event) => {
      if (button.getAttribute('aria-expanded') === 'true' && !nav.contains(event.target) && !button.contains(event.target)) closeMenu();
    });
  }

  function serviceCountLabel(value) {
    const lastTwo = value % 100;
    const last = value % 10;
    let noun = 'услуг';
    if (lastTwo < 11 || lastTwo > 14) {
      if (last === 1) noun = 'услуга';
      else if (last >= 2 && last <= 4) noun = 'услуги';
    }
    return `Показано ${value} ${noun}`;
  }

  function initializePriceCatalog() {
    if (body.dataset.page !== 'prices') return;
    const search = document.querySelector('[data-catalog-search]');
    const clear = document.querySelector('[data-clear-search]');
    const filters = [...document.querySelectorAll('[data-catalog-filter]')];
    const rows = [...document.querySelectorAll('[data-price-item]')];
    const sections = [...document.querySelectorAll('[data-catalog-category]')];
    const count = document.querySelector('[data-catalog-count]');
    const empty = document.querySelector('[data-catalog-empty]');
    let activeCategory = 'all';

    function applyFilters() {
      const term = (search?.value || '').trim().toLocaleLowerCase('ru');
      let visible = 0;
      rows.forEach((row) => {
        const categoryMatch = activeCategory === 'all' || row.dataset.category === activeCategory;
        const termMatch = !term || row.textContent.toLocaleLowerCase('ru').includes(term);
        row.hidden = !(categoryMatch && termMatch);
        if (!row.hidden) visible += 1;
      });
      sections.forEach((section) => {
        const anyRow = section.querySelector('[data-price-item]:not([hidden])');
        section.hidden = !anyRow;
      });
      if (count) count.textContent = serviceCountLabel(visible);
      if (empty) empty.hidden = visible > 0;
      if (clear) clear.hidden = !term;
    }

    filters.forEach((filter) => {
      filter.addEventListener('click', () => {
        activeCategory = filter.dataset.catalogFilter || 'all';
        filters.forEach((candidate) => {
          const active = candidate === filter;
          candidate.classList.toggle('is-active', active);
          candidate.setAttribute('aria-pressed', String(active));
        });
        applyFilters();
      });
    });
    search?.addEventListener('input', applyFilters);
    clear?.addEventListener('click', () => {
      if (search) {
        search.value = '';
        search.focus();
      }
      applyFilters();
    });
    applyFilters();
  }

  initializeMenu();
  document.querySelectorAll('[data-service-selector]').forEach(initializeSelector);
  initializeServiceDeepLink();
  initializePriceCatalog();
  initializeBookingDialog();
})();
