// "More" section: espers, items, shops, Colosseum, Lores, encounter map, tables, mod, quests, settings.
import { h, store, nf } from './util.js';
import { D, idx, itemName, atkName, locName, monLink, elChip, resetChecks, getChecks, importChecks } from './state.js';
import { srcShort } from './chars.js';

const MENU = [
  ['espers', 'Espers', 'Taught spells, level bonuses, locations'],
  ['items', 'Items & equipment', 'Stats, sources (chests, shops, steals…)'],
  ['shops', 'Shops', 'Stock of each shop'],
  ['colosseum', 'Colosseum', 'Wagered item → opponent → prize'],
  ['lores', 'Lores (Strago)', '24 Lores and who casts them'],
  ['techs', 'SwdTech, Blitz, Dances', 'Levels and effects'],
  ['world', 'Encounter map', 'Monsters per world sector'],
  ['tables', 'HP / MP / EXP tables', 'Per level'],
  ['mods', 'Mod differences', 'What changes from the original game'],
  ['quests', 'Sidequests & tips', 'Missables, exclusive choices'],
  ['rare', 'Key items', 'The 20 rare items'],
  ['settings', 'Settings & save', 'Theme, export/import, clear'],
];

export function moreMenu() {
  // items/espers have their own bottom tabs; formulas lives here
  return h('div', { class: 'tiles' }, [['formulas', 'Formulas (mod)', 'Damage & hit formulas']].concat(MENU.filter(([k]) => k !== 'items' && k !== 'espers'))
    .map(([k, t, s]) => h('a', { href: k === 'formulas' ? '#/formulas' : '#/more/' + k }, h('b', null, t), h('span', null, s))));
}

const table = (head, rows) => h('div', { class: 'scroll' }, h('table', null, h('thead', null, h('tr', null, head.map((x) => h('th', null, x)))), h('tbody', null, rows)));

function espers() {
  const root = h('div');
  D.espers.forEach((e) => {
    const rows = e.spells.map((s) => h('tr', null, h('td', null, s.spell), h('td', { class: 'num' }, 'x' + s.rate)));
    root.append(h('details', null, h('summary', null, e.name + (e.bonus ? ' · ' + e.bonus : '')),
      h('div', null, h('p', null, 'Attack: ' + e.attack), table(['Taught spell', 'Rate (per MP)'], rows),
        e.bonus_desc ? h('p', { class: 'muted' }, 'Level bonus: ' + e.bonus_desc.replace(/\n/g, ' ')) : null,
        e.hint && e.hint.length ? h('p', { class: 'muted' }, 'Hint (ROM scripts): ' + e.hint.join(', ')) : null)));
  });
  root.append(h('p', { class: 'muted' }, 'Rate: learning progress multiplier (x1 = base; spells end at 100%). Locations are hints inferred from event scripts.'));
  return root;
}

const TYPES = { weapon: 'Weapons', armor: 'Armor', shield: 'Shields', helmet: 'Helmets', relic: 'Relics', tool: 'Tools', consumable: 'Consumables' };
let itemState = { q: '', t: null };
function items() {
  const root = h('div');
  const input = h('input', { type: 'search', placeholder: 'Item name…', value: itemState.q, 'aria-label': 'Search' });
  const chips = h('div', { class: 'chips hs' });
  const ul = h('ul', { class: 'list card' });
  function draw() {
    const sl = chips.scrollLeft;
    chips.innerHTML = '';
    Object.entries(TYPES).forEach(([k, l]) => {
      const b = h('button', { class: 'chip' + (itemState.t === k ? ' on' : ''), type: 'button' }, l);
      b.addEventListener('click', () => { itemState.t = itemState.t === k ? null : k; draw(); });
      chips.append(b);
    });
    chips.scrollLeft = sl;
    ul.innerHTML = '';
    const q = itemState.q.toLowerCase();
    D.items.filter((i) => i.name && (!itemState.t || i.type === itemState.t) && (!q || i.name.toLowerCase().includes(q))).forEach((i) => {
      ul.append(h('li', null, h('a', { class: 'row chev', href: '#/more/items/' + i.id },
        h('div', { class: 'grow' }, h('div', null, i.name), h('div', { class: 'sm' }, TYPES[i.type] + (i.power !== undefined && i.type !== 'relic' ? ' · ' + i.power : ''))))));
    });
  }
  input.addEventListener('input', () => { itemState.q = input.value; draw(); });
  root.append(h('div', { class: 'sticky' }, input, chips), ul);
  draw();
  return root;
}

function itemDetail(id) {
  const i = idx.item[id];
  if (!i) return { title: 'Item', node: h('p', null, 'Not found.') };
  const root = h('div');
  root.append(h('p', { class: 'muted' }, TYPES[i.type] + ' · prix ' + nf.format(i.price) + ' gil'));
  if (i.desc) root.append(h('p', null, i.desc.replace(/\n/g, ' ')));
  const rows = [];
  const add = (k, v) => { if (v !== undefined && v !== '' && !(Array.isArray(v) && !v.length)) rows.push(h('tr', null, h('th', null, k), h('td', null, Array.isArray(v) ? v.join(', ') : String(v)))); };
  if (i.equip) {
    add(i.type === 'weapon' ? 'BP' : 'Defense', i.power);
    add(i.type === 'weapon' ? 'Hit' : 'Magic def.', i.type === 'weapon' ? i.hit : i.mdef);
    add('Element', i.element); add('Absorbs', i.absorb); add('Nullifies', i.null); add('Weak to', i.weak);
    add('Effect', i.special); add('Traits', i.wflags);
    const b = i.bonus; add('Bonus', ['str', 'spd', 'sta', 'mag'].filter((k) => b[k]).map((k) => ({ str: 'Vigor', spd: 'Speed', sta: 'Stamina', mag: 'Magic' }[k] + ' ' + (b[k] > 0 ? '+' : '') + b[k])));
    add('Evade', i.evade ? i.evade + ' %' : ''); add('M.Block', i.mevade ? i.mevade + ' %' : '');
    add('Immunity', i.immune); add('Auto statuses', i.auto); add('Effects', i.fx); add('Terrain', i.field);
    if (i.teaches) add('Teaches', atkName(i.teaches.spell) + ' (x' + i.teaches.rate + ')');
    if (i.cast) add('Casts', atkName(i.cast.spell) + (i.cast.random ? ' (random)' : ''));
    add('Equippable by', i.equip.length === 14 ? 'everyone' : i.equip);
  } else if (i.type === 'tool') add('Sort', atkName(i.cast.spell));
  root.append(h('table', null, h('tbody', null, rows)));
  const s = i.src || {};
  root.append(h('h3', null, 'Where to get it'));
  const ul = h('ul');
  (s.chest || []).forEach((c) => ul.append(h('li', null, 'Chest: ' + (c.loc ? locName(c.loc) : 'map ' + c.map) + ' (' + c.x + ',' + c.y + ')')));
  (s.shop || []).forEach((n) => ul.append(h('li', null, 'Shop: ' + n.replace(/_/g, ' ').toLowerCase())));
  (s.steal || []).forEach((x) => ul.append(h('li', null, 'Steal (' + (x.rare ? 'rare' : 'common') + ') : ', monLink(x.m))));
  (s.drop || []).forEach((x) => ul.append(h('li', null, 'Drop (' + (x.rare ? 'rare' : 'common') + ') : ', monLink(x.m))));
  (s.colo || []).forEach((x) => ul.append(h('li', null, 'Colosseum: wager ' + itemName(x.bet) + ' against ', monLink(x.m))));
  (s.metamon || []).slice(0, 12).forEach((m) => ul.append(h('li', null, 'Metamorph on ', monLink(m))));
  root.append(ul.children.length ? ul : h('p', { class: 'muted' }, 'No chest/shop/steal source: event reward or other.'));
  return { title: i.name, back: '#/more/items', node: root };
}

function shops() {
  const root = h('div');
  D.misc.shops.filter((s) => s.items.length).forEach((s) => {
    root.append(h('details', null, h('summary', null, s.name.replace(/_/g, ' ').toLowerCase()),
      h('div', null, table(['Item', 'Price'], s.items.map((i) => h('tr', null, h('td', null, h('a', { href: '#/more/items/' + i }, itemName(i))), h('td', { class: 'num' }, nf.format(idx.item[i].price))))))));
  });
  root.append(h('p', { class: 'muted' }, 'The _1/_2/_3 suffixes are the successive states of the shop (Balance then Ruin). Sell price = half.'));
  return root;
}

function colosseum() {
  const rows = [];
  D.misc.colosseum.forEach((c) => {
    if (!idx.item[c.bet] || !idx.item[c.bet].name || c.monster === 255 || c.monster === 0 && c.prize === 0) return;
    const m = idx.mon[c.monster];
    if (!m) return;
    rows.push(h('tr', null, h('td', null, h('a', { href: '#/more/items/' + c.bet }, itemName(c.bet))), h('td', null, monLink(c.monster)),
      h('td', null, h('a', { href: '#/more/items/' + c.prize }, itemName(c.prize)), c.hidden ? h('span', { class: 'tag' }, 'hidden name') : null)));
  });
  return h('div', null, h('input', { type: 'search', placeholder: 'Filter…', 'aria-label': 'Filter', oninput: (e) => {
    const q = e.target.value.toLowerCase();
    rows.forEach((r) => { r.style.display = r.textContent.toLowerCase().includes(q) ? '' : 'none'; });
  } }), table(['Wager', 'Opponent', 'Prize'], rows), h('p', { class: 'muted' }, 'Read from the Colosseum table (ROM).'));
}

function lores() {
  const root = h('div');
  const start = new Set(D.misc.lore_start);
  root.append(h('p', { class: 'muted' }, D.content.lore_hint));
  D.misc.lores.forEach((l) => {
    const a = idx.atk[l.id];
    const srcs = (D.misc.lore_sources[String(l.id)] || []).map((id) => monLink(id));
    root.append(h('details', null, h('summary', null, l.name + (start.has(l.idx) ? ' · known at the start' : '')),
      h('div', null, a ? h('p', { class: 'muted' }, 'PM ' + a.mp + ' · puissance ' + a.power + ' · ' + a.target + (a.element.length ? ' · ' + a.element.join('/') : '')) : null,
        srcs.length ? h('div', { class: 'chips' }, srcs) : h('p', { class: 'muted' }, 'No monster casts it in the normal scripts.'))));
  });
  return root;
}

function techs() {
  const root = h('div');
  root.append(h('h3', null, 'SwdTech (Cyan, mod version)'),
    table(['Name', 'Lv', 'x Fight'], D.misc.swdtech.map((s) => h('tr', null, h('td', null, s.name), h('td', { class: 'num' }, s.level), h('td', { class: 'num' }, ((idx.atk[s.id].power) / 8).toString())))));
  root.append(h('h3', null, 'Blitz (Sabin)'),
    table(['Name', 'Lv', 'Power'], D.misc.blitz.map((s) => h('tr', null, h('td', null, s.name), h('td', { class: 'num' }, s.level), h('td', { class: 'num' }, idx.atk[s.id].power)))));
  root.append(h('h3', null, 'Dances (Mog)'), table(['Dance', 'Attacks'], D.misc.dances.map((d) => h('tr', null, h('td', null, d.name), h('td', null, d.moves.join(', '))))));
  return root;
}

let wSel = { w: 0, s: null };
function worldView(w, s) {
  if (w !== undefined) wSel = { w: +w, s: s !== undefined ? +s : null };
  const root = h('div');
  const W = D.world[String(wSel.w)];
  const tabs = h('div', { class: 'chips' }, [0, 1].map((k) => h('a', { class: 'chip' + (wSel.w === k ? ' on' : ''), href: '#/more/world/' + k }, k === 0 ? 'World of Balance' : 'World of Ruin')));
  const grid = h('div', { class: 'grid8' });
  for (let sec = 0; sec < 64; sec++) {
    const c = W[String(sec)];
    const b = h('a', { class: 'chip' + (wSel.s === sec ? ' on' : ''), href: '#/more/world/' + wSel.w + '/' + sec, style: 'padding:6px 0;text-align:center;border-radius:6px' }, String(sec));
    if (!c || !c.all.length) b.style.opacity = '.4';
    grid.append(b);
  }
  root.append(tabs, h('p', { class: 'muted' }, '8×8 map (column = sector % 8, row = sector ÷ 8, north at the top). Tap a sector.'), grid);
  if (wSel.s !== null) {
    const c = W[String(wSel.s)];
    root.append(h('h3', null, 'Sector ' + wSel.s + ' (column ' + (wSel.s % 8 + 1) + ', row ' + (Math.floor(wSel.s / 8) + 1) + ')'));
    if (c && c.near) root.append(h('p', { class: 'muted' }, 'Nearest landmark: ' + locName(c.near)));
    const terrNames = ['Plains', 'Forest', 'Desert', 'Land (≈)'];
    if (!c || !c.all.length) root.append(h('p', null, 'No encounters.'));
    else c.terr.forEach((ms, ti) => { if (ms.length) root.append(h('h3', null, terrNames[ti]), h('div', { class: 'chips' }, ms.map((m) => monLink(m)))); });
  }
  return root;
}

function tables() {
  const rows = [];
  for (let lv = 2; lv <= 99; lv++) {
    const i = lv - 2;
    rows.push(h('tr', null, h('td', { class: 'num' }, lv), h('td', { class: 'num' }, nf.format(D.misc.exp_table[i])), h('td', { class: 'num' }, D.misc.hp_gain[i]), h('td', { class: 'num' }, D.misc.mp_gain[i])));
  }
  return h('div', null, table(['Lv', 'EXP to reach', 'HP gained', 'MP gained'], rows),
    h('p', { class: 'muted' }, 'Raw ROM tables (the EXP column is the EXP required for levels 2 to 99).'));
}

function mods() {
  const root = h('div');
  root.append(h('p', null, 'ff3mods mod for FF3 US v1.1 (headerless): bug fixes, minor balance changes and the Blitz menu. All data in this guide is read from the modded ROM.'));
  let g = null; let ul = null;
  D.content.mods.forEach((m) => {
    if (m.group !== g) { g = m.group; root.append(h('h2', null, g)); ul = h('ul', { class: 'list card' }); root.append(ul); }
    ul.append(h('li', null, h('div', { class: 'row' }, h('div', { class: 'grow' }, h('b', null, m.title), h('div', { class: 'sm' }, m.text)))));
  });
  root.append(h('h2', null, 'Modified data (ROM diff)'));
  if (!D.mod_diff.length) root.append(h('p', { class: 'muted' }, 'None (guide generated without a modded ROM).'));
  else root.append(table(['Table', 'Entry', 'Bytes (offset: before → after)'], D.mod_diff.map((d) => h('tr', null, h('td', null, d.kind), h('td', null, d.name + ' #' + d.id),
    h('td', null, d.bytes.map((b) => b[0] + ' : ' + b[1] + '→' + b[2]).join(' · '))))));
  return root;
}

function quests() {
  return h('div', null, D.content.sidequests.map((q) => h('div', { class: 'card' }, h('b', null, q.title), q.g ? h('span', { class: 'tag' }, '≈') : null, h('p', null, q.text))),
    h('p', { class: 'muted' }, '"≈": game knowledge, unverified in the ROM.'));
}

function rare() {
  return h('ul', { class: 'list card' }, D.misc.rare_items.map((n) => h('li', null, h('div', { class: 'row' }, n))));
}

function settings() {
  const root = h('div');
  const theme = store.get('theme', 'auto');
  const sel = h('select', null, ['auto', 'light', 'dark'].map((v) => h('option', { value: v, selected: v === theme }, { auto: 'Automatic', light: 'Light', dark: 'Dark' }[v])));
  sel.addEventListener('change', () => { store.set('theme', sel.value); applyTheme(); });
  root.append(h('h3', null, 'Theme'), sel);
  const area = h('textarea', { rows: 4, readonly: true });
  const exp = h('button', { class: 'btn', type: 'button' }, 'Export my progress');
  exp.addEventListener('click', () => { area.value = JSON.stringify(getChecks()); area.readOnly = false; area.select(); });
  const imp = h('button', { class: 'btn', type: 'button' }, 'Import (paste the text above)');
  imp.addEventListener('click', () => {
    try { const o = JSON.parse(area.value); if (o && typeof o === 'object') { importChecks(o); alert('Progress imported.'); } } catch (e) { alert('Invalid text.'); }
  });
  const rs = h('button', { class: 'btn danger', type: 'button' }, 'Clear all progress');
  rs.addEventListener('click', () => { if (confirm('Clear all checked boxes?')) { resetChecks(); alert('Progress cleared.'); } });
  root.append(h('h3', null, 'Progress'), area, h('div', { class: 'chips' }, exp, imp), rs);
  const st = h('p', { class: 'muted' }, 'Offline: checking…');
  root.append(h('h3', null, 'Offline'), st);
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistration().then((r) => {
      st.textContent = r && r.active ? 'Service worker active: the guide works without a network.' : 'Service worker is installing (reload the page).';
    }).catch(() => { st.textContent = 'Service worker unavailable.'; });
  } else st.textContent = 'This browser does not support service workers.';
  root.append(h('footer', { class: 'foot' }, 'Guide generated from the FF3 US v1.1 ROM + the ff3mods mod. No ROM is included.'));
  return root;
}

export function applyTheme() {
  const t = store.get('theme', 'auto');
  if (t === 'auto') document.documentElement.removeAttribute('data-theme');
  else document.documentElement.setAttribute('data-theme', t);
}

const TITLES = { espers: 'Espers', items: 'Items & equipment', shops: 'Shops', colosseum: 'Colosseum', lores: 'Lores', techs: 'Techniques', world: 'World encounters', tables: 'Tables', mods: 'Mod differences', quests: 'Quests & tips', rare: 'Key items', settings: 'Settings' };

export function moreView(parts) {
  const [sub, a, b] = parts;
  if (!sub) return { title: 'More', node: moreMenu() };
  if (sub === 'items' && a) return itemDetail(+a);
  const fn = { espers, items, shops, colosseum, lores, techs, tables, mods, quests, rare, settings }[sub];
  if (sub === 'world') return { title: TITLES.world, back: '#/more', node: worldView(a, b) };
  if (!fn) return { title: 'More', node: moreMenu() };
  // items and espers are bottom tabs: no back button
  return { title: TITLES[sub], back: sub === 'items' || sub === 'espers' ? null : '#/more', node: fn() };
}
