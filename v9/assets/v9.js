/**
 * DENTAL MASTER V9 — INTERACTIVE LOGIC
 * Engineered on REGINA V16 UX principles:
 * - 3-step tactile service configuration
 * - Non-disruptive choice booking dialog
 * - Zero simulated fake booking
 * - Accessible keyboard & screen reader support
 */

(function () {
  'use strict';

  // --- Real Service Catalog for Configurator ---
  const CONFIGURATOR_DATA = {
    treatment: {
      categoryName: 'Лечение зубов',
      procedures: [
        {
          id: 'svc_treatment_027',
          name: 'Восстановление зуба пломбой (1 поверхность)',
          shortDesc: 'Лечение поверхностного и среднего кариеса современными светоотверждаемыми композитами с восстановлением анатомии зуба.',
          price: '4 950 ₽',
          duration: '45 мин',
          img: '../design/assets/prokshino/treatment.webp',
          tag: 'Терапия кариеса'
        },
        {
          id: 'svc_treatment_028',
          name: 'Восстановление зуба пломбой (2 поверхности)',
          shortDesc: 'Пломбирование при контактном кариесе с созданием правильного плотного контактного пункта зубной нити.',
          price: '5 500 ₽',
          duration: '50 мин',
          img: '../design/assets/prokshino/treatment.webp',
          tag: 'Контактный кариес'
        },
        {
          id: 'svc_treatment_029',
          name: 'Эстетическая реставрация зуба (3 поверхности)',
          shortDesc: 'Послойное художественное восстановление разрушенной коронковой части зуба с воссозданием фиссур и бугров.',
          price: '6 050 ₽',
          duration: '60 мин',
          img: '../design/assets/prokshino/treatment.webp',
          tag: 'Реставрация'
        }
      ]
    },
    endodontics: {
      categoryName: 'Микроскопия Zeiss',
      procedures: [
        {
          id: 'svc_endodontics_055',
          name: 'Лечение корневых каналов под микроскопом Zeiss',
          shortDesc: 'Немецкая оптика Carl Zeiss с 25-кратным увеличением. Позволяет найти скрытые микроканалы и спасти безнадежные зубы.',
          price: '7 150 ₽',
          duration: '60–90 мин',
          img: '../design/assets/prokshino/microscope.webp',
          tag: 'Carl Zeiss 25x'
        },
        {
          id: 'svc_endodontics_048',
          name: 'Инструментальная обработка каналов с оптикой',
          shortDesc: 'Прецизионная механическая обработка никель-титановыми ротационными инструментами под постоянным визуальным контролем.',
          price: '1 320 ₽',
          duration: '45 мин',
          img: '../design/assets/prokshino/microscope.webp',
          tag: 'Обработка каналов'
        },
        {
          id: 'svc_endodontics_049',
          name: 'Временное пломбирование лечебной пастой',
          shortDesc: 'Антисептическая терапия кальцийсодержащими препаратами для снятия воспаления в периодонте перед постоянным пломбированием.',
          price: '880 ₽',
          duration: '30 мин',
          img: '../design/assets/prokshino/microscope.webp',
          tag: 'Терапия периодонтита'
        }
      ]
    },
    implantation: {
      categoryName: 'Имплантация',
      procedures: [
        {
          id: 'svc_implantation_091',
          name: 'Установка имплантата Osstem (Корея) под ключ',
          shortDesc: 'Надежная корейская система с приживаемостью более 99%. Компьютерное 3D-планирование и атравматичный хирургический протокол.',
          price: '33 000 ₽',
          duration: '45–60 мин',
          img: '../design/assets/prokshino/treatment.webp',
          tag: 'Osstem Implant'
        },
        {
          id: 'svc_implantation_093',
          name: 'Установка премиум-имплантата Straumann (Швейцария)',
          shortDesc: 'Золотой стандарт мировой дентальной имплантологии. Пожизненная международная гарантия и ускоренная остеоинтеграция Roxolid SLActive.',
          price: '66 000 ₽',
          duration: '45–60 мин',
          img: '../design/assets/prokshino/treatment.webp',
          tag: 'Straumann Swiss'
        },
        {
          id: 'svc_implantation_092',
          name: 'Установка формирователя десны',
          shortDesc: 'Формирование эстетичного естественного контура десневого края вокруг будущего искусственного зуба.',
          price: '4 400 ₽',
          duration: '30 мин',
          img: '../design/assets/prokshino/treatment.webp',
          tag: 'Пластика десны'
        }
      ]
    },
    orthodontics: {
      categoryName: 'Ортодонтия и прикус',
      procedures: [
        {
          id: 'svc_orthodontics_211',
          name: 'Фиксация брекет-системы металл (1 челюсть)',
          shortDesc: 'Надежная классическая брекет-система для точного исправления нарушений прикуса любой сложности у подростков и взрослых.',
          price: '75 000 ₽',
          duration: '60 мин',
          img: '../design/assets/prokshino/orthodontics.webp',
          tag: 'Брекеты металл'
        },
        {
          id: 'svc_orthodontics_212',
          name: 'Самолигирующая брекет-система Damon (1 челюсть)',
          shortDesc: 'Низкотрениевая система с мягкими биологическими силами. Меньше визитов в клинику и более комфортное перемещение зубов.',
          price: '75 000 ₽',
          duration: '60 мин',
          img: '../design/assets/prokshino/orthodontics.webp',
          tag: 'Damon System'
        },
        {
          id: 'svc_consultations_002',
          name: 'Первичный прием врача-ортодонта с диагностикой',
          shortDesc: 'Фотометрия лица и улыбки, анализ профиля, снятие диагностических слепков и планирование траектории исправления прикуса.',
          price: '880 ₽',
          duration: '40 мин',
          img: '../design/assets/prokshino/orthodontics.webp',
          tag: 'Консультация ортодонта'
        }
      ]
    },
    prosthetics: {
      categoryName: 'Протезирование',
      procedures: [
        {
          id: 'svc_prosthetics_127',
          name: 'Металлокерамическая коронка на зуб',
          shortDesc: 'Прочная проверенная конструкция для восстановления жевательных зубов. Точное краевое прилегание к уступу.',
          price: '14 300 ₽',
          duration: '45 мин',
          img: '../design/assets/prokshino/hero-clinic.webp',
          tag: 'Металлокерамика'
        },
        {
          id: 'svc_prosthetics_122',
          name: 'Коронка с использованием циркониевой вкладки',
          shortDesc: 'Безметалловая эстетика высшего класса. Диоксид циркония исключает темную кайму у десны и обеспечивает долговечность.',
          price: '11 000 ₽',
          duration: '45 мин',
          img: '../design/assets/prokshino/hero-clinic.webp',
          tag: 'Цирконий'
        },
        {
          id: 'svc_prosthetics_117',
          name: 'Временная коронка прямым методом',
          shortDesc: 'Защита обработанного зуба от температурных раздражителей и сохранение эстетики на период изготовления постоянной коронки.',
          price: '3 850 ₽',
          duration: '30 мин',
          img: '../design/assets/prokshino/hero-clinic.webp',
          tag: 'Временная коронка'
        }
      ]
    },
    hygiene: {
      categoryName: 'Гигиена и уход',
      procedures: [
        {
          id: 'svc_hygiene_012',
          name: 'Профессиональная гигиена полости рта и зубов',
          shortDesc: 'Комплекс AirFlow с мелкодисперсным порошком + ультразвуковое снятие камня + полировка пастами и покрытие фторлаком.',
          price: '6 000 ₽',
          duration: '60 мин',
          img: '../design/assets/prokshino/hygiene.webp',
          tag: 'AirFlow комплекс'
        },
        {
          id: 'svc_hygiene_014',
          name: 'Удаление зубного камня ультразвуком (1 зуб)',
          shortDesc: 'Точечное деликатное удаление поддесневых и наддесневых минерализованных отложений с сохранением эмали.',
          price: '440 ₽',
          duration: '20 мин',
          img: '../design/assets/prokshino/hygiene.webp',
          tag: 'Ультразвук'
        },
        {
          id: 'svc_hygiene_013',
          name: 'Реминерализирующая терапия эмали',
          shortDesc: 'Насыщение ослабленной эмали соединениями кальция и фосфора для снятия чувствительности и профилактики кариеса.',
          price: '275 ₽',
          duration: '15 мин',
          img: '../design/assets/prokshino/hygiene.webp',
          tag: 'Реминерализация'
        }
      ]
    }
  };

  // --- 1. Init Configurator ---
  function initConfigurator() {
    const root = document.querySelector('[data-v9-configurator]');
    if (!root) return;

    const catTabs = root.querySelectorAll('[data-config-cat]');
    const procContainer = root.querySelector('[data-config-proc-list]');
    const resultImg = root.querySelector('[data-result-img]');
    const resultTag = root.querySelector('[data-result-tag]');
    const resultTitle = root.querySelector('[data-result-title]');
    const resultDesc = root.querySelector('[data-result-desc]');
    const resultPrice = root.querySelector('[data-result-price]');
    const resultDuration = root.querySelector('[data-result-duration]');
    const resultBookBtn = root.querySelector('[data-result-book]');

    let currentCat = 'treatment';
    let currentProcIndex = 0;

    function renderProcedures(catKey) {
      currentCat = catKey;
      const data = CONFIGURATOR_DATA[catKey];
      if (!data || !procContainer) return;

      procContainer.innerHTML = '';
      data.procedures.forEach((proc, idx) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = `config-proc-btn ${idx === currentProcIndex ? 'is-active' : ''}`;
        btn.setAttribute('role', 'tab');
        btn.setAttribute('aria-selected', String(idx === currentProcIndex));
        btn.innerHTML = `
          <div class="proc-btn-info">
            <strong>${proc.name}</strong>
            <small>${proc.tag} · ${proc.duration}</small>
          </div>
          <span class="proc-btn-price">${proc.price}</span>
        `;

        btn.addEventListener('click', () => {
          currentProcIndex = idx;
          procContainer.querySelectorAll('.config-proc-btn').forEach((b, i) => {
            const active = i === idx;
            b.classList.toggle('is-active', active);
            b.setAttribute('aria-selected', String(active));
          });
          updateResultStage(proc);
        });

        procContainer.appendChild(btn);
      });

      updateResultStage(data.procedures[currentProcIndex]);
    }

    function updateResultStage(proc) {
      if (!proc) return;

      if (resultImg) {
        resultImg.classList.add('is-fading');
        resultImg.src = proc.img;
        resultImg.alt = proc.name;
        resultImg.onload = () => resultImg.classList.remove('is-fading');
      }

      if (resultTag) resultTag.textContent = proc.tag;
      if (resultTitle) resultTitle.textContent = proc.name;
      if (resultDesc) resultDesc.textContent = proc.shortDesc;
      if (resultPrice) resultPrice.textContent = proc.price;
      if (resultDuration) resultDuration.textContent = proc.duration;

      if (resultBookBtn) {
        resultBookBtn.dataset.serviceName = proc.name;
        resultBookBtn.dataset.servicePrice = proc.price;
      }
    }

    catTabs.forEach((tab) => {
      tab.addEventListener('click', () => {
        catTabs.forEach((t) => {
          t.classList.remove('is-active');
          t.setAttribute('aria-selected', 'false');
        });
        tab.classList.add('is-active');
        tab.setAttribute('aria-selected', 'true');

        currentProcIndex = 0;
        renderProcedures(tab.dataset.configCat);
      });
    });

    // Initial render
    renderProcedures('treatment');
  }

  // --- 2. Booking Choice Modal (REGINA Choice Dialog UX) ---
  function initBookingModal() {
    const modal = document.querySelector('#bookingChoiceModal');
    if (!modal) return;

    const contextEl = modal.querySelector('#bookingChoiceContext');
    const closeBtn = modal.querySelector('#bookingChoiceClose');
    const copyBtn = modal.querySelector('[data-copy-phone]');
    const copyStatus = modal.querySelector('[data-copy-status]');

    let returnFocusEl = null;

    function open(serviceName = null, servicePrice = null, triggerEl = null) {
      returnFocusEl = triggerEl || document.activeElement;

      if (serviceName && contextEl) {
        contextEl.innerHTML = `
          <div class="choice-context-pill">
            <div>
              <span style="font-size:0.72rem; color:var(--v9-text-dim); text-transform:uppercase; display:block; letter-spacing:0.06em;">Выбранная процедура:</span>
              <strong>${serviceName}</strong>
            </div>
            ${servicePrice ? `<span>${servicePrice}</span>` : ''}
          </div>
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

      // Focus first actionable button
      const firstBtn = modal.querySelector('button:not([disabled]), a:not([disabled])');
      if (firstBtn) firstBtn.focus();
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

    // Global click listener for open triggers
    document.addEventListener('click', (event) => {
      const openTrigger = event.target.closest('[data-open-booking]');
      if (openTrigger) {
        event.preventDefault();
        const sName = openTrigger.dataset.serviceName || null;
        const sPrice = openTrigger.dataset.servicePrice || null;
        open(sName, sPrice, openTrigger);
        return;
      }

      if (event.target.closest('#bookingChoiceClose')) {
        event.preventDefault();
        close();
        return;
      }

      // Backdrop click
      if (event.target === modal) {
        close();
      }
    });

    // Escape key listener
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && modal.classList.contains('is-open')) {
        close();
      }
    });

    // Clipboard copy handler
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
    const bar = document.querySelector('.v9-mobile-bar');
    const heroCta = document.querySelector('[data-hero-cta]');
    const footer = document.querySelector('.v9-footer');
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

  // --- 4. Interactive Photo Tour Logic (salon.html principle) ---
  function initPhotoTour() {
    const tourScene = document.querySelector('[data-tour-scene]');
    if (!tourScene) return;

    const photoA = tourScene.querySelector('#tourPhotoA');
    const photoB = tourScene.querySelector('#tourPhotoB');
    const counterEl = document.querySelector('#tourPhotoCounter');
    const titleEl = document.querySelector('#tourPhotoTitle');
    const prevBtn = document.querySelector('#tourPrevPhoto');
    const nextBtn = document.querySelector('#tourNextPhoto');
    const chapterBtns = document.querySelectorAll('[data-tour-chapter]');

    const TOUR_ITEMS = [
      {
        src: '../design/assets/prokshino/hero-clinic.webp',
        title: 'Главный холл и зона консультации пациентов',
        category: 'interior'
      },
      {
        src: '../design/assets/prokshino/microscope.webp',
        title: 'Операционный кабинет с микроскопом Carl Zeiss',
        category: 'equipment'
      },
      {
        src: '../design/assets/prokshino/treatment.webp',
        title: 'Хирургический кабинет имплантации и навигации',
        category: 'cabinets'
      },
      {
        src: '../design/assets/prokshino/orthodontics.webp',
        title: 'Ортодонтическое рабочее место и 3D-сетап',
        category: 'equipment'
      },
      {
        src: '../design/assets/prokshino/hygiene.webp',
        title: 'Кабинет гигиены полости рта и спа-протокола AirFlow',
        category: 'cabinets'
      },
      {
        src: '../design/assets/ispanskie/gallery-1.jpg',
        title: 'Стерилизационный блок и стандарты антисептики',
        category: 'interior'
      }
    ];

    let currentIndex = 0;
    let activePhoto = 'A'; // 'A' or 'B' for cross-fade

    function updatePhoto(index) {
      if (index < 0) index = TOUR_ITEMS.length - 1;
      if (index >= TOUR_ITEMS.length) index = 0;
      currentIndex = index;

      const item = TOUR_ITEMS[currentIndex];
      const targetPhoto = activePhoto === 'A' ? photoB : photoA;
      const currentPhoto = activePhoto === 'A' ? photoA : photoB;

      targetPhoto.src = item.src;
      targetPhoto.alt = item.title;
      targetPhoto.onload = () => {
        targetPhoto.classList.add('is-active');
        currentPhoto.classList.remove('is-active');
        activePhoto = activePhoto === 'A' ? 'B' : 'A';
      };

      if (counterEl) {
        counterEl.textContent = `${String(currentIndex + 1).padStart(2, '0')} / ${String(TOUR_ITEMS.length).padStart(2, '0')} · Фото клиники`;
      }
      if (titleEl) {
        titleEl.textContent = item.title;
      }
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', () => updatePhoto(currentIndex - 1));
    }
    if (nextBtn) {
      nextBtn.addEventListener('click', () => updatePhoto(currentIndex + 1));
    }

    chapterBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        chapterBtns.forEach((b) => b.classList.remove('is-active'));
        btn.classList.add('is-active');
        const cat = btn.dataset.tourChapter;
        const foundIdx = TOUR_ITEMS.findIndex((item) => cat === 'all' || item.category === cat);
        if (foundIdx !== -1) updatePhoto(foundIdx);
      });
    });

    // Touch swipe support for tour
    let touchStartX = 0;
    tourScene.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    tourScene.addEventListener('touchend', (e) => {
      const diffX = e.changedTouches[0].screenX - touchStartX;
      if (Math.abs(diffX) > 40) {
        if (diffX < 0) updatePhoto(currentIndex + 1);
        else updatePhoto(currentIndex - 1);
      }
    }, { passive: true });
  }

  // Initialize all components
  document.addEventListener('DOMContentLoaded', () => {
    initConfigurator();
    initBookingModal();
    initMobileBar();
    initPhotoTour();
  });
})();
