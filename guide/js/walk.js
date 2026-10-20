// Walkthrough + checklist.
import { h, store, pct } from './util.js';
import { D, idx, itemName, itemLink, monLink, isChecked, setChecked, locName } from './state.js';

const checkable = (r) => r.k !== 'note';
const isLost = (r) => checkable(r) && !!r.lost;
const KIND = { chest: 'Coffre', item: 'Objet', esper: 'Esper', char: 'Perso', boss: 'Boss', learn: 'Appris', shop: 'Boutique', note: 'Note' };

let counters = [];
function track(el, ids) { counters.push({ el, ids }); refresh(); return el; }
function refresh() {
  for (const c of counters) {
    const done = c.ids.filter(isChecked).length;
    if (c.kind === 'lost') {
      const left = c.ids.length - done;
      c.el.textContent = left ? left + ' à faire' : 'tout est pris';
      if (c.wrap) c.wrap.classList.toggle('clear', !left);
      continue;
    }
    c.el.textContent = done + ' / ' + c.ids.length;
    if (c.bar) c.bar.style.width = pct(done, c.ids.length) + '%';
  }
  document.querySelectorAll('[data-lostref]').forEach((b) => b.classList.toggle('done', isChecked(b.dataset.lostref)));
}
function trackBar(txt, bar, ids) { const c = { el: txt, bar, ids }; counters.push(c); refresh(); }

function chapterRows(chap) {
  const out = [];
  chap.locs.forEach((l) => l.items.forEach((r) => { if (checkable(r)) out.push(r); }));
  return out;
}
const lostRows = (chap) => chapterRows(chap).filter(isLost);
const allRows = () => D.walkthrough.chapters.flatMap(chapterRows);

export function worldLabel(w) { return w === 'B' ? 'Monde de la Balance' : w === 'R' ? 'Monde de la Ruine' : 'Suivis'; }

function vText(v) {
  if (v.kind === 'item') return itemName(v.item);
  if (v.kind === 'gil') return v.gil.toLocaleString('fr-FR') + ' gil';
  if (v.kind === 'monster') return 'Monstre : ' + v.mon.map((m) => (idx.mon[m] ? idx.mon[m].name : m)).join(', ');
  return 'Coffre vide / déclencheur';
}
const vSig = (v) => v.kind + ':' + (v.item ?? v.gil ?? (v.mon || []).join('.'));

export function rowText(r) {
  if (r.k === 'chest') return r.v.map(vText).join(' ') + ' ' + r.x + ',' + r.y;
  return r.t;
}

function rowEl(r) {
  const id = r.id;
  const cb = h('input', { type: 'checkbox', 'aria-label': 'Fait' });
  cb.checked = isChecked(id);
  const lab = h('label', { class: 'chk' + (cb.checked ? ' done' : '') });
  cb.addEventListener('change', () => {
    setChecked(id, cb.checked);
    lab.classList.toggle('done', cb.checked);
    refresh();
    if (document.body.dataset.todo === '1' && cb.checked) lab.style.display = 'none';
  });
  const txt = h('div', { class: 'txt' });
  if (r.lost) { lab.classList.add('lost'); lab.dataset.rowid = id; txt.append(h('span', { class: 'tag lost' }, 'PERDU À JAMAIS'), ' '); }
  if (r.k === 'chest') {
    const same = r.v.every((v) => vSig(v) === vSig(r.v[0]));
    txt.append(h('span', { class: 'kind' }, 'Coffre'), h('b', null, vText(r.v[0])),
      h('span', { class: 'meta' }, '  (' + r.x + ', ' + r.y + ') carte ' + r.v[0].map));
    if (r.v[0].kind === 'item') txt.append(' ', h('a', { href: '#/more/items/' + r.v[0].item, class: 'tag' }, 'fiche'));
    if (r.v[0].kind === 'monster') r.v[0].mon.forEach((m) => idx.mon[m] && txt.append(' ', monLink(m)));
    if (!same) {
      txt.append(h('div', { class: 'var' }, 'Le contenu change selon l\'avancement (même coffre, un seul tirage) : ',
        r.v.map((v, i) => [i ? ' / ' : '', vText(v) + ' [' + (v.loc ? locName(v.loc) + ', ' : '') + 'carte ' + v.map + ']'])));
      txt.append(h('span', { class: 'tag warn' }, 'variable'));
    }
  } else {
    txt.append(h('span', { class: 'kind k-' + r.k }, KIND[r.k] || r.k), r.t);
    if (r.m && !r.lost) txt.append(h('span', { class: 'tag warn' }, 'manquable'));
    if (r.g) txt.append(h('span', { class: 'tag', title: 'Déduit, non vérifié (ni ROM, ni guide)' }, '≈'));
    if (r.c) txt.append(h('span', { class: 'tag ok', title: 'Confirmé par un guide externe (Caves of Narshe)' }, 'guide'));
    if (r.rom === true) txt.append(h('span', { class: 'tag ok', title: 'Cet objet/esper est bien donné par un script de la ROM' }, 'ROM'));
    if (r.item && idx.item) {
      const it = D.items.find((x) => x.name.toLowerCase() === r.item.toLowerCase());
      if (it) txt.append(' ', h('a', { class: 'tag', href: '#/more/items/' + it.id }, 'fiche'));
    }
    if (r.mon) { txt.append(h('div', null, r.mon.map((m) => idx.mon[m] ? [monLink(m), ' '] : null))); }
  }
  if (r.m && r.k === 'chest' && !r.lost) txt.append(h('span', { class: 'tag warn' }, 'manquable'));
  if (r.hint) txt.append(h('div', { class: 'meta' }, '→ ' + r.hint));
  if (r.lost) txt.append(h('div', { class: 'lostwhy' }, '⚠ ' + r.lost));
  if (r.last) txt.append(h('span', { class: 'tag warn' }, 'dernière chance'));
  lab.append(cb, txt);
  if (store.get('fMiss', false) && !r.m) lab.style.display = 'none';
  if (store.get('fLost', false) && !r.lost) lab.style.display = 'none';
  if (store.get('fTodo', false) && cb.checked) lab.style.display = 'none';
  return lab;
}

function filterBar(rerender) {
  const mk = (key, label) => {
    const b = h('button', { class: 'chip' + (store.get(key, false) ? ' on' : ''), type: 'button' }, label);
    b.addEventListener('click', () => { store.set(key, !store.get(key, false)); rerender(); });
    return b;
  };
  return h('div', { class: 'chips' }, mk('fTodo', 'Non cochés'), mk('fMiss', 'Manquables seulement'), mk('fLost', 'Perdu à jamais'));
}

export function walkHome(rerender) {
  counters = [];
  const root = h('div');
  const rows = allRows();
  const head = h('div', { class: 'card' });
  const t = h('b'); const bar = h('i');
  head.append(h('div', null, 'Progression globale : ', t), h('div', { class: 'bar' }, bar));
  trackBar(t, bar, rows.map((r) => r.id));
  const allLost = rows.filter(isLost);
  const lw = h('div', { class: 'lostbox' });
  const lc = h('b');
  lw.append(h('div', null, h('span', { class: 'tag lost' }, 'PERDU À JAMAIS'), ' Objets et événements à prendre au bon moment : ', lc),
    h('div', { class: 'sm' }, "Chaque chapitre indique en rouge ce qu'on ne peut plus récupérer ensuite. Le filtre « Perdu à jamais » n'affiche que cela."));
  counters.push({ kind: 'lost', el: lc, wrap: lw, ids: allLost.map((r) => r.id) });
  root.append(head, lw, filterBar(rerender));
  const search = h('input', { type: 'search', placeholder: 'Chercher un objet, un lieu, un boss…', 'aria-label': 'Recherche' });
  const res = h('div');
  search.addEventListener('input', () => {
    res.innerHTML = '';
    const q = search.value.trim().toLowerCase();
    if (q.length < 2) return;
    let n = 0;
    const card = h('div', { class: 'card' });
    for (const c of D.walkthrough.chapters) {
      for (const l of c.locs) {
        for (const r of l.items) {
          if (n >= 40) break;
          if ((rowText(r) + ' ' + l.name).toLowerCase().includes(q)) {
            n++;
            card.append(h('div', { class: 'muted' }, h('a', { href: '#/walk/' + c.id }, c.title), ' › ' + l.name), rowEl(r));
          }
        }
      }
    }
    res.append(n ? card : h('p', { class: 'muted' }, 'Aucun résultat.'));
  });
  root.append(search, res);
  for (const w of ['B', 'R', 'T']) {
    root.append(h('h2', null, worldLabel(w)));
    const ul = h('ul', { class: 'list card' });
    D.walkthrough.chapters.filter((c) => c.world === w).forEach((c) => {
      const ids = chapterRows(c).map((r) => r.id);
      const cnt = h('span', { class: 'sm' }); const b = h('i');
      const lr = lostRows(c);
      const lb = h('span', { class: 'lostbadge' });
      const lwrap = h('span', { class: 'lostwrap' }, '⚠ perdu à jamais : ', lb);
      if (lr.length) counters.push({ kind: 'lost', el: lb, wrap: lwrap, ids: lr.map((r) => r.id) });
      const li = h('li', null, h('a', { class: 'row chev', href: '#/walk/' + c.id },
        h('div', { class: 'grow' }, h('div', null, c.title), h('div', { class: 'sm' }, cnt, lr.length ? [' · ', lwrap] : null), h('div', { class: 'bar' }, b))));
      trackBar(cnt, b, ids);
      ul.append(li);
    });
    root.append(ul);
  }
  root.append(h('p', { class: 'muted' }, '« ≈ » = déduit, non vérifié. « guide » = recoupé avec un walkthrough externe. « ROM » = l\'objet/esper figure bien dans un script d\'événement. '
    + 'Les coffres (position, contenu) viennent directement de la ROM.'));
  return root;
}

export function walkChapter(id, rerender) {
  counters = [];
  document.body.dataset.todo = store.get('fTodo', false) ? '1' : '0';
  const chap = idx.chap[id];
  if (!chap) return h('p', null, 'Chapitre introuvable.');
  const root = h('div');
  const ids = chapterRows(chap).map((r) => r.id);
  const t = h('b'); const bar = h('i');
  root.append(h('div', { class: 'card' }, h('div', { class: 'muted' }, worldLabel(chap.world)), h('p', null, chap.intro),
    h('div', null, 'Progression : ', t), h('div', { class: 'bar' }, bar)), filterBar(rerender));
  trackBar(t, bar, ids);
  const lr = lostRows(chap);
  if (lr.length) {
    const box = h('div', { class: 'lostbox' });
    const left = h('b');
    box.append(h('div', null, h('span', { class: 'tag lost' }, 'PERDU À JAMAIS'), ' À récupérer dans ce chapitre : ', left),
      h('div', { class: 'sm' }, 'Après ce chapitre, ces éléments ne sont plus accessibles. Touchez une ligne pour y aller.'));
    const ul = h('ul', { class: 'lostlist' });
    lr.forEach((r) => {
      const loc = chap.locs.find((l) => l.items.includes(r));
      const label = r.k === 'chest' ? (vText(r.v[0]) + (r.v.length > 1 ? ' (variable)' : '')) : r.t.split(/[:.]/)[0];
      const b = h('button', { type: 'button', class: 'lostitem', 'data-lostref': r.id }, label, h('span', { class: 'sm' }, ' — ' + (loc ? loc.name : '')));
      b.addEventListener('click', () => {
        const el = document.querySelector('[data-rowid="' + r.id + '"]');
        if (el) { el.style.display = ''; el.scrollIntoView({ behavior: 'smooth', block: 'center' }); el.classList.add('flash'); setTimeout(() => el.classList.remove('flash'), 1500); }
      });
      ul.append(h('li', null, b));
    });
    box.append(ul);
    counters.push({ kind: 'lost', el: left, wrap: box, ids: lr.map((r) => r.id) });
    root.append(box);
  }
  chap.locs.forEach((l) => {
    const sec = h('section', { class: 'card' });
    const cnt = h('span', { class: 'sm' });
    sec.append(h('h3', null, l.name, ' ', cnt));
    [...new Set(l.items.filter((r) => r.k === 'chest' && (r.lost || r.last)).map((r) => r.lost || r.last))]
      .forEach((t2) => sec.append(h('div', { class: 'lostbanner' }, '⚠ Dernière chance : ' + t2)));
    trackBar(cnt, h('i'), l.items.filter(checkable).map((r) => r.id));
    const rows = l.items;
    if (!rows.length && !l.boss_chips.length) sec.append(h('p', { class: 'muted' }, 'Rien de spécial à récupérer ici.'));
    rows.forEach((r) => {
      if (r.k === 'note') sec.append(h('div', { class: 'note' }, r.t, r.g ? h('span', { class: 'tag' }, '≈') : null));
      else sec.append(rowEl(r));
    });
    if (l.boss_chips.length) sec.append(h('div', null, h('span', { class: 'kind k-boss' }, 'Boss'), l.boss_chips.map((m) => [monLink(m), ' '])));
    if (l.mon.length) {
      sec.append(h('details', null, h('summary', null, 'Monstres rencontrés (' + l.mon.length + ')'), h('div', { class: 'chips' }, l.mon.map((m) => monLink(m)))));
    }
    root.append(sec);
  });
  return root;
}
