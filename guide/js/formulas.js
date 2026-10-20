// Formulas (modded version) + small calculators.
import { h } from './util.js';
import { D } from './state.js';

function block(b) {
  if (b.t === 'p') return h('p', null, b.x);
  if (b.t === 'f') return h('div', { class: 'f' }, b.x);
  if (b.t === 'ul') return h('ul', null, b.x.map((x) => h('li', null, x)));
  if (b.t === 'note') return h('div', { class: 'note' }, b.x);
  if (b.t === 'mod') return h('div', { class: 'mod' }, b.x);
  return h('p');
}

function num(label, val, step) {
  const i = h('input', { type: 'number', value: val, inputmode: 'numeric', step: step || 1 });
  return { i, el: h('label', { class: 'muted' }, label, i) };
}

function calc() {
  const wrap = h('div');
  // physique
  const p = { lvl: num('Level', 30), bp: num('Weapon BP', 60), vig: num('Vigor (displayed stat)', 40), def: num('Target Def', 100), mult: num('Multiplier (SwdTech: 1.25…)', 1, 0.05) };
  const pOut = h('div', { class: 'f' });
  const pf = () => {
    const L = +p.lvl.i.value, BP = +p.bp.i.value, V2 = Math.min(255, 2 * +p.vig.i.value), Df = +p.def.i.value, M = +p.mult.i.value || 1;
    const base = BP + 1.5 * Math.floor((L * L * (BP + V2)) / 256);
    const x2 = (d) => (255 - d) / 256;
    const lo = Math.min(9999, Math.floor(base * M * 224 / 256 * x2(Df) + 1));
    const hi = Math.min(9999, Math.floor(base * M * 255 / 256 * x2(Df) + 1));
    pOut.textContent = 'base = ' + Math.floor(base) + '  → after defense/variance: ' + lo + ' – ' + hi + '  (no element, excluding row/critical)';
  };
  Object.values(p).forEach((o) => o.i.addEventListener('input', pf));
  pf();
  wrap.append(h('details', null, h('summary', null, 'Calculator: a character\'s physical attack'),
    h('div', null, ...Object.values(p).map((o) => o.el), pOut)));
  // magique
  const m = { lvl: num('Level', 30), mag: num('Magic Power', 40), pw: num('Spell power', 25), md: num('Target MDef', 140) };
  const mOut = h('div', { class: 'f' });
  const mf = () => {
    const L = +m.lvl.i.value, MG = +m.mag.i.value, PW = +m.pw.i.value, MD = +m.md.i.value;
    const base = 4 * PW + Math.floor((L * MG * PW) / 32);
    const lo = Math.min(9999, Math.floor(base * 224 / 256 * (255 - MD) / 256 + 1));
    const hi = Math.min(9999, Math.floor(base * 255 / 256 * (255 - MD) / 256 + 1));
    mOut.textContent = 'base = ' + base + '  → after MDef/variance: ' + lo + ' – ' + hi + '  (Earring / Shell / elements not included)';
  };
  Object.values(m).forEach((o) => o.i.addEventListener('input', mf));
  mf();
  wrap.append(h('details', null, h('summary', null, 'Calculator: offensive spell'), h('div', null, ...Object.values(m).map((o) => o.el), mOut)));
  // précision
  const a = { hit: num('Attack hit (%)', 100), ev: num('Target Evade (%)', 50), blind: num('Attacker Blind? (1 = yes)', 0) };
  const aOut = h('div', { class: 'f' });
  const af = () => {
    let hit = +a.hit.i.value; if (+a.blind.i.value) hit = Math.floor(hit / 2);
    const mulEv = Math.max(1, 256 - 2 * +a.ev.i.value);
    const chance = Math.min(100, Math.max(0, Math.floor((hit * mulEv) / 256)));
    aOut.textContent = 'chance to hit ≈ ' + chance + '%  (mod Evade active)';
  };
  Object.values(a).forEach((o) => o.i.addEventListener('input', af));
  af();
  wrap.append(h('details', null, h('summary', null, 'Calculator: chance to hit'), h('div', null, ...Object.values(a).map((o) => o.el), aOut)));
  return wrap;
}

export function formulasView() {
  const root = h('div');
  root.append(h('p', { class: 'muted' }, 'Game version with the mod: the "MOD" boxes show what changes from the original game. Formulas checked against the disassembled code.'));
  root.append(calc());
  D.content.formulas.forEach((s, i) => {
    root.append(h('details', { open: i < 2 }, h('summary', null, s.title), h('div', null, s.blocks.map(block))));
  });
  return root;
}
