// Shared state: loaded data, indexes, checked boxes.
import { h, store } from './util.js';

export const D = {};
export const idx = { mon: {}, item: {}, atk: {}, esper: {}, loc: {}, chap: {} };

export async function loadData() {
  const names = ['monsters', 'items', 'attacks', 'espers', 'chars', 'misc', 'walkthrough', 'world', 'content', 'mod_diff'];
  const res = await Promise.all(names.map((n) => fetch('data/' + n + '.json').then((r) => {
    if (!r.ok) throw new Error(n + ' : HTTP ' + r.status);
    return r.json();
  })));
  names.forEach((n, i) => { D[n] = res[i]; });
  D.monsters.forEach((m) => { idx.mon[m.id] = m; });
  D.items.forEach((m) => { idx.item[m.id] = m; });
  D.attacks.forEach((m) => { idx.atk[m.id] = m; });
  D.espers.forEach((m) => { idx.esper[m.name] = m; });
  idx.loc = D.walkthrough.locs;
  D.walkthrough.chapters.forEach((c) => { idx.chap[c.id] = c; });
}

export const itemName = (id) => (id === null || id === undefined ? '—' : (idx.item[id] && idx.item[id].name) || '#' + id);
export const atkName = (id) => {
  if (id === 0xEE) return 'Normal attack';
  if (id === 0xEF) return 'Special attack';
  const a = idx.atk[id];
  return (a && a.name) || '#' + id;
};
export const locName = (id) => (idx.loc[id] ? idx.loc[id].name : id);

// ---- checked boxes (persisted)
let checks = store.get('checks', {});
export const isChecked = (id) => !!checks[id];
export function setChecked(id, on) {
  if (on) checks[id] = 1; else delete checks[id];
  store.set('checks', checks);
}
export function resetChecks() { checks = {}; store.set('checks', checks); }
export const getChecks = () => checks;
export function importChecks(obj) { checks = obj; store.set('checks', checks); }

// ---- links
export const monLink = (id, label) => h('a', { class: 'chip', href: '#/bestiary/' + id }, label || (idx.mon[id] ? idx.mon[id].name : '#' + id));
export const itemLink = (id, label) => (id === null || id === undefined ? '—' : h('a', { href: '#/more/items/' + id }, label || itemName(id)));

export function elChip(name) { return h('span', { class: 'chip el-' + name }, name); }
