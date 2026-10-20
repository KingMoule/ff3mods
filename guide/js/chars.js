// Characters.
import { h } from './util.js';
import { D, idx, itemName, atkName, locName } from './state.js';

const SWD_MOD = {
  Dispatch: 'ignores defense, single target', Retort: 'counter, ignores defense', Slash: '+ Sap, works on bosses',
  'Quadra Slam': '4 hits, random targets', Empowerer: 'HP drain then x0.25 as MP drain', Stunner: 'all + Stop (140/256)',
  'Quadra Slice': '4 hits, ignores defense', Cleave: 'all + Death (182/256)',
};

export function srcShort(it) {
  const s = it.src || {};
  if (s.chest && s.chest.length) { const c = s.chest[0]; return 'chest: ' + (c.loc ? locName(c.loc) : 'map ' + c.map) + ' (' + c.x + ',' + c.y + ')'; }
  if (s.shop && s.shop.length) return 'shop: ' + s.shop[0].replace(/_/g, ' ').toLowerCase();
  if (s.steal && s.steal.length) { const m = idx.mon[s.steal[0].m]; return 'steal: ' + (m ? m.name : '?'); }
  if (s.drop && s.drop.length) { const m = idx.mon[s.drop[0].m]; return 'drop: ' + (m ? m.name : '?'); }
  if (s.colo && s.colo.length) return 'Colosseum';
  if (s.metamon && s.metamon.length) { const m = idx.mon[s.metamon[0]]; return 'Metamorph: ' + (m ? m.name : '?'); }
  return 'event / other';
}

export function charList() {
  const ul = h('ul', { class: 'list card' });
  D.chars.filter((c) => c.id < 14).forEach((c) => {
    ul.append(h('li', null, h('a', { class: 'row chev', href: '#/chars/' + c.name },
      h('div', { class: 'grow' }, h('div', null, c.name), h('div', { class: 'sm' }, c.role || c.cmds.join(', '))))));
  });
  return h('div', null, ul, h('p', { class: 'muted' }, 'Starting stats and equipment read from the ROM (at the starting level). Equipment advice: hand-written, unverified.'));
}

function gearTable(c, type, label, n) {
  const list = D.items.filter((i) => i.type === type && i.equip && i.equip.includes(c.name))
    .sort((a, b) => (b.power || 0) - (a.power || 0)).slice(0, n);
  if (!list.length) return null;
  return h('details', null, h('summary', null, label + ' (best ' + list.length + ')'),
    h('div', { class: 'scroll' }, h('table', null,
      h('thead', null, h('tr', null, h('th', null, 'Name'), h('th', { class: 'num' }, type === 'weapon' ? 'BP' : 'Def'), h('th', null, 'Where'))),
      h('tbody', null, list.map((i) => h('tr', null,
        h('td', null, h('a', { href: '#/more/items/' + i.id }, i.name)), h('td', { class: 'num' }, i.power), h('td', null, srcShort(i))))))));
}

export function charDetail(name) {
  const c = D.chars.find((x) => x.name === name);
  if (!c) return { title: 'Character', node: h('p', null, 'Not found.') };
  const root = h('div');
  root.append(h('p', null, c.role || ''));
  root.append(h('div', { class: 'kv' },
    [['HP', c.hp], ['MP', c.mp], ['Vigor', c.str], ['Speed', c.agi], ['Stamina', c.sta], ['Magic', c.mag], ['Atk', c.atk], ['Def', c.def], ['MDef', c.mdef], ['Evade', c.evade + '%'], ['M.Block', c.mblock + '%'], ['Run', c.run]]
      .map(([k, v]) => h('div', null, h('b', null, v), h('span', null, k)))));
  root.append(h('p', { class: 'muted' }, 'Commands: ' + c.cmds.join(', ') + ' · starting level ' + c.levelmod + ' vs. party average'));
  const e = c.equip;
  root.append(h('p', { class: 'muted' }, 'Starting equipment: ' + ['weapon', 'shield', 'helmet', 'armor', 'relic1', 'relic2']
    .map((k) => (e[k] === null || e[k] === 255 ? null : itemName(e[k]))).filter(Boolean).join(', ')));
  if (c.tips) root.append(h('ul', null, c.tips.map((t) => h('li', null, t))));

  // techniques
  const NM = D.misc.natural_magic;
  if (NM[c.name]) {
    root.append(h('h3', null, 'Natural magic'), h('table', null, h('thead', null, h('tr', null, h('th', null, 'Spell'), h('th', { class: 'num' }, 'Level'))),
      h('tbody', null, NM[c.name].map((s) => h('tr', null, h('td', null, s.spell), h('td', { class: 'num' }, s.level))))));
  }
  if (c.name === 'Cyan') {
    root.append(h('h3', null, 'SwdTech (mod version)'), h('div', { class: 'scroll' }, h('table', null,
      h('thead', null, h('tr', null, h('th', null, 'Technique'), h('th', { class: 'num' }, 'Lv'), h('th', { class: 'num' }, 'x Fight'), h('th', null, 'Effect'))),
      h('tbody', null, D.misc.swdtech.map((s) => {
        const a = idx.atk[s.id];
        return h('tr', null, h('td', null, s.name), h('td', { class: 'num' }, s.level), h('td', { class: 'num' }, a ? (a.power / 8).toString() : '?'), h('td', null, SWD_MOD[s.name] || ''));
      })))));
    root.append(h('p', { class: 'muted' }, 'The gauge fills 2x faster. Multiplier = spell power / 8, read from the modded ROM.'));
  }
  if (c.name === 'Sabin') {
    root.append(h('h3', null, 'Blitz'), h('div', { class: 'scroll' }, h('table', null,
      h('thead', null, h('tr', null, h('th', null, 'Blitz'), h('th', { class: 'num' }, 'Lv'), h('th', { class: 'num' }, 'Power'), h('th', null, 'Target'))),
      h('tbody', null, D.misc.blitz.map((s) => {
        const a = idx.atk[s.id];
        return h('tr', null, h('td', null, s.name), h('td', { class: 'num' }, s.level), h('td', { class: 'num' }, a ? a.power : '?'), h('td', null, a ? a.target : ''));
      })))));
    root.append(h('p', { class: 'muted' }, 'Mod: the Blitz command opens a list; pick the Blitz then the target.'));
  }
  if (c.name === 'Mog') {
    root.append(h('h3', null, 'Dances'), h('table', null, h('tbody', null, D.misc.dances.map((d) => h('tr', null, h('th', null, d.name), h('td', null, d.moves.join(', ')))))));
    root.append(h('p', { class: 'muted' }, 'The dance learned depends on the battle terrain.'));
  }
  if (c.name === 'Strago') root.append(h('h3', null, 'Lores'), h('p', null, h('a', { href: '#/more/lores' }, '→ List of the 24 Lores and who casts them')));
  if (c.name === 'Edgar') {
    const tools = D.items.filter((i) => i.type === 'tool');
    root.append(h('h3', null, 'Tools'), h('ul', null, tools.map((i) => h('li', null, h('a', { href: '#/more/items/' + i.id }, i.name), ' — ' + (i.desc || '').replace(/\n/g, ' ') + ' · ' + srcShort(i)))));
  }
  if (c.name === 'Locke') root.append(h('h3', null, 'Steal'), h('p', null, 'Success = Locke level + 50 − target level (%), x2 with the Sneak Ring. Rare: 1/4 (mod).'));
  if (c.name === 'Gau') root.append(h('h3', null, 'Rage'), h('p', null, 'See the Bestiary: each page gives the Rage attack.'));
  if (c.gear) root.append(h('h3', null, 'Which gear when?'), h('ul', null, c.gear.map(([w, t]) => h('li', null, h('b', null, w + ' : '), t))));
  root.append(h('h3', null, 'Best equipment (ROM)'));
  [['weapon', 'Weapons', 6], ['armor', 'Armor', 5], ['helmet', 'Helmets', 5], ['shield', 'Shields', 5]].forEach(([t, l, n]) => {
    const g = gearTable(c, t, l, n); if (g) root.append(g);
  });
  return { title: c.name, back: '#/chars', node: root };
}
