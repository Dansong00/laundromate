/**
 * Base API client utility for making HTTP requests to Next.js API routes.
 * Provides a centralized apiFetch function with authentication and error handling.
 * All requests are routed through Next.js API routes which proxy to the FastAPI backend.
 */

import axios, { type AxiosInstance, type AxiosRequestConfig } from "axios";
import { toApiError } from "@/lib/api/error";

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

function normalizeApiPath(path: string): string {
  // We use an Axios baseURL of "/api", so callers may pass:
  // - "/api/foo"  -> "/foo"
  // - "/foo"      -> "/foo"
  // - "foo"       -> "/foo"
  if (path.startsWith("/api/")) return path.slice(4);
  if (path === "/api") return "/";
  if (path.startsWith("/")) return path;
  return `/${path}`;
}

function toPlainHeaders(
  headersInit: HeadersInit | undefined,
): Record<string, string> {
  if (!headersInit) return {};
  if (headersInit instanceof Headers) {
    const out: Record<string, string> = {};
    headersInit.forEach((value, key) => {
      out[key] = value;
    });
    return out;
  }
  if (Array.isArray(headersInit)) {
    const out: Record<string, string> = {};
    for (const [key, value] of headersInit) out[key] = value;
    return out;
  }
  return headersInit as Record<string, string>;
}

let apiAxios: AxiosInstance | null = null;
function getApiAxios(): AxiosInstance {
  if (apiAxios) return apiAxios;

  apiAxios = axios.create({
    baseURL: "/api",
  });

  apiAxios.interceptors.request.use((config) => {
    config.headers = config.headers ?? {};

    // Default Content-Type if not provided
    if (
      !("Content-Type" in config.headers) &&
      !("content-type" in config.headers)
    ) {
      config.headers["Content-Type"] = "application/json";
    }

    // Attach bearer token on the client when available, unless caller already set it
    const token = getAccessToken();
    const hasAuth =
      "Authorization" in config.headers || "authorization" in config.headers;
    if (token && !hasAuth) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  });

  apiAxios.interceptors.response.use(
    (res) => res,
    (err) => Promise.reject(toApiError(err)),
  );

  return apiAxios;
}

/**
 * Generic API fetch function with authentication and error handling.
 * Routes requests through Next.js API routes (BFF pattern).
 * @param path - API endpoint path (with or without leading slash, e.g., "/api/super-admin/organizations")
 * @param options - Fetch options (method, body, headers, etc.)
 * @returns Promise resolving to the response data
 * @throws Error if request fails
 */
export async function apiFetch<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const url = normalizeApiPath(path);
  const headers = toPlainHeaders(options.headers);

  const config: AxiosRequestConfig = {
    url,
    method: (options.method || "GET") as AxiosRequestConfig["method"],
    headers,
    // Preserve fetch semantics: caller provides body as string (usually JSON.stringify)
    data: options.body,
    // Avoid caching surprises in browser
    withCredentials: true,
  };

  const res = await getApiAxios().request(config);
  const data = res.data;

  // Some endpoints may return no content
  if (data === "" || data === null || typeof data === "undefined") {
    return undefined as unknown as T;
  }

  return data as T;
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
