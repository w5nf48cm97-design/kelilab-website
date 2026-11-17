'use strict';

const menuButton = document.querySelector('[data-menu-button]');
const navigation = document.querySelector('[data-navigation]');
if (menuButton && navigation) {
  menuButton.addEventListener('click', function () {
    const open = menuButton.getAttribute('aria-expanded') === 'true';
    menuButton.setAttribute('aria-expanded', String(!open));
    navigation.classList.toggle('is-open', !open);
  });
  navigation.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function () {
      navigation.classList.remove('is-open');
      menuButton.setAttribute('aria-expanded', 'false');
    });
  });
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
      navigation.classList.remove('is-open');
      menuButton.setAttribute('aria-expanded', 'false');
    }
  });
}

const appSearch = document.querySelector('[data-app-search]');
const appCards = Array.from(document.querySelectorAll('[data-app-card]'));
const filterButtons = Array.from(document.querySelectorAll('[data-filter]'));
const emptyResult = document.querySelector('[data-empty-result]');
const resultCount = document.querySelector('[data-result-count]');
let selectedFilter = 'all';

function normalize(text) {
  return text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
}

function filterApps() {
  const query = normalize(appSearch ? appSearch.value.trim() : '');
  let visible = 0;
  appCards.forEach(function (card) {
    const categoryMatches = selectedFilter === 'all' || card.dataset.category === selectedFilter;
    const searchMatches = normalize(card.dataset.search).includes(query);
    card.hidden = !(categoryMatches && searchMatches);
    if (!card.hidden) visible += 1;
  });
  if (emptyResult) emptyResult.hidden = visible !== 0;
  if (resultCount) resultCount.textContent = visible + (visible === 1 ? ' proyecto' : ' proyectos');
}

if (appSearch) appSearch.addEventListener('input', filterApps);
filterButtons.forEach(function (button) {
  button.addEventListener('click', function () {
    selectedFilter = button.dataset.filter;
    filterButtons.forEach(function (filter) {
      const active = filter === button;
      filter.setAttribute('aria-pressed', String(active));
      filter.classList.toggle('is-active', active);
    });
    filterApps();
  });
});
const resetSearch = document.querySelector('[data-reset-search]');
if (resetSearch) resetSearch.addEventListener('click', function () {
  if (appSearch) appSearch.value = '';
  selectedFilter = 'all';
  filterButtons.forEach(function (button) {
    const active = button.dataset.filter === 'all';
    button.classList.toggle('is-active', active);
    button.setAttribute('aria-pressed', String(active));
  });
  filterApps();
  if (appSearch) appSearch.focus();
});

const modal = document.querySelector('[data-image-dialog]');
if (modal && typeof modal.showModal === 'function') {
  const modalImage = modal.querySelector('img');
  const modalCaption = modal.querySelector('[data-dialog-caption]');
  document.querySelectorAll('[data-enlarge]').forEach(function (button) {
    button.addEventListener('click', function () {
      const image = button.querySelector('img');
      modalImage.src = image.src;
      modalImage.alt = image.alt;
      modalCaption.textContent = image.alt;
      modal.showModal();
    });
  });
  modal.querySelector('[data-close-dialog]').addEventListener('click', function () { modal.close(); });
  modal.addEventListener('click', function (event) {
    if (event.target === modal) {
      const bounds = modal.getBoundingClientRect();
      if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) modal.close();
    }
  });
}
