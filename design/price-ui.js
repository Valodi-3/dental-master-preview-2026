(() => {
  'use strict';

  // The existing shared controller supplies the mobile drawer and detail accordions.
  // This design-owned pass keeps search and category selection as a true intersection.
  document.addEventListener('DOMContentLoaded', () => {
    const search = document.getElementById('price-search');
    const count = document.getElementById('price-catalog-count');
    const empty = document.getElementById('price-catalog-empty');
    const categories = Array.from(document.querySelectorAll('.price-category'));
    const chips = Array.from(document.querySelectorAll('.price-cat-chip'));
    let activeCategory = chips.find(chip => chip.classList.contains('active'))?.dataset.catFilter || 'all';

    if (!count || categories.length === 0) return;

    function applyCatalogFilters() {
      const query = (search?.value || '').trim().toLocaleLowerCase('ru-RU');
      let visibleCount = 0;

      categories.forEach(category => {
        const categoryId = category.dataset.priceCategory || category.id;
        const categoryAllowed = activeCategory === 'all' || categoryId === activeCategory;
        let categoryMatches = 0;

        category.querySelectorAll('.price-row').forEach(row => {
          const matches = categoryAllowed && (!query || row.textContent.toLocaleLowerCase('ru-RU').includes(query));
          row.style.display = matches ? '' : 'none';
          if (matches) {
            categoryMatches += 1;
            visibleCount += 1;
          }
        });

        category.style.display = categoryMatches > 0 || (activeCategory === 'all' && !query) ? '' : 'none';
      });

      count.textContent = `Показано услуг: ${visibleCount}`;
      if (empty) empty.hidden = visibleCount !== 0;
    }

    if (search) search.addEventListener('input', applyCatalogFilters);
    chips.forEach(chip => {
      chip.addEventListener('click', () => {
        activeCategory = chip.dataset.catFilter || 'all';
        applyCatalogFilters();
      });
    });

    applyCatalogFilters();
  });
})();
