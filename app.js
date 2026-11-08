/**
 * ДАНТИСТЪ — VNext Interactive Controller (2026)
 * Accessibility-first: WCAG 2.1 AA, Focus Trap, Keyboard Nav & Live Filters
 */

(function () {
  'use strict';

  // State
  let activeFilter = 'all';
  let activeSearchQuery = '';
  let previouslyFocusedElement = null;

  // Elements
  const menuToggle = document.getElementById('menu-toggle');
  const mobileNav = document.getElementById('mobile-nav');
  const filterChips = document.querySelectorAll('.filter-chip');
  const searchInput = document.getElementById('catalogue-search');
  const serviceCards = document.querySelectorAll('.service-card');
  const symptomChips = document.querySelectorAll('.symptom-chip');
  
  // Modals
  const bookingModal = document.getElementById('booking-modal');
  const bookingModalClose = document.getElementById('booking-modal-close');
  const bookingTriggers = document.querySelectorAll('[data-open-booking]');
  const bookingForm = document.getElementById('quick-booking-form');
  const formSuccessBox = document.getElementById('form-success-box');

  const certModal = document.getElementById('cert-modal');
  const certModalClose = document.getElementById('cert-modal-close');
  const certTriggers = document.querySelectorAll('[data-open-certs]');
  const certModalTitle = document.getElementById('cert-modal-title');
  const certModalGallery = document.getElementById('cert-modal-gallery');

  // Certificate database (verified from live clinic template)
  const doctorCertificates = {
    'danielyan': {
      name: 'Даниелян Арам Яковлевич',
      certs: [
        {
          title: 'Osstem: базовый хирургический курс, 2018',
          src: 'https://dantist-prokshino.ru/wp-content/themes/your-clean-template-3/studio-staff/certificates/danielyan-osstem.webp'
        },
        {
          title: 'Имплантация: хирургические и ортопедические протоколы, 2018',
          src: 'https://dantist-prokshino.ru/wp-content/themes/your-clean-template-3/studio-staff/certificates/danielyan-implantation.webp'
        },
        {
          title: 'Препарирование под виниры, 2021',
          src: 'https://dantist-prokshino.ru/wp-content/themes/your-clean-template-3/studio-staff/certificates/danielyan-veneers.webp'
        },
        {
          title: 'Лечение корневых каналов под микроскопом',
          src: 'https://dantist-prokshino.ru/wp-content/themes/your-clean-template-3/studio-staff/certificates/danielyan-endodontics.webp'
        }
      ]
    },
    'nadzhafov': {
      name: 'Наджафов Азер Этибарович',
      certs: [
        {
          title: 'Реставрация жевательной группы зубов, 2019',
          src: 'https://dantist-prokshino.ru/wp-content/themes/your-clean-template-3/studio-staff/certificates/nadzhafov-restoration.webp'
        }
      ]
    },
    'karapetyan': {
      name: 'Карапетян Анна Арменаковна',
      certs: [
        {
          title: 'Художественная реставрация фронтальных зубов, AVS school, 2021',
          src: 'https://dantist-prokshino.ru/wp-content/themes/your-clean-template-3/studio-staff/certificates/karapetyan-restoration-2021.jpg'
        },
        {
          title: 'Ultimate Endo: клиническая эндодонтия от диагностики до обтурации, 2021',
          src: 'https://dantist-prokshino.ru/wp-content/themes/your-clean-template-3/studio-staff/certificates/karapetyan-ultimate-endo-2021.jpg'
        },
        {
          title: 'Курс «Эндодонтическое перелечивание», 2021',
          src: 'https://dantist-prokshino.ru/wp-content/themes/your-clean-template-3/studio-staff/certificates/karapetyan-endodontic-retreatment-2021.jpg'
        }
      ]
    }
  };

  /* ==========================================================================
     1. Mobile Navigation
     ========================================================================== */
  if (menuToggle && mobileNav) {
    menuToggle.addEventListener('click', function () {
      const isOpen = mobileNav.classList.toggle('open');
      menuToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      menuToggle.innerHTML = isOpen ? '✕' : '☰';
    });

    // Close when clicking nav link
    const mobileLinks = mobileNav.querySelectorAll('.mobile-nav-link');
    mobileLinks.forEach(function (link) {
      link.addEventListener('click', function () {
        mobileNav.classList.remove('open');
        menuToggle.setAttribute('aria-expanded', 'false');
        menuToggle.innerHTML = '☰';
      });
    });
  }

  /* ==========================================================================
     2. Services Filter & Search
     ========================================================================== */
  function updateServicesVisibility() {
    let matchCount = 0;
    const query = activeSearchQuery.toLowerCase().trim();

    serviceCards.forEach(function (card) {
      const category = card.getAttribute('data-category');
      const title = (card.querySelector('.service-title')?.textContent || '').toLowerCase();
      const desc = (card.querySelector('.service-desc')?.textContent || '').toLowerCase();
      const scope = (card.getAttribute('data-scope') || '').toLowerCase();

      const matchesCategory = (activeFilter === 'all') || (category === activeFilter);
      const matchesSearch = !query || title.includes(query) || desc.includes(query) || scope.includes(query);

      if (matchesCategory && matchesSearch) {
        card.style.display = '';
        matchCount++;
      } else {
        card.style.display = 'none';
      }
    });

    // Update status counter if element exists
    const counterEl = document.getElementById('catalogue-count');
    if (counterEl) {
      counterEl.textContent = `Показано направлений: ${matchCount}`;
    }
  }

  filterChips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      filterChips.forEach(function (c) {
        c.classList.remove('active');
        c.setAttribute('aria-pressed', 'false');
      });
      chip.classList.add('active');
      chip.setAttribute('aria-pressed', 'true');
      activeFilter = chip.getAttribute('data-filter') || 'all';
      updateServicesVisibility();
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', function (e) {
      activeSearchQuery = e.target.value;
      updateServicesVisibility();
    });
  }

  /* ==========================================================================
     3. Symptom Quick-Click Trigger
     ========================================================================== */
  symptomChips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      const targetFilter = chip.getAttribute('data-filter') || 'all';
      const targetChip = document.querySelector(`.filter-chip[data-filter="${targetFilter}"]`);
      if (targetChip) {
        targetChip.click();
      }
      const servicesSection = document.getElementById('services');
      if (servicesSection) {
        servicesSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* ==========================================================================
     4. Focus Trap & Accessible Modal Manager
     ========================================================================== */
  function getFocusableElements(container) {
    return Array.from(
      container.querySelectorAll(
        'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
      )
    );
  }

  function trapFocus(e, modalContainer) {
    if (e.key !== 'Tab') return;

    const focusables = getFocusableElements(modalContainer);
    if (focusables.length === 0) return;

    const firstFocusable = focusables[0];
    const lastFocusable = focusables[focusables.length - 1];

    if (e.shiftKey) {
      if (document.activeElement === firstFocusable) {
        lastFocusable.focus();
        e.preventDefault();
      }
    } else {
      if (document.activeElement === lastFocusable) {
        firstFocusable.focus();
        e.preventDefault();
      }
    }
  }

  function openModal(modal) {
    if (!modal) return;
    previouslyFocusedElement = document.activeElement;
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';

    const focusables = getFocusableElements(modal);
    if (focusables.length > 0) {
      setTimeout(() => focusables[0].focus(), 50);
    }
  }

  function closeModal(modal) {
    if (!modal) return;
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';

    if (previouslyFocusedElement) {
      previouslyFocusedElement.focus();
    }
  }

  // Booking Modal Events
  bookingTriggers.forEach(function (trigger) {
    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      openModal(bookingModal);
    });
  });

  if (bookingModalClose) {
    bookingModalClose.addEventListener('click', function () {
      closeModal(bookingModal);
    });
  }

  if (bookingModal) {
    bookingModal.addEventListener('click', function (e) {
      if (e.target === bookingModal) {
        closeModal(bookingModal);
      }
    });
    bookingModal.addEventListener('keydown', function (e) {
      trapFocus(e, bookingModal);
    });
  }

  // Certificate Modal Events
  certTriggers.forEach(function (trigger) {
    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      const docKey = trigger.getAttribute('data-doctor-key');
      const docData = doctorCertificates[docKey];

      if (docData && certModalGallery && certModalTitle) {
        certModalTitle.textContent = `Сертификаты: ${docData.name}`;
        certModalGallery.innerHTML = docData.certs.map(function (c) {
          return `
            <div class="cert-item">
              <a href="${c.src}" target="_blank" rel="noopener noreferrer" title="Открыть в полном размере">
                <img src="${c.src}" alt="${c.title}" loading="lazy">
              </a>
              <div class="cert-item-title">${c.title}</div>
            </div>
          `;
        }).join('');

        openModal(certModal);
      }
    });
  });

  if (certModalClose) {
    certModalClose.addEventListener('click', function () {
      closeModal(certModal);
    });
  }

  if (certModal) {
    certModal.addEventListener('click', function (e) {
      if (e.target === certModal) {
        closeModal(certModal);
      }
    });
    certModal.addEventListener('keydown', function (e) {
      trapFocus(e, certModal);
    });
  }

  // Global Escape key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      if (bookingModal && bookingModal.classList.contains('open')) {
        closeModal(bookingModal);
      }
      if (certModal && certModal.classList.contains('open')) {
        closeModal(certModal);
      }
    }
  });

  /* ==========================================================================
     5. Booking Form Submission
     ========================================================================== */
  if (bookingForm) {
    bookingForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const phoneInput = bookingForm.querySelector('input[type="tel"]');
      if (phoneInput && !phoneInput.value.trim()) {
        phoneInput.focus();
        return;
      }

      // Display polite submission state
      if (formSuccessBox) {
        bookingForm.style.display = 'none';
        formSuccessBox.style.display = 'block';
      }
    });
  }



  /* ==========================================================================
     6. Complete 10-Category Price Catalogue Controller (VNext)
     ========================================================================== */
  const priceCatChips = document.querySelectorAll('.price-cat-chip');
  const priceSearchInput = document.getElementById('price-catalog-search');
  const priceCategories = document.querySelectorAll('.price-category');
  const priceRows = document.querySelectorAll('.price-row');
  const priceCountBadge = document.getElementById('price-catalog-count');
  const priceEmptyMsg = document.getElementById('price-catalog-empty');

  let activePriceCategory = 'all';
  let activePriceSearch = '';

  function filterFullPriceCatalog() {
    let visibleCount = 0;
    const query = activePriceSearch.toLowerCase().trim();

    priceCategories.forEach(function (cat) {
      const catId = cat.getAttribute('data-price-category');
      const matchesCategory = (activePriceCategory === 'all' || activePriceCategory === catId);
      
      if (!matchesCategory) {
        cat.style.display = 'none';
        return;
      }

      let visibleInCat = 0;
      const rows = cat.querySelectorAll('.price-row');
      rows.forEach(function (row) {
        const text = row.textContent.toLowerCase();
        const matchesSearch = (!query || text.includes(query));

        if (matchesSearch) {
          row.style.display = '';
          visibleInCat++;
          visibleCount++;
        } else {
          row.style.display = 'none';
        }
      });

      if (visibleInCat > 0) {
        cat.style.display = '';
        const countSpan = cat.querySelector('.price-category-count');
        if (countSpan) {
          countSpan.textContent = 'Показано: ' + visibleInCat;
        }
      } else {
        cat.style.display = 'none';
      }
    });

    if (priceCountBadge) {
      priceCountBadge.innerHTML = 'Показано услуг: <strong>' + visibleCount + '</strong>';
    }

    if (priceEmptyMsg) {
      priceEmptyMsg.hidden = (visibleCount > 0);
    }
  }

  // Category chip event listeners
  priceCatChips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      priceCatChips.forEach(function (c) {
        c.classList.remove('active');
        c.setAttribute('aria-selected', 'false');
      });
      chip.classList.add('active');
      chip.setAttribute('aria-selected', 'true');
      activePriceCategory = chip.getAttribute('data-cat-filter');
      filterFullPriceCatalog();
    });
  });

  // Search input event listener
  if (priceSearchInput) {
    priceSearchInput.addEventListener('input', function (e) {
      activePriceSearch = e.target.value;
      filterFullPriceCatalog();
    });
  }

  // Accordion row trigger event listeners
  document.querySelectorAll('.price-row-trigger').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const isExpanded = btn.getAttribute('aria-expanded') === 'true';
      const detailId = btn.getAttribute('aria-controls');
      const detail = document.getElementById(detailId);

      btn.setAttribute('aria-expanded', !isExpanded);
      if (detail) {
        detail.hidden = isExpanded;
      }
    });
  });

  // Prefill booking modal when booking from specific price item
  document.querySelectorAll('.price-detail-booking-btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const parentRow = btn.closest('.price-row');
      const serviceName = parentRow ? parentRow.querySelector('.price-item-name').textContent.trim() : '';
      
      const commentInput = document.getElementById('booking-comment') || document.querySelector('input[name="comment"]');
      if (commentInput && serviceName) {
        commentInput.value = 'Запись на услугу: ' + serviceName;
      }

      if (bookingModal) {
        openModal(bookingModal);
      }
    });
  });




  // Selected Service Badge Clear button
  const badgeClearBtn = document.getElementById('booking-selected-clear');
  if (badgeClearBtn) {
    badgeClearBtn.addEventListener('click', function () {
      const badgeEl = document.getElementById('booking-selected-badge');
      const badgeName = document.getElementById('booking-selected-name');
      const commentInput = document.getElementById('booking-comment');
      if (badgeEl) badgeEl.hidden = true;
      if (badgeName) badgeName.textContent = '';
      if (commentInput) commentInput.value = '';
    });
  }

})();
