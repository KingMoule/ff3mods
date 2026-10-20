// Petits utilitaires : création de DOM, stockage tolérant aux erreurs.

export function h(tag, attrs, ...kids) {
  const el = document.createElement(tag);
  if (attrs) {
    for (const [k, v] of Object.entries(attrs)) {
      if (v === null || v === undefined || v === false) continue;
      if (k === 'class') el.className = v;
      else if (k === 'html') el.innerHTML = v;
      else if (k.startsWith('on') && typeof v === 'function') el.addEventListener(k.slice(2), v);
      else if (v === true) el.setAttribute(k, '');
      else el.setAttribute(k, v);
    }
  }
  add(el, kids);
  return el;
}

function add(el, kids) {
  for (const k of kids) {
    if (k === null || k === undefined || k === false) continue;
    if (Array.isArray(k)) add(el, k);
    else el.appendChild(k instanceof Node ? k : document.createTextNode(String(k)));
  }
}

// localStorage peut être indisponible (mode privé, données bloquées) : tout est protégé.
const mem = {};
export const store = {
  get(key, fallback) {
    try {
      const v = localStorage.getItem('ff6g.' + key);
      if (v !== null) return JSON.parse(v);
    } catch (e) { /* ignore */ }
    return key in mem ? mem[key] : fallback;
  },
  set(key, value) {
    mem[key] = value;
    try { localStorage.setItem('ff6g.' + key, JSON.stringify(value)); return true; } catch (e) { return false; }
  },
  remove(key) {
    delete mem[key];
    try { localStorage.removeItem('ff6g.' + key); } catch (e) { /* ignore */ }
  },
};

export const nf = new Intl.NumberFormat('fr-FR');
export const pct = (a, b) => (b ? Math.round((100 * a) / b) : 0);
export const uniq = (a) => [...new Set(a)];
