'use strict';

// Progressive enhancement: the complete register is already in the HTML.
(() => {
  const form = document.getElementById('filter-form');
  if (!form) return;
  const search = document.getElementById('search');
  const status = document.getElementById('status-filter');
  const category = document.getElementById('category-filter');
  const counter = document.getElementById('result-count');
  const empty = document.getElementById('empty-state');
  const claims = Array.from(document.querySelectorAll('.claim'));
  function filter() {
    const terms = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let shown = 0;
    for (const claim of claims) {
      const matches = terms.every(term => claim.dataset.search.includes(term)) &&
        (status.value === 'all' || claim.dataset.status === status.value) &&
        (category.value === 'all' || claim.dataset.category === category.value);
      claim.hidden = !matches;
      if (matches) shown += 1;
    }
    counter.textContent = `Showing ${shown} of ${claims.length} claims`;
    empty.hidden = shown !== 0;
  }
  form.addEventListener('submit', event => event.preventDefault());
  search.addEventListener('input', filter);
  status.addEventListener('change', filter);
  category.addEventListener('change', filter);
  form.addEventListener('reset', () => {
    search.value = '';
    status.value = 'all';
    category.value = 'all';
    filter();
  });
})();
