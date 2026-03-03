/**
 * Server-side API route utilities for Next.js API routes.
 * Provides helpers for proxying requests to the FastAPI backend with authentication.
 */

import { NextRequest, NextResponse } from "next/server";
import axios, { type AxiosRequestConfig } from "axios";
import { auth } from "@clerk/nextjs/server";
import { toApiError } from "@/lib/api/error";

/**
 * Get the backend API URL, preferring internal Docker service name.
 */
export function getApiUrl(): string {
  return (
    process.env.API_URL_INTERNAL ||
    process.env.NEXT_PUBLIC_API_URL ||
    "http://localhost:8000"
  );
}

/**
 * Extract authorization token from request (cookie, header, or Clerk session).
 * Returns the token string or null if not found.
 */
export async function getAuthToken(req: NextRequest): Promise<string | null> {
  // Check cookie first (legacy auth)
  const cookieToken = req.cookies.get("access_token")?.value;
  if (cookieToken) {
    return cookieToken;
  }

  // Fall back to Authorization header (from client-side requests)
  const headerAuth = req.headers.get("authorization");
  if (headerAuth) {
    // Extract token from "Bearer <token>" format
    const match = headerAuth.match(/^Bearer\s+(.+)$/i);
    return match ? match[1] : headerAuth;
  }

  // Try Clerk session token
  try {
    const { getToken } = await auth();
    const clerkToken = await getToken();
    if (clerkToken) {
      return clerkToken;
    }
  } catch {
    // Clerk auth not available or failed
  }

  return null;
}

/**
 * Build authorization headers from request.
 * Returns headers object with Authorization header if token is available.
 */
export async function getAuthHeaders(
  req: NextRequest,
): Promise<Record<string, string>> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  const token = await getAuthToken(req);
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  return headers;
}

/**
 * Build query string from URLSearchParams, filtering out null/undefined values.
 */
export function buildQueryString(
  params: URLSearchParams,
  additionalParams?: Record<
    string,
    string | number | boolean | null | undefined
  >,
): string {
  const searchParams = new URLSearchParams(params);

  if (additionalParams) {
    Object.entries(additionalParams).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        searchParams.append(key, String(value));
      }
    });
  }

  const queryString = searchParams.toString();
  return queryString ? `?${queryString}` : "";
}

/**
 * Proxy a request to the backend API.
 * Handles authentication, request forwarding, and response parsing.
 *
 * @param req - Next.js request object
 * @param backendPath - Backend API path (e.g., "/super-admin/organizations")
 * @param options - Additional fetch options (method, body, etc.)
 * @returns NextResponse with proxied backend response
 */
export async function proxyToBackend(
  req: NextRequest,
  backendPath: string,
  options: {
    method?: string;
    body?: unknown;
    searchParams?: Record<string, string | number | boolean | null | undefined>;
  } = {},
): Promise<NextResponse> {
  const apiUrl = getApiUrl();
  const headers = await getAuthHeaders(req);

  // Build URL with query params
  const baseUrl = `${apiUrl}${
    backendPath.startsWith("/") ? backendPath : `/${backendPath}`
  }`;
  const queryString = buildQueryString(
    req.nextUrl.searchParams,
    options.searchParams,
  );
  const url = `${baseUrl}${queryString}`;

  const method = options.method || req.method;

  // Add body if provided or from request
  let dataToSend: unknown = undefined;
  if (options.body !== undefined) {
    dataToSend = options.body;
  } else if (req.method !== "GET" && req.method !== "HEAD") {
    try {
      dataToSend = await req.json();
    } catch {
      // No body or invalid JSON, continue without body
    }
  }

  const config: AxiosRequestConfig = {
    url,
    method: method as AxiosRequestConfig["method"],
    headers,
    data: dataToSend,
    // Always respond with the backend status code instead of throwing
    validateStatus: () => true,
  };

  try {
    const res = await axios.request(config);
    const payload =
      res.data === "" || res.data === null || typeof res.data === "undefined"
        ? {}
        : res.data;
    return NextResponse.json(payload, { status: res.status });
  } catch (err) {
    const apiErr = toApiError(err);
    return NextResponse.json(
      {
        message: apiErr.message,
        status: apiErr.status,
        details: apiErr.details,
        code: apiErr.code,
      },
      { status: apiErr.status ?? 502 },
    );
  }
}

/**
 * Helper for GET requests - proxies to backend with query params.
 */
export async function proxyGet(
  req: NextRequest,
  backendPath: string,
  additionalParams?: Record<
    string,
    string | number | boolean | null | undefined
  >,
): Promise<NextResponse> {
  return proxyToBackend(req, backendPath, {
    method: "GET",
    searchParams: additionalParams,
  });
}

/**
 * Helper for POST requests - proxies to backend with body.
 */
export async function proxyPost(
  req: NextRequest,
  backendPath: string,
  body?: unknown,
): Promise<NextResponse> {
  return proxyToBackend(req, backendPath, {
    method: "POST",
    body,
  });
}

/**
 * Helper for PUT requests - proxies to backend with body.
 */
export async function proxyPut(
  req: NextRequest,
  backendPath: string,
  body?: unknown,
): Promise<NextResponse> {
  return proxyToBackend(req, backendPath, {
    method: "PUT",
    body,
  });
}

/**
 * Helper for DELETE requests.
 */
export async function proxyDelete(
  req: NextRequest,
  backendPath: string,
): Promise<NextResponse> {
  return proxyToBackend(req, backendPath, {
    method: "DELETE",
  });
}
