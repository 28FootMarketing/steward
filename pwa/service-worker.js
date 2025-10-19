/* Basic offline-first cache with stale-while-revalidate */
const CACHE_NAME = "steward-pwa-v1";
const OFFLINE_URL = "/offline.html"; // optional

self.addEventListener("install", (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_NAME);
    await cache.addAll([
      "/",                 // landing
      "/manifest.webmanifest",
      "/app-icons/icon-192.png",
      "/app-icons/icon-512.png"
      // Add "/offline.html" if you create one
    ]);
    self.skipWaiting();
  })());
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.map(k => k !== CACHE_NAME ? caches.delete(k) : null));
    self.clients.claim();
  })());
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  // Bypass non-GET and third-party requests
  if (req.method !== "GET" || new URL(req.url).origin !== location.origin) return;

  event.respondWith((async () => {
    const cache = await caches.open(CACHE_NAME);
    const cached = await cache.match(req);
    const networkFetch = fetch(req).then((res) => {
      cache.put(req, res.clone()).catch(()=>{});
      return res;
    }).catch(() => cached || caches.match(OFFLINE_URL));
    return cached || networkFetch;
  })());
});
