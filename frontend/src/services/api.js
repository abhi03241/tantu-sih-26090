// Base API service with automatic backend detection and graceful offline mock fallback

const isNativePlatform =
  typeof window !== 'undefined' &&
  typeof window.Capacitor?.isNativePlatform === 'function' &&
  window.Capacitor.isNativePlatform();

// Vercel deployment / Capacitor shells receive VITE_API_BASE_URL or VITE_BACKEND_URL at build time.
const BACKEND_URL =
  import.meta.env.VITE_API_BASE_URL ||
  import.meta.env.VITE_BACKEND_URL ||
  (isNativePlatform ? '' : 'http://localhost:8000');

const normalizedBackendUrl = BACKEND_URL.replace(/\/$/, '');

// FastAPI deliberately returns `/uploads/...` and `/enhanced/...` routes so
// local clients can use them directly. A Vercel page has a different origin,
// so hydrate just those API asset URLs before React renders them.
function resolveAssetUrl(url) {
  if (typeof url !== 'string' || !url.startsWith('/')) return url;
  return normalizedBackendUrl ? `${normalizedBackendUrl}${url}` : url;
}

function hydrateAssetUrls(payload) {
  if (Array.isArray(payload)) return payload.map(hydrateAssetUrls);
  if (!payload || typeof payload !== 'object') return payload;

  return Object.fromEntries(Object.entries(payload).map(([key, value]) => [
    key,
    key === 'image_url' || key === 'enhanced_image_url'
      ? resolveAssetUrl(value)
      : hydrateAssetUrls(value)
  ]));
}

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
    ...options,
    headers: {
      ...(options.body instanceof FormData ? {} : { 'Content-Type': 'application/json' }),
      ...options.headers
    }
  };

  try {
    const res = await fetch(url, config);
    if (!res.ok) {
      const errorBody = await res.text();
      throw new Error(`API Error ${res.status}: ${errorBody}`);
    }
    isBackendReachable = true;
    return hydrateAssetUrls(await res.json());
  } catch (error) {
    // Flag offline and bubble error up to caller so caller can use mock data fallback
    isBackendReachable = false;
    throw error;
  }
}
