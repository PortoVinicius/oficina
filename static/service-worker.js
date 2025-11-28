// Nome do cache
const CACHE_NAME = "oficina-cache-v1";

// Arquivos que serão armazenados offline
const urlsToCache = [
  "/",
  "/static/css/style.css",
  "/static/js/install.js",
  "/static/img/logo-192.png",
  "/static/img/logo-512.png",

];

// INSTALAÇÃO — Mantemos sua lógica original
self.addEventListener("install", (event) => {
  console.log("Service Worker instalado");

  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(urlsToCache);
    })
  );
});

// ATIVAÇÃO — Limpando versões antigas
self.addEventListener("activate", (event) => {
  console.log("Service Worker ativado");

  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    })
  );
});

// INTERCEPTAÇÃO DE REQUISIÇÕES — Trabalhar offline
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      return cachedResponse || fetch(event.request);
    })
  );
});
