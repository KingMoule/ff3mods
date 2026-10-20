// Bestiary: filterable list + monster page.
import { h, store, nf } from './util.js';
import { D, idx, itemName, itemLink, atkName, locName, elChip } from './state.js';

const ELEMS = ['Fire', 'Ice', 'Bolt', 'Poison', 'Wind', 'Pearl', 'Earth', 'Water'];
let st = { q: '', weak: null, world: null, boss: false, sort: 'id' };

const isBoss = (m) => m.places.some((p) => p.t === 'boss');
function worldsOf(m) {
  const w = new Set();
  m.places.forEach((p) => {
    if (p.t === 'w') w.add(p.w === 0 ? 'B' : 'R');
    else if (p.c && idx.chap[p.c]) w.add(idx.chap[p.c].world);
  });
  return w;
}
function haystack(m) {
  if (m._h) return m._h;
  const parts = [m.name, m.special.name];
  [...m.steal, ...m.drop].forEach((i) => i !== null && parts.push(itemName(i)));
  [...m.attacks, m.rage, ...m.sketch, ...m.control].forEach((a) => a !== undefined && parts.push(atkName(a)));
  m._h = parts.join(' ').toLowerCase();
  return m._h;
}

export function bestiaryList() {
  const root = h('div');
  const input = h('input', { type: 'search', placeholder: 'Name, stolen/dropped item, attack…', value: st.q, 'aria-label': 'Search' });
  const out = h('ul', { class: 'list card' });
  const count = h('p', { class: 'muted' });
  const chips = h('div');
  function chip(label, on, fn, cls) {
    const b = h('button', { class: 'chip' + (on ? ' on' : '') + (cls ? ' ' + cls : ''), type: 'button' }, label);
    b.addEventListener('click', () => { fn(); drawChips(); draw(); });
    return b;
  }
  function drawChips() {
    // two horizontally scrolling rows: filters, then weaknesses
    const sl = [...chips.children].map((r) => r.scrollLeft);
    chips.innerHTML = '';
    const r1 = h('div', { class: 'chips hs' }); const r2 = h('div', { class: 'chips hs' });
    chips.append(r1, r2);
    r1.append(chip('Boss', st.boss, () => { st.boss = !st.boss; }));
    r1.append(chip('Balance', st.world === 'B', () => { st.world = st.world === 'B' ? null : 'B'; }));
    r1.append(chip('Ruin', st.world === 'R', () => { st.world = st.world === 'R' ? null : 'R'; }));
    r1.append(chip(st.sort === 'id' ? 'Sort: game order' : 'Sort: level', false, () => { st.sort = st.sort === 'id' ? 'lvl' : 'id'; }));
    r2.append(h('span', { class: 'muted' }, 'Weak to:'));
    ELEMS.forEach((e) => r2.append(chip(e, st.weak === e, () => { st.weak = st.weak === e ? null : e; }, 'el-' + e)));
    [r1, r2].forEach((r, i) => { r.scrollLeft = sl[i] || 0; });
  }
  function draw() {
    const q = st.q.trim().toLowerCase();
    let list = D.monsters.filter((m) => {
      if (q && !haystack(m).includes(q)) return false;
      if (st.weak && !m.weak.includes(st.weak)) return false;
      if (st.boss && !isBoss(m)) return false;
      if (st.world && !worldsOf(m).has(st.world)) return false;
      return true;
    });
    if (st.sort === 'lvl') list = list.slice().sort((a, b) => a.level - b.level || a.id - b.id);
    count.textContent = list.length + ' monster(s)';
    out.innerHTML = '';
    const frag = document.createDocumentFragment();
    list.forEach((m) => {
      frag.append(h('li', null, h('a', { class: 'row chev', href: '#/bestiary/' + m.id },
        h('div', { class: 'grow' }, h('div', null, m.name, isBoss(m) ? h('span', { class: 'tag warn' }, 'boss') : null),
          h('div', { class: 'sm' }, 'Lv ' + m.level + ' · HP ' + nf.format(m.hp) + (m.weak.length ? ' · weak: ' + m.weak.join(', ') : ''))))));
    });
    out.append(frag);
  }
  input.addEventListener('input', () => { st.q = input.value; draw(); });
  drawChips();
  root.append(h('div', { class: 'sticky' }, input, chips), count, out);
  draw();
  return root;
}

function kv(label, value) { return h('div', null, h('b', null, value), h('span', null, label)); }

function placeEl(p) {
  if (p.t === 'loc') return h('a', { class: 'chip', href: '#/walk/' + p.c }, locName(p.id));
  if (p.t === 'boss') return h('a', { class: 'chip', href: '#/walk/' + p.c }, 'Boss · ' + locName(p.id));
  if (p.t === 'chest') return h('span', { class: 'chip' }, 'Monster chest · ' + locName(p.id));
  return h('a', { class: 'chip', href: '#/more/world/' + p.w + '/' + p.s }, (p.w === 0 ? 'Balance' : 'Ruin') + ' · sector ' + p.s);
}

export function monsterDetail(id) {
  const m = idx.mon[id];
  if (!m) return { title: 'Monster', node: h('p', null, 'Not found.') };
  const root = h('div');
  root.append(h('div', { class: 'kv' }, kv('Level', m.level), kv('HP', nf.format(m.hp)), kv('MP', nf.format(m.mp)),
    kv('EXP', nf.format(m.exp)), kv('Gil', nf.format(m.gil)), kv('Speed', m.speed),
    kv('Atk', m.atk), kv('Hit', m.hit + ' %'), kv('Evade', m.evade + ' %'),
    kv('Def', m.def), kv('MDef', m.mdef), kv('M.Block', m.mblock + ' %'), kv('Mag', m.magpwr)));
  const sec = (title, node) => root.append(h('h3', null, title), node);
  const chipsOf = (arr, fn) => (arr.length ? h('div', { class: 'chips' }, arr.map(fn)) : h('p', { class: 'muted' }, 'None'));
  sec('Weaknesses', chipsOf(m.weak, elChip));
  if (m.null.length) sec('Elemental immunities', chipsOf(m.null, elChip));
  if (m.absorb.length) sec('Absorbs', chipsOf(m.absorb, elChip));
  if (m.immune.length) sec('Status immunities', chipsOf(m.immune, (s) => h('span', { class: 'chip' }, s)));
  if (m.start.length) sec('Starting statuses', chipsOf(m.start, (s) => h('span', { class: 'chip' }, s)));
  const traits = [...m.flags, ...m.mstatus, m.flying ? 'Flies (Float)' : null].filter(Boolean);
  if (traits.length) sec('Traits', chipsOf(traits, (s) => h('span', { class: 'chip' }, s)));
  root.append(h('h3', null, 'Items'));
  root.append(h('table', null, h('tbody', null,
    h('tr', null, h('th', null, 'Steal (rare / common)'), h('td', null, itemLink(m.steal[0]), ' / ', itemLink(m.steal[1]))),
    h('tr', null, h('th', null, 'Drop (rare 1/8 / common)'), h('td', null, itemLink(m.drop[0]), ' / ', itemLink(m.drop[1]))),
  )));
  root.append(h('p', { class: 'muted' }, 'Locke mod: the rare item is stolen 1 time in 4 (instead of 1/8) once the steal succeeds.'));
  sec('Attacks (AI script)', chipsOf(m.attacks, (a) => h('span', { class: 'chip' }, atkName(a) + (a === 0xEF && m.special.name ? ' : ' + m.special.name : ''))));
  if (m.counter.length) sec('Counterattacks', chipsOf(m.counter, (a) => h('span', { class: 'chip' }, atkName(a))));
  if (m.special.name) {
    root.append(h('p', null, h('b', null, 'Special attack: '), m.special.name,
      m.special.effect ? ' (' + m.special.effect + ')' : '', m.special.nomiss ? ' · never misses' : '', m.special.nodmg ? ' · no damage' : ''));
  }
  const rows = [];
  if (m.rage !== undefined) rows.push(['Rage (Gau)', atkName(m.rage) + (m.rage === 0xEF && m.special.name ? ' (' + m.special.name + ')' : '')]);
  rows.push(['Sketch (Relm)', m.sketch.map(atkName).join(' / ')]);
  rows.push(['Control', m.control.map(atkName).join(', ') || '—']);
  if (m.meta) {
    const g = D.misc.metamorph[m.meta.group];
    rows.push(['Metamorph', (g ? [...new Set(g)].map(itemName).join(', ') : '?') + ' — success ' + D.misc.metamorph_rates[m.meta.rate]]);
  }
  root.append(h('table', null, h('tbody', null, rows.map((r) => h('tr', null, h('th', null, r[0]), h('td', null, r[1]))))));
  root.append(h('h3', null, 'Where to find'));
  if (m.places.length) {
    const shown = m.places.slice(0, 14);
    root.append(h('div', { class: 'chips' }, shown.map(placeEl)));
    if (m.places.length > shown.length) {
      root.append(h('details', null, h('summary', null, '+ ' + (m.places.length - shown.length) + ' more places'),
        h('div', { class: 'chips' }, m.places.slice(14).map(placeEl))));
    }
  } else root.append(h('p', { class: 'muted' }, 'Event battle (not tied to a location in this guide).'));
  return { title: m.name, sub: '#' + m.id, back: '#/bestiary', node: root };
}
