/**
 * @license
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/**
 * Copyright (c) 2014, 2019, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */

/* Service Worker
 * Use service worker to
 * 1. handle fetch of static resources, serve from cache if available
 * 2. handle push notification for web app
 */

var CACHE_NAME = 'static';
var urlsToCache = [
  'index.html',
  'js/',
  'css/'
];

// add urls of static files to cache
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(urlsToCache);
    })
  );
});

// handle fetch
// return response from cache if there's a match
// otherwise fetch from server and add it to cache
self.addEventListener('fetch', function(event) {
  if(/(public_html)/g.test(event.request.url)) {
    event.respondWith(
      caches.match(event.request).then(function(response) {
        return response || fetch(event.request).then(function(response) {
          return caches.open(CACHE_NAME).then(function(cache) {
            cache.put(event.request, response.clone());
            return response;
          });
        });
      })
    );
  }

});

// handle push notification
// currently notification content is generated in sw.js
self.addEventListener('push', function(event) {
  self.registration.showNotification('FixItFast', {
    body: 'A new incident has been assigned to you.',
    icon: 'img/FIF_launcher2_icon.png'
  });
});

// handle clicking on notification card
// navigate existing page to incidents list or open a new window
self.addEventListener('notificationclick', function (event) {
  event.notification.close();
  event.waitUntil(clients.matchAll({
    type: "window"
  }).then(function(clientList) {
    for (var i = 0; i < clientList.length; i++) {
      var client = clientList[i];
      if (client && 'focus' in client)
        client.navigate('index.html?root=incidents&incidentsTab=incidentsTabList');
        return client.focus();
    }
    if (clients.openWindow)
      return clients.openWindow('index.html?root=incidents&incidentsTab=incidentsTabList');
  }));
}, false)
