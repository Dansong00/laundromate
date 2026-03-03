/**
 * Route constants and helpers for the application.
 * Centralizes route definitions for better maintainability and type safety.
 */

/**
 * Base route paths for different sections of the application.
 */
export const ROUTES = {
  // Public routes
  HOME: "/",
  LOGIN: "/auth/login",
  REGISTER: "/auth/register",
  ACCEPT_INVITATION: "/auth/accept-invitation",

  // Portal routes (customer-facing)
  PORTAL: "/portal",
  PORTAL_ORDERS: "/portal/orders",
  PORTAL_ORDER_DETAIL: (id: string) => `/portal/orders/${id}`,
  PORTAL_ORDERS_NEW: "/portal/orders/new",
  PORTAL_ADDRESSES: "/portal/addresses",
  PORTAL_PROFILE: "/portal/profile",

  // Admin routes
  ADMIN: "/admin",
  ADMIN_ORGANIZATIONS: "/admin/organizations",
  ADMIN_ORGANIZATION_DETAIL: (id: string) => `/admin/organizations/${id}`,
  ADMIN_ORGANIZATION_NEW: "/admin/organizations/new",
  ADMIN_ORGANIZATION_INVITE: (id: string) =>
    `/admin/organizations/${id}/invite-member`,
  ADMIN_ORGANIZATION_STORES: (id: string) =>
    `/admin/organizations/${id}/stores`,
  ADMIN_ORGANIZATION_STORE_NEW: (id: string) =>
    `/admin/organizations/${id}/stores/new`,

  // Store routes
  ADMIN_STORES: "/admin/stores",
  ADMIN_STORE_DETAIL: (id: string) => `/admin/stores/${id}`,
} as const;

/**
 * Type-safe route builder helper.
 * Usage: route(ROUTES.ADMIN_ORGANIZATION_DETAIL, { id: "123" })
 */
export function route(
  routeFn: (param: string) => string,
  params: { id: string },
): string;
export function route(
  routePath: string,
  params?: Record<string, string>,
): string;
export function route(
  routePath: string | ((param: string) => string),
  params?: { id: string } | Record<string, string>,
): string {
  if (typeof routePath === "function") {
    if (params && "id" in params) {
      return routePath(params.id);
    }
    throw new Error("Function route requires { id: string } parameter");
  }
  if (!params) return routePath;
  return Object.entries(params).reduce(
    (path, [key, value]) => path.replace(`:${key}`, value),
    routePath,
  );
}

/**
 * Helper to build query string for routes.
 * Usage: `${ROUTES.PORTAL_ORDERS}?${queryString({ status: "active" })}`
 */
export function queryString(
  params: Record<string, string | number | boolean>,
): string {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    searchParams.append(key, String(value));
  });
  return searchParams.toString();
}
