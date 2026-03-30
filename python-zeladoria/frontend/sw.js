const CACHE_NAME = 'zelo-v4';
const STATIC_ASSETS = ['/app', '/manifest.json'];

// ── Instalação ─────────────────────────────────────────
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(STATIC_ASSETS))
            .catch(() => {})
    );
    self.skipWaiting();
});

// ── Ativação (limpa caches antigos) ────────────────────
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(
                keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
            )
        )
    );
    self.clients.claim();
});

// ── Fetch strategy ─────────────────────────────────────
self.addEventListener('fetch', event => {
    const url = new URL(event.request.url);

    // API — network first, cache como fallback offline
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(
            fetch(event.request)
                .then(resp => {
                    if (resp.ok) {
                        const clone = resp.clone();
                        caches.open(CACHE_NAME).then(c => c.put(event.request, clone));
                    }
                    return resp;
                })
                .catch(() => caches.match(event.request))
        );
        return;
    }

    // Assets estáticos — cache first
    event.respondWith(
        caches.match(event.request).then(cached => {
            if (cached) return cached;
            return fetch(event.request).then(resp => {
                if (resp && resp.ok) {
                    const clone = resp.clone();
                    caches.open(CACHE_NAME).then(c => c.put(event.request, clone));
                }
                return resp;
            });
        })
    );
});

// ── Push Notifications ─────────────────────────────────
self.addEventListener('push', event => {
    const data = event.data ? event.data.json() : {};
    const title = data.title || 'Zelô — Zeladoria de Belém';
    const options = {
        body:    data.body  || 'Atualização no seu chamado',
        icon:    data.icon  || '/static/icons/icon-192.png',
        badge:   '/static/icons/icon-192.png',
        tag:     data.tag   || 'zelo-notif',
        renotify: true,
        data: { url: data.url || '/app' },
        actions: [
            { action: 'ver',    title: 'Ver agora' },
            { action: 'fechar', title: 'Fechar'    },
        ],
        vibrate: [200, 100, 200],
    };
    event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', event => {
    event.notification.close();
    if (event.action === 'fechar') return;
    const url = event.notification.data?.url || '/app';
    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true })
            .then(cls => {
                const match = cls.find(c => c.url.includes('/app'));
                if (match) return match.focus();
                return clients.openWindow(url);
            })
    );
});

// ── Background Sync (fila offline) ─────────────────────
self.addEventListener('sync', event => {
    if (event.tag === 'sync-chamados') {
        event.waitUntil(syncChamadosPendentes());
    }
});

async function syncChamadosPendentes() {
    // Lê fila do IndexedDB (implementado no frontend)
    // Esta função é chamada quando a conexão é restaurada
    const clients_list = await clients.matchAll();
    clients_list.forEach(c => c.postMessage({ type: 'SYNC_COMPLETE' }));
}
