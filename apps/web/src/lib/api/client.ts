/**
 * Base API client utility for making HTTP requests to the backend API.
 * Provides a centralized apiFetch function with authentication and error handling.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Get the access token from session storage
 */
function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return sessionStorage.getItem("access_token");
}

/**
 * Get authorization header with bearer token
 */
export function getAuthHeader(): Record<string, string> {
  const token = getAccessToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

/**
 * Generic API fetch function with authentication and error handling
 * @param path - API endpoint path (with or without leading slash)
 * @param options - Fetch options (method, body, headers, etc.)
 * @returns Promise resolving to the response data
 * @throws Error if request fails
 */
export async function apiFetch<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const url = `${API_URL}${path.startsWith("/") ? path : `/${path}`}`;
  const headers = new Headers(options.headers || {});

  // Set Content-Type if not already set
  if (!headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  // Attach bearer token on the client when available
  const authHeader = getAuthHeader();
  if (authHeader.Authorization && !headers.has("Authorization")) {
    headers.set("Authorization", authHeader.Authorization);
  }

  const res = await fetch(url, { ...options, headers });

  if (!res.ok) {
    let message = `Request failed with ${res.status}`;
    try {
      const data = await res.json();
      message = (data && (data.detail || data.message)) || message;
    } catch {
      // ignore JSON parse errors
    }
    throw new Error(message);
  }

  // Some endpoints may return no content
  const text = await res.text();
  return text ? (JSON.parse(text) as T) : (undefined as unknown as T);
}

/**
 * Helper to build query string from parameters
 */
export function buildQueryString(
  params: Record<string, string | number | boolean | undefined>,
): string {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      searchParams.append(key, String(value));
    }
  });
  const queryString = searchParams.toString();
  return queryString ? `?${queryString}` : "";
}
