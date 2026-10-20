/* Service worker du guide — généré par tools/build_data.py (ne pas éditer sw.js à la main). */
const VERSION = "a988bb1a3b";
const CACHE = "ff6guide-" + VERSION;
const ASSETS = [
 "./",
 "css/app.css",
 "data/attacks.json",
 "data/chars.json",
 "data/content.json",
 "data/espers.json",
 "data/items.json",
 "data/misc.json",
 "data/mod_diff.json",
 "data/monsters.json",
 "data/walkthrough.json",
 "data/world.json",
 "icons/apple-touch-icon.png",
 "icons/icon-192.png",
 "icons/icon-512.png",
 "icons/icon-maskable-512.png",
 "index.html",
 "js/app.js",
 "js/bestiary.js",
 "js/chars.js",
 "js/formulas.js",
 "js/more.js",
 "js/state.js",
 "js/util.js",
 "js/walk.js",
 "manifest.webmanifest"
];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k.startsWith("ff6guide-") && k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  e.respondWith(
    caches.match(req, { ignoreSearch: true }).then((hit) => {
      if (hit) return hit;
      return fetch(req).catch(() => caches.match("./index.html"));
    })
  );
});
