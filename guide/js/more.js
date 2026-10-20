// Section « Plus » : espers, objets, boutiques, Colisée, Lores, carte des rencontres, tables, mod, quêtes, réglages.
import { h, store, nf } from './util.js';
import { D, idx, itemName, atkName, locName, monLink, elChip, resetChecks, getChecks, importChecks } from './state.js';
import { srcShort } from './chars.js';

const MENU = [
  ['espers', 'Espers', 'Sorts enseignés, bonus de niveau, lieux'],
  ['items', 'Objets & équipement', 'Stats, sources (coffres, boutiques, vol…)'],
  ['shops', 'Boutiques', 'Stock de chaque boutique'],
  ['colosseum', 'Colisée', 'Objet misé → adversaire → gain'],
  ['lores', 'Lores (Strago)', '24 Lores et qui les lance'],
  ['techs', 'SwdTech, Blitz, Danses', 'Niveaux et effets'],
  ['world', 'Carte des rencontres', 'Monstres par secteur du monde'],
  ['tables', 'Tables PV / PM / EXP', 'Par niveau'],
  ['mods', 'Différences du mod', 'Ce qui change par rapport au jeu d\'origine'],
  ['quests', 'Quêtes annexes & astuces', 'Manquables, choix exclusifs'],
  ['rare', 'Objets de quête', 'Les 20 objets rares'],
  ['settings', 'Réglages & sauvegarde', 'Thème, export/import, effacer'],
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
      h('div', null, h('p', null, 'Attaque : ' + e.attack), table(['Sort enseigné', 'Taux (par PM)'], rows),
        e.bonus_desc ? h('p', { class: 'muted' }, 'Bonus de niveau : ' + e.bonus_desc.replace(/\n/g, ' ')) : null,
        e.hint && e.hint.length ? h('p', { class: 'muted' }, 'Indice (scripts de la ROM) : ' + e.hint.join(', ')) : null)));
  });
  root.append(h('p', { class: 'muted' }, 'Taux : multiplicateur de progression d\'apprentissage (x1 = base ; les sorts finissent à 100 %). Les lieux sont des indices déduits des scripts d\'événement.'));
  return root;
}

const TYPES = { weapon: 'Armes', armor: 'Armures', shield: 'Boucliers', helmet: 'Casques', relic: 'Reliques', tool: 'Outils', consumable: 'Consommables' };
let itemState = { q: '', t: null };
function items() {
  const root = h('div');
  const input = h('input', { type: 'search', placeholder: 'Nom d\'objet…', value: itemState.q, 'aria-label': 'Recherche' });
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
  if (!i) return { title: 'Objet', node: h('p', null, 'Introuvable.') };
  const root = h('div');
  root.append(h('p', { class: 'muted' }, TYPES[i.type] + ' · prix ' + nf.format(i.price) + ' gil'));
  if (i.desc) root.append(h('p', null, i.desc.replace(/\n/g, ' ')));
  const rows = [];
  const add = (k, v) => { if (v !== undefined && v !== '' && !(Array.isArray(v) && !v.length)) rows.push(h('tr', null, h('th', null, k), h('td', null, Array.isArray(v) ? v.join(', ') : String(v)))); };
  if (i.equip) {
    add(i.type === 'weapon' ? 'BP' : 'Défense', i.power);
    add(i.type === 'weapon' ? 'Précision' : 'Déf. magique', i.type === 'weapon' ? i.hit : i.mdef);
    add('Élément', i.element); add('Absorbe', i.absorb); add('Annule', i.null); add('Faible', i.weak);
    add('Effet', i.special); add('Particularités', i.wflags);
    const b = i.bonus; add('Bonus', ['str', 'spd', 'sta', 'mag'].filter((k) => b[k]).map((k) => ({ str: 'Vigor', spd: 'Vitesse', sta: 'Stamina', mag: 'Magie' }[k] + ' ' + (b[k] > 0 ? '+' : '') + b[k])));
    add('Évasion', i.evade ? i.evade + ' %' : ''); add('Blocage mag.', i.mevade ? i.mevade + ' %' : '');
    add('Immunité', i.immune); add('Statuts auto', i.auto); add('Effets', i.fx); add('Terrain', i.field);
    if (i.teaches) add('Enseigne', atkName(i.teaches.spell) + ' (x' + i.teaches.rate + ')');
    if (i.cast) add('Lance', atkName(i.cast.spell) + (i.cast.random ? ' (aléatoire)' : ''));
    add('Équipable par', i.equip.length === 14 ? 'tous' : i.equip);
  } else if (i.type === 'tool') add('Sort', atkName(i.cast.spell));
  root.append(h('table', null, h('tbody', null, rows)));
  const s = i.src || {};
  root.append(h('h3', null, 'Où l\'obtenir'));
  const ul = h('ul');
  (s.chest || []).forEach((c) => ul.append(h('li', null, 'Coffre : ' + (c.loc ? locName(c.loc) : 'carte ' + c.map) + ' (' + c.x + ',' + c.y + ')')));
  (s.shop || []).forEach((n) => ul.append(h('li', null, 'Boutique : ' + n.replace(/_/g, ' ').toLowerCase())));
  (s.steal || []).forEach((x) => ul.append(h('li', null, 'Vol (' + (x.rare ? 'rare' : 'commun') + ') : ', monLink(x.m))));
  (s.drop || []).forEach((x) => ul.append(h('li', null, 'Butin (' + (x.rare ? 'rare' : 'commun') + ') : ', monLink(x.m))));
  (s.colo || []).forEach((x) => ul.append(h('li', null, 'Colisée : miser ' + itemName(x.bet) + ' contre ', monLink(x.m))));
  (s.metamon || []).slice(0, 12).forEach((m) => ul.append(h('li', null, 'Metamorph sur ', monLink(m))));
  root.append(ul.children.length ? ul : h('p', { class: 'muted' }, 'Aucune source en coffre/boutique/vol : récompense d\'événement ou autre.'));
  return { title: i.name, back: '#/more/items', node: root };
}

function shops() {
  const root = h('div');
  D.misc.shops.filter((s) => s.items.length).forEach((s) => {
    root.append(h('details', null, h('summary', null, s.name.replace(/_/g, ' ').toLowerCase()),
      h('div', null, table(['Objet', 'Prix'], s.items.map((i) => h('tr', null, h('td', null, h('a', { href: '#/more/items/' + i }, itemName(i))), h('td', { class: 'num' }, nf.format(idx.item[i].price))))))));
  });
  root.append(h('p', { class: 'muted' }, 'Les suffixes _1/_2/_3 correspondent aux états successifs du magasin (Balance puis Ruine). Prix de vente = moitié.'));
  return root;
}

function colosseum() {
  const rows = [];
  D.misc.colosseum.forEach((c) => {
    if (!idx.item[c.bet] || !idx.item[c.bet].name || c.monster === 255 || c.monster === 0 && c.prize === 0) return;
    const m = idx.mon[c.monster];
    if (!m) return;
    rows.push(h('tr', null, h('td', null, h('a', { href: '#/more/items/' + c.bet }, itemName(c.bet))), h('td', null, monLink(c.monster)),
      h('td', null, h('a', { href: '#/more/items/' + c.prize }, itemName(c.prize)), c.hidden ? h('span', { class: 'tag' }, 'nom caché') : null)));
  });
  return h('div', null, h('input', { type: 'search', placeholder: 'Filtrer…', 'aria-label': 'Filtre', oninput: (e) => {
    const q = e.target.value.toLowerCase();
    rows.forEach((r) => { r.style.display = r.textContent.toLowerCase().includes(q) ? '' : 'none'; });
  } }), table(['Miser', 'Adversaire', 'Gain'], rows), h('p', { class: 'muted' }, 'Lu dans la table du Colisée (ROM).'));
}

function lores() {
  const root = h('div');
  const start = new Set(D.misc.lore_start);
  root.append(h('p', { class: 'muted' }, D.content.lore_hint));
  D.misc.lores.forEach((l) => {
    const a = idx.atk[l.id];
    const srcs = (D.misc.lore_sources[String(l.id)] || []).map((id) => monLink(id));
    root.append(h('details', null, h('summary', null, l.name + (start.has(l.idx) ? ' · connu au départ' : '')),
      h('div', null, a ? h('p', { class: 'muted' }, 'PM ' + a.mp + ' · puissance ' + a.power + ' · ' + a.target + (a.element.length ? ' · ' + a.element.join('/') : '')) : null,
        srcs.length ? h('div', { class: 'chips' }, srcs) : h('p', { class: 'muted' }, 'Aucun monstre ne la lance dans les scripts normaux.'))));
  });
  return root;
}

function techs() {
  const root = h('div');
  root.append(h('h3', null, 'SwdTech (Cyan, version mod)'),
    table(['Nom', 'Niv.', 'x Fight'], D.misc.swdtech.map((s) => h('tr', null, h('td', null, s.name), h('td', { class: 'num' }, s.level), h('td', { class: 'num' }, ((idx.atk[s.id].power) / 8).toString().replace('.', ','))))));
  root.append(h('h3', null, 'Blitz (Sabin)'),
    table(['Nom', 'Niv.', 'Puiss.'], D.misc.blitz.map((s) => h('tr', null, h('td', null, s.name), h('td', { class: 'num' }, s.level), h('td', { class: 'num' }, idx.atk[s.id].power)))));
  root.append(h('h3', null, 'Danses (Mog)'), table(['Danse', 'Attaques'], D.misc.dances.map((d) => h('tr', null, h('td', null, d.name), h('td', null, d.moves.join(', '))))));
  return root;
}

let wSel = { w: 0, s: null };
function worldView(w, s) {
  if (w !== undefined) wSel = { w: +w, s: s !== undefined ? +s : null };
  const root = h('div');
  const W = D.world[String(wSel.w)];
  const tabs = h('div', { class: 'chips' }, [0, 1].map((k) => h('a', { class: 'chip' + (wSel.w === k ? ' on' : ''), href: '#/more/world/' + k }, k === 0 ? 'Monde de la Balance' : 'Monde de la Ruine')));
  const grid = h('div', { class: 'grid8' });
  for (let sec = 0; sec < 64; sec++) {
    const c = W[String(sec)];
    const b = h('a', { class: 'chip' + (wSel.s === sec ? ' on' : ''), href: '#/more/world/' + wSel.w + '/' + sec, style: 'padding:6px 0;text-align:center;border-radius:6px' }, String(sec));
    if (!c || !c.all.length) b.style.opacity = '.4';
    grid.append(b);
  }
  root.append(tabs, h('p', { class: 'muted' }, 'Carte 8×8 (colonne = secteur % 8, ligne = secteur ÷ 8, nord en haut). Touchez un secteur.'), grid);
  if (wSel.s !== null) {
    const c = W[String(wSel.s)];
    root.append(h('h3', null, 'Secteur ' + wSel.s + ' (colonne ' + (wSel.s % 8 + 1) + ', ligne ' + (Math.floor(wSel.s / 8) + 1) + ')'));
    if (c && c.near) root.append(h('p', { class: 'muted' }, 'Point de repère le plus proche : ' + locName(c.near)));
    const terrNames = ['Plaine', 'Forêt', 'Désert', 'Terre (≈)'];
    if (!c || !c.all.length) root.append(h('p', null, 'Aucune rencontre.'));
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
  return h('div', null, table(['Niv.', 'EXP pour y arriver', 'PV gagnés', 'PM gagnés'], rows),
    h('p', { class: 'muted' }, 'Tables brutes de la ROM (la colonne EXP est l\'EXP requis du niveau 2 au 99).'));
}

function mods() {
  const root = h('div');
  root.append(h('p', null, 'Mod ff3mods pour FF3 US v1.1 (sans header) : correctifs de bugs, mini-équilibrage et menu Blitz. Toutes les données de ce guide sont lues dans la ROM moddée.'));
  let g = null; let ul = null;
  D.content.mods.forEach((m) => {
    if (m.group !== g) { g = m.group; root.append(h('h2', null, g)); ul = h('ul', { class: 'list card' }); root.append(ul); }
    ul.append(h('li', null, h('div', { class: 'row' }, h('div', { class: 'grow' }, h('b', null, m.title), h('div', { class: 'sm' }, m.text)))));
  });
  root.append(h('h2', null, 'Données modifiées (diff ROM)'));
  if (!D.mod_diff.length) root.append(h('p', { class: 'muted' }, 'Aucune (guide généré sans ROM moddée).'));
  else root.append(table(['Table', 'Entrée', 'Octets (offset : avant → après)'], D.mod_diff.map((d) => h('tr', null, h('td', null, d.kind), h('td', null, d.name + ' #' + d.id),
    h('td', null, d.bytes.map((b) => b[0] + ' : ' + b[1] + '→' + b[2]).join(' · '))))));
  return root;
}

function quests() {
  return h('div', null, D.content.sidequests.map((q) => h('div', { class: 'card' }, h('b', null, q.title), q.g ? h('span', { class: 'tag' }, '≈') : null, h('p', null, q.text))),
    h('p', { class: 'muted' }, '« ≈ » : connaissance de jeu, non vérifiée dans la ROM.'));
}

function rare() {
  return h('ul', { class: 'list card' }, D.misc.rare_items.map((n) => h('li', null, h('div', { class: 'row' }, n))));
}

function settings() {
  const root = h('div');
  const theme = store.get('theme', 'auto');
  const sel = h('select', null, ['auto', 'light', 'dark'].map((v) => h('option', { value: v, selected: v === theme }, { auto: 'Automatique', light: 'Clair', dark: 'Sombre' }[v])));
  sel.addEventListener('change', () => { store.set('theme', sel.value); applyTheme(); });
  root.append(h('h3', null, 'Thème'), sel);
  const area = h('textarea', { rows: 4, readonly: true });
  const exp = h('button', { class: 'btn', type: 'button' }, 'Exporter ma progression');
  exp.addEventListener('click', () => { area.value = JSON.stringify(getChecks()); area.readOnly = false; area.select(); });
  const imp = h('button', { class: 'btn', type: 'button' }, 'Importer (coller le texte ci-dessus)');
  imp.addEventListener('click', () => {
    try { const o = JSON.parse(area.value); if (o && typeof o === 'object') { importChecks(o); alert('Progression importée.'); } } catch (e) { alert('Texte invalide.'); }
  });
  const rs = h('button', { class: 'btn danger', type: 'button' }, 'Effacer toute la progression');
  rs.addEventListener('click', () => { if (confirm('Effacer toutes les cases cochées ?')) { resetChecks(); alert('Progression effacée.'); } });
  root.append(h('h3', null, 'Progression'), area, h('div', { class: 'chips' }, exp, imp), rs);
  const st = h('p', { class: 'muted' }, 'Hors-ligne : vérification…');
  root.append(h('h3', null, 'Hors-ligne'), st);
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistration().then((r) => {
      st.textContent = r && r.active ? 'Service worker actif : le guide fonctionne sans réseau.' : 'Service worker en cours d\'installation (rechargez la page).';
    }).catch(() => { st.textContent = 'Service worker indisponible.'; });
  } else st.textContent = 'Ce navigateur ne gère pas les service workers.';
  root.append(h('footer', { class: 'foot' }, 'Guide généré depuis la ROM FF3 US v1.1 + mod ff3mods. Aucune ROM n\'est incluse.'));
  return root;
}

export function applyTheme() {
  const t = store.get('theme', 'auto');
  if (t === 'auto') document.documentElement.removeAttribute('data-theme');
  else document.documentElement.setAttribute('data-theme', t);
}

const TITLES = { espers: 'Espers', items: 'Objets & équipement', shops: 'Boutiques', colosseum: 'Colisée', lores: 'Lores', techs: 'Techniques', world: 'Rencontres du monde', tables: 'Tables', mods: 'Différences du mod', quests: 'Quêtes & astuces', rare: 'Objets de quête', settings: 'Réglages' };

export function moreView(parts) {
  const [sub, a, b] = parts;
  if (!sub) return { title: 'Plus', node: moreMenu() };
  if (sub === 'items' && a) return itemDetail(+a);
  const fn = { espers, items, shops, colosseum, lores, techs, tables, mods, quests, rare, settings }[sub];
  if (sub === 'world') return { title: TITLES.world, back: '#/more', node: worldView(a, b) };
  if (!fn) return { title: 'Plus', node: moreMenu() };
  // items and espers are bottom tabs: no back button
  return { title: TITLES[sub], back: sub === 'items' || sub === 'espers' ? null : '#/more', node: fn() };
}
