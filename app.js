/**
 * ДАНТИСТЪ — VNext Interactive Controller (RC-4)
 * Handles: Booking Modal, Doctor Dossier Modal, Mobile Drawer, Price Filter & Search
 */

document.addEventListener('DOMContentLoaded', () => {
  'use strict';

  // --- Doctor Dossier Data ---
  const doctorsData = {
    danielyan: {
      name: 'Даниелян Арам Яковлевич',
      role: 'Главный врач · Стоматолог-хирург, имплантолог, ортопед, терапевт',
      exp: 'Стаж 25 лет',
      photo: 'https://dantist-prokshino.ru/wp-content/uploads/2025/10/IMG-20251028-WA0052-1.jpg',
      bio: 'Ведущий хирург и основатель клинической практики. Специализируется на комплексной реабилитации зубочелюстной системы, сложной костной пластике, синус-лифтинге, дентальной имплантации системами Osstem (Южная Корея) и Straumann (Швейцария), а также прецизионном протезировании керамическими винирами и коронками.',
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
      role: 'Врач-стоматолог, хирург-имплантолог',
      exp: 'Стаж 10 лет',
      photo: 'https://dantist-prokshino.ru/wp-content/themes/your-clean-template-3/studio-staff/portraits/portrait-02.webp',
      bio: 'Эксперт в области амбулаторной хирургии и дентальной имплантации. Проводит атравматичное удаление зубов любой сложности (включая ретинированные и дистопированные восьмерки), одномоментную имплантацию с установкой формирователя десны, пластику мягких тканей полости рта.',
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
      bio: 'Специалист по сохранению сложных зубов и высокоэстетической реставрации. Владеет передовыми протоколами инструментальной и медикаментозной обработки корневых каналов под увеличением дентального микроскопа Carl Zeiss, трехмерной обтурацией гуттаперчей и художественным моделированием эмали фотокомпозитами.',
      education: 'Высшее медицинское образование. Специализация по терапевтической стоматологии и микроскопной эндодонтии.',
      certs: []
    },
    karapetyan: {
      name: 'Карапетян Анна Артаковна',
      role: 'Врач-ортодонт',
      exp: 'Стаж более 10 лет',
      photo: 'https://dantist-prokshino.ru/wp-content/themes/your-clean-template-3/studio-staff/portraits/anna-karapetyan-960.jpg',
      bio: 'Ведущий ортодонт клиники. Специализируется на ранней ортодонтической коррекции у детей и исправлении сложных аномалий прикуса у взрослых. Работает со всеми видами брекет-систем (самолигирующие Damon, керамические эстетические брекеты) и прозрачными элайнерами.',
      education: 'Ординатура по специальности «Ортодонтия». Сертификаты по работе с современными биомеханическими системами перемещения зубов.',
      certs: []
    }
  };

  // --- Mobile Drawer ---
  const menuToggle = document.getElementById('menu-toggle');
  const mobileNav = document.getElementById('mobile-nav');
  if (menuToggle && mobileNav) {
    menuToggle.addEventListener('click', () => {
      const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
      menuToggle.setAttribute('aria-expanded', !isExpanded);
      mobileNav.classList.toggle('active');
    });

    mobileNav.querySelectorAll('.mobile-link').forEach(link => {
      link.addEventListener('click', () => {
        menuToggle.setAttribute('aria-expanded', 'false');
        mobileNav.classList.remove('active');
      });
    });
  }

  // --- Booking Modal ---
  const bookingModal = document.getElementById('booking-modal');
  const bookingModalClose = document.getElementById('booking-modal-close');
  const bookingTriggers = document.querySelectorAll('[data-open-booking]');
  const quickForm = document.getElementById('quick-booking-form');
  const quickSuccess = document.getElementById('booking-success-message');
  const serviceInput = document.getElementById('client-service');

  function openBookingModal(serviceName) {
    if (bookingModal) {
      if (serviceName && serviceInput) {
        serviceInput.value = serviceName;
      }
      bookingModal.classList.add('active');
      bookingModal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeBookingModal() {
    if (bookingModal) {
      bookingModal.classList.remove('active');
      bookingModal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }
  }

  bookingTriggers.forEach(btn => {
    btn.addEventListener('click', () => {
      const service = btn.getAttribute('data-service') || '';
      openBookingModal(service);
    });
  });

  if (bookingModalClose) {
    bookingModalClose.addEventListener('click', closeBookingModal);
  }

  if (bookingModal) {
    bookingModal.addEventListener('click', (e) => {
      if (e.target === bookingModal) closeBookingModal();
    });
  }

  if (quickForm) {
    quickForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const submitBtn = quickForm.querySelector('button[type="submit"]');
      if (submitBtn) submitBtn.disabled = true;
      if (quickSuccess) quickSuccess.style.display = 'block';
      setTimeout(() => {
        quickForm.reset();
        if (submitBtn) submitBtn.disabled = false;
        setTimeout(closeBookingModal, 2500);
      }, 1000);
    });
  }

  // --- Doctor Dossier Modal ---
  const certsModal = document.getElementById('certs-modal');
  const certsModalClose = document.getElementById('certs-modal-close');
  const certsContent = document.getElementById('certs-modal-content');
  const certTriggers = document.querySelectorAll('[data-open-certs]');

  function openDoctorModal(docKey) {
    const doc = doctorsData[docKey];
    if (!doc || !certsContent || !certsModal) return;

    let certsHtml = '';
    if (doc.certs && doc.certs.length > 0) {
      certsHtml = `
        <div class="dossier-block-title">Подтверждённые сертификаты обучения (${doc.certs.length}):</div>
        <div class="certs-gallery">
          ${doc.certs.map(c => `
            <a href="${c.img}" target="_blank" rel="noopener noreferrer" class="cert-thumb-link" title="Открыть в полном размере">
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

  if (certsModalClose) {
    certsModalClose.addEventListener('click', closeDoctorModal);
  }

  if (certsModal) {
    certsModal.addEventListener('click', (e) => {
      if (e.target === certsModal) closeDoctorModal();
    });
  }

  // Escape key handler for modals
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeBookingModal();
      closeDoctorModal();
    }
  });

  // --- Price Catalogue Search & Category Filtering ---
  const searchInput = document.getElementById('price-search') || document.getElementById('catalogue-search');
  const priceCategories = document.querySelectorAll('.price-category');
  const tabButtons = document.querySelectorAll('.tab-btn');

  function filterPrices() {
    const query = searchInput ? searchInput.value.toLowerCase().trim() : '';

    priceCategories.forEach(cat => {
      let catHasMatch = false;
      const rows = cat.querySelectorAll('.price-row');

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

  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      tabButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const targetCat = btn.getAttribute('data-target-category');

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

  // Booking buttons inside price list rows
  document.querySelectorAll('.price-cell-action button, .marketing-category-link, [data-price-book]').forEach(btn => {
    btn.addEventListener('click', () => {
      const row = btn.closest('.price-row');
      const title = row ? row.querySelector('.price-cell-title').childNodes[0].textContent.trim() : '';
      openBookingModal(title);
    });
  });
});
