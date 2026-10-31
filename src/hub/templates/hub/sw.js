const CACHE = "little-wms-v2";
const ASSETS = [
    "/",
    "/static/hub/bootstrap/css/bootstrap.min.css",
    "/static/hub/bootstrap/js/bootstrap.bundle.min.js",
    "/static/hub/jquery/jquery.min.js",
    "/static/hub/symbols/Logo.svg",
];

self.addEventListener("install", (event) => {
    event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(ASSETS)));
});

self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((keys) =>
            Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key)))
        )
    );
});

self.addEventListener("fetch", (event) => {
    if (event.request.method !== "GET") return;
    // Network-first for pages so they are never stale (e.g. after a language
    // change); cache-first for static assets.
    if (event.request.mode === "navigate") {
        event.respondWith(fetch(event.request).catch(() => caches.match("/")));
        return;
    }
    event.respondWith(
        caches.match(event.request).then((cached) => cached || fetch(event.request))
    );
});
