// Walkthrough + checklist.
import { h, store, pct } from './util.js';
import { D, idx, itemName, itemLink, monLink, isChecked, setChecked, locName } from './state.js';

const checkable = (r) => r.k !== 'note';
const isLost = (r) => checkable(r) && !!r.lost;
const KIND = { chest: 'Chest', item: 'Item', esper: 'Esper', char: 'Party', boss: 'Boss', learn: 'Learn', shop: 'Shop', note: 'Note' };

let counters = [];
function track(el, ids) { counters.push({ el, ids }); refresh(); return el; }
function refresh() {
  for (const c of counters) {
    const done = c.ids.filter(isChecked).length;
    if (c.kind === 'lost') {
      const left = c.ids.length - done;
      c.el.textContent = left ? left + ' to do' : 'all taken';
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

export function worldLabel(w) { return w === 'B' ? 'World of Balance' : w === 'R' ? 'World of Ruin' : 'Trackers'; }

function vText(v) {
  if (v.kind === 'item') return itemName(v.item);
  if (v.kind === 'gil') return v.gil.toLocaleString('en-US') + ' gil';
  if (v.kind === 'monster') return 'Monster: ' + v.mon.map((m) => (idx.mon[m] ? idx.mon[m].name : m)).join(', ');
  return 'Empty chest / trigger';
}
const vSig = (v) => v.kind + ':' + (v.item ?? v.gil ?? (v.mon || []).join('.'));

export function rowText(r) {
  if (r.k === 'chest') return r.v.map(vText).join(' ') + ' ' + r.x + ',' + r.y;
  return r.t;
}

function rowEl(r) {
  const id = r.id;
  const cb = h('input', { type: 'checkbox', 'aria-label': 'Done' });
  cb.checked = isChecked(id);
  const lab = h('label', { class: 'chk' + (cb.checked ? ' done' : '') });
  cb.addEventListener('change', () => {
    setChecked(id, cb.checked);
    lab.classList.toggle('done', cb.checked);
    refresh();
    if (document.body.dataset.todo === '1' && cb.checked) lab.style.display = 'none';
  });
  const txt = h('div', { class: 'txt' });
  if (r.lost) { lab.classList.add('lost'); lab.dataset.rowid = id; txt.append(h('span', { class: 'tag lost' }, 'LOST FOR GOOD'), ' '); }
  if (r.k === 'chest') {
    const same = r.v.every((v) => vSig(v) === vSig(r.v[0]));
    txt.append(h('span', { class: 'kind' }, 'Chest'), h('b', null, vText(r.v[0])),
      h('span', { class: 'meta' }, '  (' + r.x + ', ' + r.y + ') map ' + r.v[0].map));
    if (r.v[0].kind === 'item') txt.append(' ', h('a', { href: '#/more/items/' + r.v[0].item, class: 'tag' }, 'info'));
    if (r.v[0].kind === 'monster') r.v[0].mon.forEach((m) => idx.mon[m] && txt.append(' ', monLink(m)));
    if (!same) {
      txt.append(h('div', { class: 'var' }, 'The contents change with progress (same chest, one roll only): ',
        r.v.map((v, i) => [i ? ' / ' : '', vText(v) + ' [' + (v.loc ? locName(v.loc) + ', ' : '') + 'map ' + v.map + ']'])));
      txt.append(h('span', { class: 'tag warn' }, 'variable'));
    }
  } else {
    txt.append(h('span', { class: 'kind k-' + r.k }, KIND[r.k] || r.k), r.t);
    if (r.m && !r.lost) txt.append(h('span', { class: 'tag warn' }, 'missable'));
    if (r.g) txt.append(h('span', { class: 'tag', title: 'Inferred, unverified (neither ROM nor guide)' }, '≈'));
    if (r.c) txt.append(h('span', { class: 'tag ok', title: 'Confirmed by an external guide (Caves of Narshe)' }, 'guide'));
    if (r.rom === true) txt.append(h('span', { class: 'tag ok', title: 'This item/Esper is indeed given by a ROM script' }, 'ROM'));
    if (r.item && idx.item) {
      const it = D.items.find((x) => x.name.toLowerCase() === r.item.toLowerCase());
      if (it) txt.append(' ', h('a', { class: 'tag', href: '#/more/items/' + it.id }, 'info'));
    }
    if (r.mon) { txt.append(h('div', null, r.mon.map((m) => idx.mon[m] ? [monLink(m), ' '] : null))); }
  }
  if (r.m && r.k === 'chest' && !r.lost) txt.append(h('span', { class: 'tag warn' }, 'missable'));
  if (r.hint) txt.append(h('div', { class: 'meta' }, '→ ' + r.hint));
  if (r.lost) txt.append(h('div', { class: 'lostwhy' }, '⚠ ' + r.lost));
  if (r.last) txt.append(h('span', { class: 'tag warn' }, 'last chance'));
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
  return h('div', { class: 'chips hs' }, mk('fTodo', 'Unchecked'), mk('fMiss', 'Missable only'), mk('fLost', 'Lost for good'));
}

const chapNum = (c) => {
  if (c.id === 't_esper') return 'Espers';
  if (c.id === 't_char') return 'Party';
  if (c.id === 't_lore') return 'Lores';
  return (c.world === 'R' ? 'R' : '') + c.id.replace(/^\D+/, '');
};

function chapStrip(cur) {
  const strip = h('div', { class: 'chapstrip', role: 'navigation', 'aria-label': 'Chapters' });
  let prevW = null;
  D.walkthrough.chapters.forEach((c) => {
    const ids = chapterRows(c).map((r) => r.id);
    const fin = ids.length && ids.every(isChecked);
    const a = h('a', { href: '#/walk/' + c.id, title: c.title, class: (c.id === cur ? 'on ' : '') + (fin ? 'fin ' : '') + (prevW && prevW !== c.world ? 'sep' : '') }, chapNum(c));
    prevW = c.world;
    strip.append(a);
  });
  requestAnimationFrame(() => { const on = strip.querySelector('.on'); if (on) strip.scrollLeft = on.offsetLeft - strip.clientWidth / 2 + on.offsetWidth / 2; });
  return h('div', { class: 'sticky' }, strip);
}

export function walkHome(rerender) {
  counters = [];
  const root = h('div');
  const rows = allRows();
  const head = h('div', { class: 'card' });
  const t = h('b'); const bar = h('i');
  head.append(h('div', { class: 'hrow' }, h('span', null, 'Overall progress'), t), h('div', { class: 'bar' }, bar));
  trackBar(t, bar, rows.map((r) => r.id));
  const allLost = rows.filter(isLost);
  const lw = h('div', { class: 'lostbox' });
  const lc = h('b');
  lw.append(h('div', null, h('span', { class: 'tag lost' }, 'LOST FOR GOOD'), ' Items and events to take at the right time: ', lc),
    h('div', { class: 'sm' }, 'Each chapter flags in red what can no longer be obtained afterwards. The "Lost for good" filter shows only those.'));
  counters.push({ kind: 'lost', el: lc, wrap: lw, ids: allLost.map((r) => r.id) });
  const last = store.get('lastChap', null);
  if (last && idx.chap[last]) root.append(h('a', { class: 'cont', href: '#/walk/' + last }, 'Continue: ' + idx.chap[last].title));
  root.append(head, lw, filterBar(rerender));
  const search = h('input', { type: 'search', placeholder: 'Search an item, a place, a boss…', 'aria-label': 'Search' });
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
    res.append(n ? card : h('p', { class: 'muted' }, 'No results.'));
  });
  root.append(search, res);
  for (const w of ['B', 'R', 'T']) {
    root.append(h('h2', null, worldLabel(w)));
    const g = h('div', { class: 'wgrid' });
    D.walkthrough.chapters.filter((c) => c.world === w).forEach((c) => {
      const ids = chapterRows(c).map((r) => r.id);
      const cnt = h('span', { class: 'sm' }); const b = h('i');
      const lr = lostRows(c);
      const lb = h('span', { class: 'lostbadge' });
      const lwrap = h('span', { class: 'lostwrap' }, '⚠ ', lb);
      if (lr.length) counters.push({ kind: 'lost', el: lb, wrap: lwrap, ids: lr.map((r) => r.id) });
      g.append(h('a', { href: '#/walk/' + c.id },
        h('div', { class: 'nm' }, h('b', null, chapNum(c) + '. '), c.title),
        h('div', { class: 'sm' }, cnt, lr.length ? [' · ', lwrap] : null), h('div', { class: 'bar' }, b)));
      trackBar(cnt, b, ids);
    });
    root.append(g);
  }
  root.append(h('p', { class: 'muted' }, '"≈" = inferred, unverified. "guide" = cross-checked with an external walkthrough. "ROM" = the item/Esper does appear in an event script. '
    + 'Chests (position, contents) are read directly from the ROM.'));
  return root;
}

export function walkChapter(id, rerender) {
  counters = [];
  document.body.dataset.todo = store.get('fTodo', false) ? '1' : '0';
  const chap = idx.chap[id];
  if (!chap) return h('p', null, 'Chapter not found.');
  store.set('lastChap', id);
  const root = h('div');
  root.append(chapStrip(id));
  const ids = chapterRows(chap).map((r) => r.id);
  const t = h('b'); const bar = h('i');
  root.append(h('div', { class: 'card' }, h('div', { class: 'hrow' }, h('span', { class: 'muted' }, worldLabel(chap.world)), t), h('p', null, chap.intro),
    h('div', { class: 'bar' }, bar)), filterBar(rerender));
  trackBar(t, bar, ids);
  const lr = lostRows(chap);
  if (lr.length) {
    const box = h('div', { class: 'lostbox' });
    const left = h('b');
    box.append(h('div', null, h('span', { class: 'tag lost' }, 'LOST FOR GOOD'), ' To collect in this chapter: ', left),
      h('div', { class: 'sm' }, 'After this chapter these can no longer be obtained. Tap a line to jump to it.'));
    const ul = h('ul', { class: 'lostlist' });
    lr.forEach((r) => {
      const loc = chap.locs.find((l) => l.items.includes(r));
      const label = r.k === 'chest' ? (vText(r.v[0]) + (r.v.length > 1 ? ' (variable)' : '')) : r.t.split(/[:.]/)[0];
      const b = h('button', { type: 'button', class: 'lostitem', 'data-lostref': r.id }, label, h('span', { class: 'sm' }, ' — ' + (loc ? loc.name : '')));
      b.addEventListener('click', () => {
        const el = document.querySelector('[data-rowid="' + r.id + '"]');
        if (el) { el.style.display = ''; const sc = el.closest('section'); if (sc) sc.classList.remove('collapsed'); el.scrollIntoView({ behavior: 'smooth', block: 'center' }); el.classList.add('flash'); setTimeout(() => el.classList.remove('flash'), 1500); }
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
    const hd = h('h3', null, l.name, ' ', cnt);
    hd.addEventListener('click', () => sec.classList.toggle('collapsed'));
    sec.append(hd);
    [...new Set(l.items.filter((r) => r.k === 'chest' && (r.lost || r.last)).map((r) => r.lost || r.last))]
      .forEach((t2) => sec.append(h('div', { class: 'lostbanner' }, '⚠ Last chance: ' + t2)));
    trackBar(cnt, h('i'), l.items.filter(checkable).map((r) => r.id));
    const rows = l.items;
    if (!rows.length && !l.boss_chips.length) sec.append(h('p', { class: 'muted' }, 'Nothing special to collect here.'));
    rows.forEach((r) => {
      if (r.k === 'note') sec.append(h('div', { class: 'note' }, r.t, r.g ? h('span', { class: 'tag' }, '≈') : null));
      else sec.append(rowEl(r));
    });
    if (l.boss_chips.length) sec.append(h('div', null, h('span', { class: 'kind k-boss' }, 'Boss'), l.boss_chips.map((m) => [monLink(m), ' '])));
    if (l.mon.length) {
      sec.append(h('details', null, h('summary', null, 'Monsters encountered (' + l.mon.length + ')'), h('div', { class: 'chips' }, l.mon.map((m) => monLink(m)))));
    }
    root.append(sec);
  });
  const all = D.walkthrough.chapters; const ci = all.findIndex((c) => c.id === id);
  const nav = (c, lab) => (c ? h('a', { href: '#/walk/' + c.id }, lab) : h('a', { class: 'off', href: '#/walk' }, '.'));
  root.append(h('div', { class: 'chapnav' }, nav(all[ci - 1], '‹ ' + (all[ci - 1] ? chapNum(all[ci - 1]) : '')), h('a', { href: '#/walk' }, 'All'), nav(all[ci + 1], (all[ci + 1] ? chapNum(all[ci + 1]) : '') + ' ›')));
  return root;
}
