// Base API service with automatic backend detection and graceful offline mock fallback

const isNativePlatform =
  typeof window !== 'undefined' &&
  typeof window.Capacitor?.isNativePlatform === 'function' &&
  window.Capacitor.isNativePlatform();

// Browsers retain the local development default. A Capacitor shell must receive
// VITE_BACKEND_URL at build time so an APK never attempts to call its own localhost.
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || (isNativePlatform ? '' : 'http://localhost:8000');

let isBackendReachable = null;

export const checkBackendHealth = async () => {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 1200);
    const response = await fetch(`${BACKEND_URL}/api/health`, {
      method: 'GET',
      signal: controller.signal
    });
    clearTimeout(timeoutId);
    isBackendReachable = response.ok;
    return isBackendReachable;
  } catch (err) {
    isBackendReachable = false;
    return false;
  }
};

export const getBackendStatus = () => isBackendReachable;

export async function request(endpoint, options = {}) {
  const url = `${BACKEND_URL}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    ...options
  };

  try {
    const res = await fetch(url, config);
    if (!res.ok) {
      const errorBody = await res.text();
      throw new Error(`API Error ${res.status}: ${errorBody}`);
    }
    isBackendReachable = true;
    return await res.json();
  } catch (error) {
    // Flag offline and bubble error up to caller so caller can use mock data fallback
    isBackendReachable = false;
    throw error;
  }
}
