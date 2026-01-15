/**
 * React Query queries for stores.
 * Provides query keys and query functions for fetching store data.
 */

import { useQuery } from "@tanstack/react-query";
import { listStoresByOrganization, getStore } from "./client";
import type { Store } from "@laundromate/types";

/**
 * Query keys for stores.
 */
export const storeKeys = {
  all: ["stores"] as const,
  lists: () => [...storeKeys.all, "list"] as const,
  list: (organizationId: string, filters?: { skip?: number; limit?: number }) =>
    [...storeKeys.lists(), organizationId, filters] as const,
  details: () => [...storeKeys.all, "detail"] as const,
  detail: (id: string) => [...storeKeys.details(), id] as const,
  byOrganization: (organizationId: string) =>
    [...storeKeys.all, "organization", organizationId] as const,
};

/**
 * Hook to fetch stores for a specific organization.
 * @param organizationId - Required organization ID (must be non-empty string)
 */
export function useStoresByOrganizationQuery(
  organizationId: string,
  params?: {
    skip?: number;
    limit?: number;
  },
) {
  return useQuery<Store[]>({
    queryKey: storeKeys.list(organizationId, params),
    queryFn: () => listStoresByOrganization(organizationId, params),
    enabled: organizationId.length > 0,
  });
}

/**
 * Hook to fetch a single store by ID.
 * @param storeId - Required store ID (must be non-empty string)
 */
export function useStoreQuery(storeId: string) {
  return useQuery<Store>({
    queryKey: storeKeys.detail(storeId),
    queryFn: () => getStore(storeId),
    enabled: storeId.length > 0,
  });
}
