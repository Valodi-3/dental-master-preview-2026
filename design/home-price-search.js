(() => {
  'use strict';

  function initHomePriceSearch() {
    const root = document.querySelector('[data-home-price-search]');
    if (!root) return;

    const input = root.querySelector('#price-search');
    const rows = Array.from(root.querySelectorAll('[data-home-price-row]'));
    const empty = root.querySelector('[data-home-price-empty]');
    const status = root.querySelector('[data-home-price-status]');
    if (!input || rows.length === 0) return;

    function updateResults() {
      const query = input.value.trim().toLocaleLowerCase('ru-RU');
      let visible = 0;
      for (const row of rows) {
        const text = `${row.textContent || ''} ${row.dataset.search || ''}`.toLocaleLowerCase('ru-RU');
        const match = !query || text.includes(query);
        row.hidden = !match;
        if (match) visible += 1;
      }
      if (empty) empty.hidden = visible !== 0;
      if (status) {
        status.textContent = query
          ? `В быстрых примерах: ${visible}. Полный каталог содержит 254 услуги.`
          : 'Быстрые примеры из официального прайса. Полный каталог — 254 услуги.';
      }
    }

    input.addEventListener('input', updateResults);
    updateResults();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHomePriceSearch, { once: true });
  } else {
    initHomePriceSearch();
  }
})();
