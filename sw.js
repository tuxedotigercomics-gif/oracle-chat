// Oracle Chat — offline cache for the hosted (phone/guest) build.
// The app shell is updated from the network when available; downloaded model
// files and the transformers.js library are cached so chat keeps working
// without a connection after the first successful load.
const CACHE = 'oracle-chat-v6';
const SHELL = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png', './apple-touch-icon.png'];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE)
      .then(cache => cache.addAll(SHELL))
      .then(() => self.skipWaiting())
      .catch(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// The page asks a freshly installed worker to take over immediately so an
// installed Home Screen app can load the new build on its next foreground.
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') self.skipWaiting();
});

function remember(request, response) {
  if (response && (response.ok || response.type === 'opaque')) {
    const copy = response.clone();
    caches.open(CACHE).then(cache => cache.put(request, copy)).catch(() => {});
  }
  return response;
}

self.addEventListener('fetch', event => {
  const request = event.request;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);

  if (url.origin === self.location.origin) {
    if (request.mode === 'navigate') {
      event.respondWith(
        fetch(request)
          .then(response => {
            remember('./index.html', response.clone());
            return response;
          })
          .catch(() => caches.match('./index.html'))
      );
      return;
    }
    event.respondWith(
      caches.match(request).then(hit => hit || fetch(request).then(response => remember(request, response)))
    );
    return;
  }

  // Never cache partial responses — a cached 206 would corrupt an asset.
  if (request.headers.has('range')) return;

  // Only the wllama JS/WASM runtime lives here. GGUF weights are persisted by
  // wllama itself in OPFS; caching them here would store a second full copy on
  // the phone and be wiped by every service-worker cache version bump.
  if (/cdn\.jsdelivr\.net/.test(url.hostname)) {
    event.respondWith(
      caches.match(request).then(hit => {
        if (hit) return hit;
        return fetch(request)
          .then(response => remember(request, response))
          .catch(() => hit);
      })
    );
  }
});
