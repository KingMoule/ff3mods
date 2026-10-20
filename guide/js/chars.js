// Personnages.
import { h } from './util.js';
import { D, idx, itemName, atkName, locName } from './state.js';

const SWD_MOD = {
  Dispatch: 'ignore la défense, une cible', Retort: 'contre, ignore la défense', Slash: '+ Sap, fonctionne sur les boss',
  'Quadra Slam': '4 coups, cibles aléatoires', Empowerer: 'drain PV puis x0,25 en drain PM', Stunner: 'tous + Stop (140/256)',
  'Quadra Slice': '4 coups, ignore la défense', Cleave: 'tous + Death (182/256)',
};

export function srcShort(it) {
  const s = it.src || {};
  if (s.chest && s.chest.length) { const c = s.chest[0]; return 'coffre : ' + (c.loc ? locName(c.loc) : 'carte ' + c.map) + ' (' + c.x + ',' + c.y + ')'; }
  if (s.shop && s.shop.length) return 'boutique : ' + s.shop[0].replace(/_/g, ' ').toLowerCase();
  if (s.steal && s.steal.length) { const m = idx.mon[s.steal[0].m]; return 'vol : ' + (m ? m.name : '?'); }
  if (s.drop && s.drop.length) { const m = idx.mon[s.drop[0].m]; return 'butin : ' + (m ? m.name : '?'); }
  if (s.colo && s.colo.length) return 'Colisée';
  if (s.metamon && s.metamon.length) { const m = idx.mon[s.metamon[0]]; return 'Metamorph : ' + (m ? m.name : '?'); }
  return 'événement / autre';
}

export function charList() {
  const ul = h('ul', { class: 'list card' });
  D.chars.filter((c) => c.id < 14).forEach((c) => {
    ul.append(h('li', null, h('a', { class: 'row chev', href: '#/chars/' + c.name },
      h('div', { class: 'grow' }, h('div', null, c.name), h('div', { class: 'sm' }, c.role || c.cmds.join(', '))))));
  });
  return h('div', null, ul, h('p', { class: 'muted' }, 'Stats et équipement de départ lus dans la ROM (au niveau de départ). Conseils d\'équipement : rédigés, non vérifiés.'));
}

function gearTable(c, type, label, n) {
  const list = D.items.filter((i) => i.type === type && i.equip && i.equip.includes(c.name))
    .sort((a, b) => (b.power || 0) - (a.power || 0)).slice(0, n);
  if (!list.length) return null;
  return h('details', null, h('summary', null, label + ' (meilleurs ' + list.length + ')'),
    h('div', { class: 'scroll' }, h('table', null,
      h('thead', null, h('tr', null, h('th', null, 'Nom'), h('th', { class: 'num' }, type === 'weapon' ? 'BP' : 'Déf'), h('th', null, 'Où'))),
      h('tbody', null, list.map((i) => h('tr', null,
        h('td', null, h('a', { href: '#/more/items/' + i.id }, i.name)), h('td', { class: 'num' }, i.power), h('td', null, srcShort(i))))))));
}

export function charDetail(name) {
  const c = D.chars.find((x) => x.name === name);
  if (!c) return { title: 'Personnage', node: h('p', null, 'Introuvable.') };
  const root = h('div');
  root.append(h('p', null, c.role || ''));
  root.append(h('div', { class: 'kv' },
    [['PV', c.hp], ['PM', c.mp], ['Vigor', c.str], ['Agilité', c.agi], ['Stamina', c.sta], ['Magie', c.mag], ['Atq', c.atk], ['Déf', c.def], ['MDéf', c.mdef], ['Évasion', c.evade + ' %'], ['Blocage', c.mblock + ' %'], ['Fuite', c.run]]
      .map(([k, v]) => h('div', null, h('b', null, v), h('span', null, k)))));
  root.append(h('p', { class: 'muted' }, 'Commandes : ' + c.cmds.join(', ') + ' · niveau de départ ' + c.levelmod + ' vs. moyenne du groupe'));
  const e = c.equip;
  root.append(h('p', { class: 'muted' }, 'Équipement de départ : ' + ['weapon', 'shield', 'helmet', 'armor', 'relic1', 'relic2']
    .map((k) => (e[k] === null || e[k] === 255 ? null : itemName(e[k]))).filter(Boolean).join(', ')));
  if (c.tips) root.append(h('ul', null, c.tips.map((t) => h('li', null, t))));

  // techniques
  const NM = D.misc.natural_magic;
  if (NM[c.name]) {
    root.append(h('h3', null, 'Magie naturelle'), h('table', null, h('thead', null, h('tr', null, h('th', null, 'Sort'), h('th', { class: 'num' }, 'Niveau'))),
      h('tbody', null, NM[c.name].map((s) => h('tr', null, h('td', null, s.spell), h('td', { class: 'num' }, s.level))))));
  }
  if (c.name === 'Cyan') {
    root.append(h('h3', null, 'SwdTech (version mod)'), h('div', { class: 'scroll' }, h('table', null,
      h('thead', null, h('tr', null, h('th', null, 'Technique'), h('th', { class: 'num' }, 'Niv.'), h('th', { class: 'num' }, 'x Fight'), h('th', null, 'Effet'))),
      h('tbody', null, D.misc.swdtech.map((s) => {
        const a = idx.atk[s.id];
        return h('tr', null, h('td', null, s.name), h('td', { class: 'num' }, s.level), h('td', { class: 'num' }, a ? (a.power / 8).toString().replace('.', ',') : '?'), h('td', null, SWD_MOD[s.name] || ''));
      })))));
    root.append(h('p', { class: 'muted' }, 'La jauge se remplit 2x plus vite. Multiplicateur = puissance du sort / 8, lue dans la ROM moddée.'));
  }
  if (c.name === 'Sabin') {
    root.append(h('h3', null, 'Blitz'), h('div', { class: 'scroll' }, h('table', null,
      h('thead', null, h('tr', null, h('th', null, 'Blitz'), h('th', { class: 'num' }, 'Niv.'), h('th', { class: 'num' }, 'Puiss.'), h('th', null, 'Cible'))),
      h('tbody', null, D.misc.blitz.map((s) => {
        const a = idx.atk[s.id];
        return h('tr', null, h('td', null, s.name), h('td', { class: 'num' }, s.level), h('td', { class: 'num' }, a ? a.power : '?'), h('td', null, a ? a.target : ''));
      })))));
    root.append(h('p', { class: 'muted' }, 'Mod : la commande Blitz ouvre une liste ; on choisit le Blitz puis la cible.'));
  }
  if (c.name === 'Mog') {
    root.append(h('h3', null, 'Danses'), h('table', null, h('tbody', null, D.misc.dances.map((d) => h('tr', null, h('th', null, d.name), h('td', null, d.moves.join(', ')))))));
    root.append(h('p', { class: 'muted' }, 'La danse apprise dépend du terrain du combat.'));
  }
  if (c.name === 'Strago') root.append(h('h3', null, 'Lores'), h('p', null, h('a', { href: '#/more/lores' }, '→ Liste des 24 Lores et qui les lance')));
  if (c.name === 'Edgar') {
    const tools = D.items.filter((i) => i.type === 'tool');
    root.append(h('h3', null, 'Outils'), h('ul', null, tools.map((i) => h('li', null, h('a', { href: '#/more/items/' + i.id }, i.name), ' — ' + (i.desc || '').replace(/\n/g, ' ') + ' · ' + srcShort(i)))));
  }
  if (c.name === 'Locke') root.append(h('h3', null, 'Vol'), h('p', null, 'Réussite = niveau de Locke + 50 − niveau de la cible (%), x2 avec la Sneak Ring. Rare : 1/4 (mod).'));
  if (c.name === 'Gau') root.append(h('h3', null, 'Rage'), h('p', null, 'Voir le Bestiaire : chaque fiche donne l\'attaque de Rage.'));
  if (c.gear) root.append(h('h3', null, 'Quel équipement quand ?'), h('ul', null, c.gear.map(([w, t]) => h('li', null, h('b', null, w + ' : '), t))));
  root.append(h('h3', null, 'Meilleur équipement (ROM)'));
  [['weapon', 'Armes', 6], ['armor', 'Armures', 5], ['helmet', 'Casques', 5], ['shield', 'Boucliers', 5]].forEach(([t, l, n]) => {
    const g = gearTable(c, t, l, n); if (g) root.append(g);
  });
  return { title: c.name, back: '#/chars', node: root };
}
