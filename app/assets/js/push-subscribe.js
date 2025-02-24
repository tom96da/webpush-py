function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/-/g, '+')
    .replace(/_/g, '/');
  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);
  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

async function getVapidPublicKey() {
  const response = await fetch('/vapid-public-key');
  const data = await response.json();
  return data.publicKey;
}

async function subscribePush() {
  if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
    alert("Push messaging is not supported in your browser.");
    return;
  }
  if (Notification.permission === "default") {
    await Notification.requestPermission();
  }
  try {
    const reg = await navigator.serviceWorker.register("/assets/js/service-worker.js", { scope: "/assets/js/" });
    if (!reg.active) {
      console.error("Service worker registration failed.");
      return;
    }
    const publicKey = await getVapidPublicKey();
    const applicationServerKey = urlBase64ToUint8Array(publicKey);
    const subscription = await reg.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: applicationServerKey
    });
    const id = "1412"; // Set a unique ID for each user
    const data = {"id": id, "subscription": subscription.toJSON()};
    await fetch(`/subscribe`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    console.log("Push subscription:" , subscription);
  } catch (e) {
    console.error(e);
  }
}

async function unsubscribePush() {
  if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
    alert("Push messaging is not supported in your browser.");
    return;
  }
  try {
    const reg = await navigator.serviceWorker.getRegistration("/assets/js/");
    if (!reg) {
      console.error("Service worker registration not found.");
      return;
    }
    const subscription = await reg.pushManager.getSubscription();
    if (subscription) {
      const id = "1412"; // Set a unique ID for each user
      await subscription.unsubscribe();
      await fetch(`/unsubscribe`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "id": id, "subscription": subscription.toJSON() })
      });
      console.log("Push unsubscription:", subscription);
    } else {
      console.log("No subscription found.");
    }
  } catch (e) {
    console.error(e);
  }
}

document.addEventListener("DOMContentLoaded", async function () {
  const checkbox = document.getElementById('push-subscribe-checkbox');
  try {
    const reg = await navigator.serviceWorker.getRegistration("/assets/js/");
    if (reg) {
      const subscription = await reg.pushManager.getSubscription();
      if (subscription) {
        checkbox.checked = true;
      }
    }
  } catch (e) {
    console.error(e);
  }

  checkbox.addEventListener('change', function (event) {
    checkbox.disabled = true; // Prevent multiple subscriptions
    if (event.target.checked) {
      console.log("Checkbox checked:", event.target.checked);
      subscribePush().then(() => checkbox.disabled = false);
    } else {
      console.log("Checkbox unchecked:", event.target.checked);
      unsubscribePush().then(() => checkbox.disabled = false);
    }
  });
});
