
const API_URL = import.meta.env.VITE_API_BASE_URL ||
  'http://127.0.0.1:8000';

async function authRequest(endpoint, data) {
  const response = await fetch(`${API_URL}${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });

  const result = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(
      result.detail || 'Authentication failed.'
    );
  }

  return result;
}

export function registerUser(data) {
  return authRequest('/api/auth/register', data);
}

export function loginUser(data) {
  return authRequest('/api/auth/login', data);
}
