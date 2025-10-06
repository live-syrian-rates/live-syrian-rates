importScripts('https://www.gstatic.com/firebasejs/9.22.1/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.22.1/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey: "AIzaSyANmR1UrR8aMUag3gNHrFFNmiXMQzekeXg",
  authDomain: "syrian-currency.firebaseapp.com",
  projectId: "syrian-currency",
  storageBucket: "syrian-currency.firebasestorage.app",
  messagingSenderId: "58493358809",
  appId: "1:58493358809:web:6eebd63d123855210424c8"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage(function(payload) {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});
