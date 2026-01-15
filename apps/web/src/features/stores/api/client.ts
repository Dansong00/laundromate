/**
 * API client functions for stores.
 * Provides functions to interact with the stores API endpoints.
 */

import { apiFetch, buildQueryString } from "@/lib/api/client";
import type { Store, StoreCreate, StoreUpdate } from "@laundromate/types";

/**
 * List all stores for a specific organization.
 */
export async function listStoresByOrganization(
  organizationId: string,
  params?: {
    skip?: number;
    limit?: number;
  },
): Promise<Store[]> {
  const queryParams: Record<string, string | number | undefined> = {};
  if (params?.skip !== undefined) queryParams.skip = params.skip;
  if (params?.limit !== undefined) queryParams.limit = params.limit;

  const queryString = buildQueryString(queryParams);
  return apiFetch<Store[]>(
    `/api/admin/stores/organizations/${organizationId}/stores${queryString}`,
  );
}

/**
 * Get a specific store by ID.
 */
export async function getStore(storeId: string): Promise<Store> {
  return apiFetch<Store>(`/api/admin/stores/${storeId}`);
}

/**
 * Create a new store for an organization.
 */
export async function createStore(data: StoreCreate): Promise<Store> {
  return apiFetch<Store>(
    `/api/admin/stores/organizations/${data.organizationId}/stores`,
    {
      method: "POST",
      body: JSON.stringify(data),
    },
  );
}

/**
 * Update a store.
 */
export async function updateStore(
  storeId: string,
  data: StoreUpdate,
): Promise<Store> {
  return apiFetch<Store>(`/api/admin/stores/${storeId}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

/**
 * Invite a store owner (deprecated - use organization-level invitations instead).
 * @deprecated This endpoint is deprecated. Use organization-level invitations instead.
 */
export async function inviteStoreOwner(
  storeId: string,
  email: string,
): Promise<void> {
  // Note: This endpoint may not exist in the backend anymore
  // Keeping for backwards compatibility but marked as deprecated
  return apiFetch<void>(`/api/admin/stores/${storeId}/invite-owner`, {
    method: "POST",
    body: JSON.stringify({ email }),
  });
}
