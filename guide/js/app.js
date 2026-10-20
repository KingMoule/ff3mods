// Entry point: hash router, service worker.
import { h } from './util.js';
import { D, loadData, idx } from './state.js';
import { walkHome, walkChapter } from './walk.js';
import { bestiaryList, monsterDetail } from './bestiary.js';
import { charList, charDetail } from './chars.js';
import { formulasView } from './formulas.js';
import { moreView, applyTheme } from './more.js';

const view = document.getElementById('view');
const titleEl = document.getElementById('title');
const subEl = document.getElementById('sub');
const backEl = document.getElementById('back');
const scrollPos = {};
let current = '';

function route() {
  const hash = location.hash.replace(/^#\/?/, '');
  const parts = hash.split('/').filter(Boolean).map(decodeURIComponent);
  const tab = parts[0] || 'walk';
  let res;
  try {
    if (tab === 'walk') {
      if (parts[1]) {
        const c = idx.chap[parts[1]];
        res = { title: c ? c.title : 'Chapter', back: '#/walk', node: walkChapter(parts[1], route) };
      } else res = { title: 'Walkthrough & checklist', node: walkHome(route) };
    } else if (tab === 'bestiary') {
      res = parts[1] ? monsterDetail(+parts[1]) : { title: 'Bestiary', node: bestiaryList() };
    } else if (tab === 'chars') {
      res = parts[1] ? charDetail(parts[1]) : { title: 'Characters', node: charList() };
    } else if (tab === 'formulas') {
      res = { title: 'Formulas (mod version)', back: '#/more', node: formulasView() };
    } else if (tab === 'more') {
      res = moreView(parts.slice(1));
    } else {
      location.hash = '#/walk';
      return;
    }
  } catch (err) {
    console.error(err);
    res = { title: 'Error', node: h('p', null, 'Display error: ' + err.message) };
  }
  scrollPos[current] = window.scrollY;
  current = hash;
  titleEl.textContent = res.title;
  subEl.textContent = res.sub || '';
  backEl.hidden = !res.back;
  backEl.onclick = () => { if (res.back) location.hash = res.back; };
  document.title = res.title + ' — Guide FF6';
  view.replaceChildren(res.node);
  const key = tab === 'formulas' ? 'more' : tab === 'more' && (parts[1] === 'items' || parts[1] === 'espers') ? parts[1] : tab;
  document.querySelectorAll('#tabs a').forEach((a) => a.classList.toggle('on', a.dataset.tab === key));
  window.scrollTo(0, scrollPos[hash] || 0);
}

async function main() {
  applyTheme();
  try {
    await loadData();
  } catch (e) {
    view.replaceChildren(h('p', { class: 'loading' }, 'Could not load the data: ' + e.message));
    return;
  }
  window.addEventListener('hashchange', route);
  route();
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js').catch((e) => console.warn('SW', e));
  }
}
main();
