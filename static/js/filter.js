/* filter.js — Catalog filter auto-submit & mobile toggle */

document.addEventListener('DOMContentLoaded', () => {
  const filterForm = document.getElementById('filter-form');
  if (!filterForm) return;

  // Auto-submit on any select/radio/checkbox change
  filterForm.querySelectorAll('select, input[type="radio"]').forEach(el => {
    el.addEventListener('change', () => filterForm.submit());
  });

  // Mobile filter toggle
  const toggleBtn = document.getElementById('filter-toggle');
  const sidebar   = document.getElementById('filter-sidebar');
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      toggleBtn.textContent = sidebar.classList.contains('open') ? 'Hide Filters' : 'Show Filters';
    });
  }

  // Sort select auto-submit
  const sortSelect = document.getElementById('sort-select');
  if (sortSelect) {
    sortSelect.addEventListener('change', () => filterForm.submit());
  }
});
