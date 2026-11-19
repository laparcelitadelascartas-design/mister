/* Míster · funcionamiento sin conexión */
const CACHE = "mister-6dcc658251";
const IA = "mister-ia-1";
const CORE = ["./", "./index.html", "./manifest.webmanifest", "./icon-192.png", "./icon-512.png", "./apple-touch-icon.png"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(CORE)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  /* la IA (unos 13 MB) se guarda aparte para no volver a descargarla en cada actualización */
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE && k !== IA).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});

const guardar = (req, res) => { const copia = res.clone(); caches.open(CACHE).then((c) => c.put(req, copia)); return res; };

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (req.mode === "navigate") {
    /* Con conexión carga la última versión; sin conexión, la guardada */
    e.respondWith(fetch(req).then((res) => guardar("./index.html", res)).catch(() => caches.match("./index.html")));
    return;
  }
  if (url.origin === location.origin && url.pathname.indexOf("/ia/") >= 0) {
    e.respondWith(caches.open(IA).then((c) => c.match(req).then((hit) => hit || fetch(req).then((res) => { if (res.ok) c.put(req, res.clone()); return res; }))));
    return;
  }
  if (url.origin === location.origin || /fonts\.(googleapis|gstatic)\.com$/.test(url.hostname)) {
    e.respondWith(caches.match(req).then((hit) => hit || fetch(req).then((res) => guardar(req, res))));
  }
});
