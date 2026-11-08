/**
 * ДАНТИСТЪ — Interactive Controller (RC-4 Distinct Edition)
 * Authentic functionality: Doctor Dossier Modal, Real Booking Channels, Live Price Filtering, Accessible Navigation
 * ZERO mock forms, ZERO simulated submissions.
 */

document.addEventListener('DOMContentLoaded', () => {
  'use strict';

  // --- Doctor Dossier Data (Official Registry & Certificates) ---
  const doctorsData = {
    danielyan: {
      name: 'Даниелян Арам Яковлевич',
      role: 'Главный врач · Стоматолог-хирург, имплантолог, ортопед, терапевт',
      exp: 'Стаж 25 лет',
      photo: 'https://dantist-prokshino.ru/wp-content/uploads/2025/10/IMG-20251028-WA0052-1.jpg',
      bio: 'Ведущий хирург клиники. Специализируется на комплексной реабилитации зубочелюстной системы, сложной костной пластике, синус-лифтинге, дентальной имплантации системами Osstem (Южная Корея) и Straumann (Швейцария), а также прецизионном протезировании керамическими винирами и коронками.',
      education: 'Высшее медицинское образование. Регулярные стажировки и сертификационные курсы по имплантологии, хирургическим протоколам и микроскопной эндодонтии.',
      certs: [
        {
          title: 'Osstem: базовый хирургический курс, 2018',
          img: 'https://dantist-prokshino.ru/wp-content/themes/your-clean-template-3/studio-staff/certificates/danielyan-osstem.webp'
        },
        {
          title: 'Имплантация: хирургические и ортопедические протоколы, 2018',
          img: 'https://dantist-prokshino.ru/wp-content/themes/your-clean-template-3/studio-staff/certificates/danielyan-implantation.webp'
        },
        {
          title: 'Препарирование под виниры, 2018',
          img: 'https://dantist-prokshino.ru/wp-content/themes/your-clean-template-3/studio-staff/certificates/danielyan-veneers.webp'
        },
        {
          title: 'Эндодонтия с микроскопом, 2018',
          img: 'https://dantist-prokshino.ru/wp-content/themes/your-clean-template-3/studio-staff/certificates/danielyan-endodontics.webp'
        }
      ]
    },
    nadzhafov: {
      name: 'Наджафов Азер Этибарович',
      role: 'Главный врач (Испанские кварталы) · Стоматолог-терапевт, ортопед, хирург',
      exp: 'Стаж 14 лет',
      photo: 'https://stomatolog-ispanskie-kvartaly.ru/wp-content/themes/your-clean-template-3/studio-staff/portraits/portrait-02.webp',
      bio: 'Специалист в области терапевтической, хирургической и ортопедической стоматологии. Проводит атравматичное удаление зубов любой сложности, прецизионное протезирование и микропротезирование керамическими вкладками и коронками.',
      education: 'Государственный медицинский университет. Сертифицированный специалист по дентальной хирургии и реставрационной стоматологии.',
      certs: [
        {
          title: 'Эстетическая и функциональная реставрация, 2018',
          img: 'https://dantist-prokshino.ru/wp-content/themes/your-clean-template-3/studio-staff/certificates/nadzhafov-restoration.webp'
        }
      ]
    },
    fiasheva: {
      name: 'Фиашева Диана Аслановна',
      role: 'Стоматолог-терапевт, эндодонтист',
      exp: 'Стаж 7 лет',
      photo: 'https://dantist-prokshino.ru/wp-content/themes/your-clean-template-3/studio-staff/portraits/portrait-01.webp',
      bio: 'Специалист по сохранению сложных зубов и высокоэстетической реставрации. Владеет передовыми протоколами инструментальной и медикаментозной обработки корневых каналов под дентальным микроскопом Carl Zeiss, трехмерной обтурацией гуттаперчей и художественным моделированием эмали фотокомпозитами.',
      education: 'Высшее медицинское образование. Специализация по терапевтической стоматологии и микроскопной эндодонтии.',
      certs: []
    },
    karapetyan: {
      name: 'Карапетян Анна Артаковна',
      role: 'Врач-ортодонт',
      exp: 'Стаж 10 лет',
      photo: 'https://stomatolog-ispanskie-kvartaly.ru/wp-content/themes/your-clean-template-3/studio-staff/portraits/anna-karapetyan-960.jpg',
      bio: 'Ведущий ортодонт клиники. Специализируется на ранней ортодонтической коррекции у детей и исправлении сложных аномалий прикуса у взрослых. Работает со всеми видами брекет-систем и прозрачными элайнерами.',
      education: 'Ординатура по специальности «Ортодонтия». Сертификаты по работе с современными биомеханическими системами перемещения зубов.',
      certs: []
    },
    mashrabova: {
      name: 'Машрабова Азиза Махмудовна',
      role: 'Детский стоматолог, терапевт',
      exp: 'Стаж 8 лет',
      photo: 'https://stomatolog-ispanskie-kvartaly.ru/wp-content/themes/your-clean-template-3/studio-staff/portraits/portrait-01.webp',
      bio: 'Специалист по детскому и подростковому стоматологическому приёму. Психологическая адаптация ребенка, безболезненное лечение молочных и постоянных зубов, реминерализирующая терапия и гигиеническое обучение.',
      education: 'Высшее медицинское образование по детской стоматологии и терапевтическому профилю.',
      certs: []
    }
  };

  // --- Mobile Drawer (Supports both sites) ---
  const menuToggles = document.querySelectorAll('#menu-toggle, #menuToggleBtn');
  const mobileNavs = document.querySelectorAll('#mobile-nav, #mobileDrawer');
  const drawerCloseBtns = document.querySelectorAll('#drawerCloseBtn, .drawer-close-btn');

  menuToggles.forEach(toggle => {
    toggle.addEventListener('click', () => {
      const isExpanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', !isExpanded);
      mobileNavs.forEach(nav => {
        nav.classList.toggle('active');
        nav.classList.toggle('is-open');
        nav.setAttribute('aria-hidden', isExpanded ? 'true' : 'false');
      });
      document.body.style.overflow = !isExpanded ? 'hidden' : '';
    });
  });

  function closeAllDrawers() {
    menuToggles.forEach(t => t.setAttribute('aria-expanded', 'false'));
    mobileNavs.forEach(nav => {
      nav.classList.remove('active');
      nav.classList.remove('is-open');
      nav.setAttribute('aria-hidden', 'true');
    });
    document.body.style.overflow = '';
  }

  drawerCloseBtns.forEach(btn => btn.addEventListener('click', closeAllDrawers));

  mobileNavs.forEach(nav => {
    nav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', closeAllDrawers);
    });
    nav.addEventListener('click', (e) => {
      if (e.target === nav) closeAllDrawers();
    });
  });

  // --- Real Booking Modal (No Form Simulation, 3 Real Channels) ---
  const bookingModals = document.querySelectorAll('#booking-modal, #bookingModal');
  const modalCloseBtns = document.querySelectorAll('#modal-close, #modalCloseBtn, .modal-close');
  const selectedServicePills = document.querySelectorAll('#selected-service-pill, #modalSelectedServicePill');
  const selectedServiceNames = document.querySelectorAll('#selected-service-name, #modalSelectedServiceName');

  function openBookingModal(serviceName) {
    bookingModals.forEach(modal => {
      modal.classList.add('active');
      modal.classList.add('is-active');
      modal.setAttribute('aria-hidden', 'false');
    });

    if (serviceName && serviceName.trim()) {
      selectedServiceNames.forEach(el => el.textContent = serviceName.trim());
      selectedServicePills.forEach(el => {
        el.style.display = 'block';
        el.classList.add('is-visible');
      });
    } else {
      selectedServicePills.forEach(el => {
        el.style.display = 'none';
        el.classList.remove('is-visible');
      });
    }

    document.body.style.overflow = 'hidden';
  }

  function closeBookingModal() {
    bookingModals.forEach(modal => {
      modal.classList.remove('active');
      modal.classList.remove('is-active');
      modal.setAttribute('aria-hidden', 'true');
    });
    document.body.style.overflow = '';
  }

  // Universal booking triggers
  document.querySelectorAll('[data-booking-trigger], [data-book], .book-cta-btn, [data-price-book]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const serviceName = btn.getAttribute('data-service-name') || '';
      openBookingModal(serviceName);
    });
  });

  modalCloseBtns.forEach(btn => btn.addEventListener('click', closeBookingModal));

  bookingModals.forEach(modal => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeBookingModal();
    });
  });

  // --- Doctor Dossier Modal ---
  const certsModal = document.getElementById('certs-modal');
  const certsModalClose = document.getElementById('certs-modal-close');
  const certsContent = document.getElementById('certs-modal-content');
  const certTriggers = document.querySelectorAll('[data-doctor-key]');

  function openDoctorModal(key) {
    const doc = doctorsData[key];
    if (!doc || !certsContent || !certsModal) return;

    let certsHtml = '';
    if (doc.certs && doc.certs.length > 0) {
      certsHtml = `
        <div class="dossier-block-title" style="margin-top: 24px;">Дипломы и сертификаты:</div>
        <div class="dossier-certs-grid">
          ${doc.certs.map(c => `
            <a href="${c.img}" target="_blank" rel="noopener" class="cert-thumb-link" title="Посмотреть сертификат">
              <img src="${c.img}" alt="${c.title}" class="cert-thumb-img" loading="lazy">
              <span class="cert-thumb-title">${c.title}</span>
            </a>
          `).join('')}
        </div>
      `;
    }

    certsContent.innerHTML = `
      <div class="dossier-header">
        <img src="${doc.photo}" alt="${doc.name}" class="dossier-photo">
        <div>
          <h2 class="dossier-name">${doc.name}</h2>
          <div class="dossier-role">${doc.role}</div>
          <span class="dossier-exp">${doc.exp}</span>
        </div>
      </div>
      <div class="dossier-body">
        <div class="dossier-block-title">Специализация и клинический опыт:</div>
        <p class="dossier-block-text">${doc.bio}</p>

        <div class="dossier-block-title">Образование и квалификация:</div>
        <p class="dossier-block-text">${doc.education}</p>

        ${certsHtml}
      </div>
    `;

    certsModal.classList.add('active');
    certsModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeDoctorModal() {
    if (certsModal) {
      certsModal.classList.remove('active');
      certsModal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }
  }

  certTriggers.forEach(btn => {
    btn.addEventListener('click', () => {
      const key = btn.getAttribute('data-doctor-key');
      openDoctorModal(key);
    });
  });

  if (certsModalClose) certsModalClose.addEventListener('click', closeDoctorModal);
  if (certsModal) {
    certsModal.addEventListener('click', (e) => {
      if (e.target === certsModal) closeDoctorModal();
    });
  }

  // Keyboard navigation (Escape key)
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeBookingModal();
      closeDoctorModal();
      closeAllDrawers();
    }
  });

  // --- Price Catalogue Search & Category Filtering ---
  const searchInput = document.getElementById('catalogue-search') || document.getElementById('price-search');
  const priceCategories = document.querySelectorAll('.price-category');
  const catChips = document.querySelectorAll('.price-cat-chip, .tab-btn, .price-category-btn');

  function filterPrices() {
    const query = searchInput ? searchInput.value.toLowerCase().trim() : '';

    priceCategories.forEach(cat => {
      let catHasMatch = false;
      const rows = cat.querySelectorAll('.price-row, .price-table tr:not(:first-child)');

      rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (query === '' || text.includes(query)) {
          row.style.display = '';
          catHasMatch = true;
        } else {
          row.style.display = 'none';
        }
      });

      if (catHasMatch || query === '') {
        cat.style.display = '';
      } else {
        cat.style.display = 'none';
      }
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', filterPrices);
  }

  catChips.forEach(chip => {
    chip.addEventListener('click', () => {
      catChips.forEach(c => {
        c.classList.remove('active');
        c.classList.remove('is-active');
        c.setAttribute('aria-selected', 'false');
      });
      chip.classList.add('active');
      chip.classList.add('is-active');
      chip.setAttribute('aria-selected', 'true');

      const targetCat = chip.getAttribute('data-cat-filter') || chip.getAttribute('data-target-category') || 'all';

      priceCategories.forEach(cat => {
        const catId = cat.getAttribute('data-price-category') || cat.id;
        if (targetCat === 'all' || catId === targetCat) {
          cat.style.display = '';
        } else {
          cat.style.display = 'none';
        }
      });
    });
  });

  // Accordion details toggle inside price rows
  document.querySelectorAll('[data-price-toggle]').forEach(trigger => {
    trigger.addEventListener('click', () => {
      const row = trigger.closest('.price-row');
      const detail = row ? row.querySelector('[data-price-detail]') : null;
      if (detail) {
        const isHidden = detail.hasAttribute('hidden');
        if (isHidden) {
          detail.removeAttribute('hidden');
          trigger.setAttribute('aria-expanded', 'true');
        } else {
          detail.setAttribute('hidden', '');
          trigger.setAttribute('aria-expanded', 'false');
        }
      }
    });
  });

  // Quick booking buttons in price list rows
  document.querySelectorAll('.price-detail-booking-btn, [data-price-book], .price-book-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const row = btn.closest('.price-row, tr');
      const nameEl = row ? (row.querySelector('.price-item-name') || row.querySelector('.price-col-service') || row.querySelector('.price-detail-title')) : null;
      const title = nameEl ? nameEl.textContent.trim() : '';
      openBookingModal(title);
    });
  });
});
