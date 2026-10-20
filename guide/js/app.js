// Point d'entrée : routeur par hash, service worker.
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
        res = { title: c ? c.title : 'Chapitre', back: '#/walk', node: walkChapter(parts[1], route) };
      } else res = { title: 'Marche & checklist', node: walkHome(route) };
    } else if (tab === 'bestiary') {
      res = parts[1] ? monsterDetail(+parts[1]) : { title: 'Bestiaire', node: bestiaryList() };
    } else if (tab === 'chars') {
      res = parts[1] ? charDetail(parts[1]) : { title: 'Personnages', node: charList() };
    } else if (tab === 'formulas') {
      res = { title: 'Formules (version mod)', node: formulasView() };
    } else if (tab === 'more') {
      res = moreView(parts.slice(1));
    } else {
      location.hash = '#/walk';
      return;
    }
  } catch (err) {
    console.error(err);
    res = { title: 'Erreur', node: h('p', null, 'Erreur d\'affichage : ' + err.message) };
  }
  scrollPos[current] = window.scrollY;
  current = hash;
  titleEl.textContent = res.title;
  subEl.textContent = res.sub || '';
  backEl.hidden = !res.back;
  backEl.onclick = () => { if (res.back) location.hash = res.back; };
  document.title = res.title + ' — Guide FF6';
  view.replaceChildren(res.node);
  document.querySelectorAll('#tabs a').forEach((a) => a.classList.toggle('on', a.dataset.tab === tab));
  window.scrollTo(0, scrollPos[hash] || 0);
}

async function main() {
  applyTheme();
  try {
    await loadData();
  } catch (e) {
    view.replaceChildren(h('p', { class: 'loading' }, 'Impossible de charger les données : ' + e.message));
    return;
  }
  window.addEventListener('hashchange', route);
  route();
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js').catch((e) => console.warn('SW', e));
  }
}
main();
