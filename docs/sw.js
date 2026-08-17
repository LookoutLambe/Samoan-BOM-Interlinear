/* Service worker: full up-front precache.
 *
 * The reader is meant to work with no connection once installed, so activation
 * pulls every chapter file listed in assets.json (~10 MB across 247 requests)
 * rather than caching lazily. Requests are batched so a phone doesn't open 247
 * sockets at once, and progress is posted back to the page.
 */

// Stamped by scripts/build_web_data.py from a hash of the published files, so
// a redeploy always produces a new cache and never strands readers on an old
// build. Do not edit by hand.
const VERSION = 'af39018ca261';
const CACHE = `bom-${VERSION}`;
const BATCH = 12;

// The shell changes between deploys; the corpus does not, within a version.
// Shell files go network-first so a reader picks up a new build immediately,
// falling back to cache when offline. Everything else stays cache-first.
const SHELL = /\/(index\.html|app\.js|styles\.css|manifest\.webmanifest|assets\.json)$/;
const isShell = (url) => SHELL.test(url.pathname) || url.pathname.endsWith('/');

self.addEventListener('install', (event) => {
  event.waitUntil(self.skipWaiting());
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      const names = await caches.keys();
      await Promise.all(names.filter((n) => n !== CACHE).map((n) => caches.delete(n)));
      await self.clients.claim();
      await precacheAll();
    })()
  );
});

async function post(message) {
  const clients = await self.clients.matchAll({ includeUncontrolled: true });
  for (const client of clients) client.postMessage(message);
}

async function precacheAll() {
  const cache = await caches.open(CACHE);

  let manifest;
  try {
    manifest = await (await fetch(new URL('assets.json', self.registration.scope))).json();
  } catch {
    return;
  }

  const urls = [...manifest.shell, ...manifest.data].map(
    (path) => new URL(path, self.registration.scope).href
  );

  let done = 0;
  for (let i = 0; i < urls.length; i += BATCH) {
    const slice = urls.slice(i, i + BATCH);
    await Promise.all(
      slice.map(async (url) => {
        try {
          // cache.add would refetch assets already stored from a prior visit.
          if (!(await cache.match(url))) await cache.add(url);
        } catch {
          /* A single missing asset shouldn't abort the whole precache. */
        }
      })
    );
    done += slice.length;
    await post({ type: 'precache-progress', done, total: urls.length });
  }
  await post({ type: 'precache-done', total: urls.length });
}

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  if (url.origin !== location.origin) return;

  event.respondWith(
    (async () => {
      const cache = await caches.open(CACHE);

      // Shell: network-first, so a redeploy is picked up on the next load
      // rather than waiting for the cache to be invalidated.
      if (isShell(url) || request.mode === 'navigate') {
        try {
          // `cache: 'no-cache'` revalidates with the server instead of trusting
          // the HTTP cache. GitHub Pages sends max-age=600 on HTML, so a plain
          // fetch here can hand back the previous build's index.html for ten
          // minutes after a deploy — which is exactly the staleness this
          // network-first branch exists to prevent. Revalidation is a 304 when
          // nothing changed, so the cost is a header round-trip.
          const res = await fetch(request.url, {
            cache: 'no-cache',
            credentials: 'same-origin',
          });
          if (res.ok) cache.put(request, res.clone());
          return res;
        } catch {
          const hit =
            (await cache.match(request, { ignoreSearch: true })) ||
            (await cache.match(new URL('index.html', self.registration.scope).href));
          if (hit) return hit;
          return new Response('Offline', { status: 503, statusText: 'Offline' });
        }
      }

      // Corpus and icons: cache-first — immutable within a version, and this
      // is what makes offline reading fast.
      const hit = await cache.match(request, { ignoreSearch: true });
      if (hit) return hit;
      try {
        const res = await fetch(request);
        if (res.ok) cache.put(request, res.clone());
        return res;
      } catch {
        return new Response('Offline', { status: 503, statusText: 'Offline' });
      }
    })()
  );
});
