/**
 * React Query queries for organizations.
 * Provides query keys and query functions for fetching organization data.
 */

import { useQuery } from "@tanstack/react-query";
import { listOrganizations, getOrganization } from "./client";
import type { Organization } from "@laundromate/types";

/**
 * Query keys for organizations.
 */
export const organizationKeys = {
  all: ["organizations"] as const,
  lists: () => [...organizationKeys.all, "list"] as const,
  list: (filters?: { skip?: number; limit?: number; status?: string }) =>
    [...organizationKeys.lists(), filters] as const,
  details: () => [...organizationKeys.all, "detail"] as const,
  detail: (id: string) => [...organizationKeys.details(), id] as const,
  members: (id: string) => [...organizationKeys.detail(id), "members"] as const,
};

/**
 * Hook to fetch a list of organizations.
 */
export function useOrganizationsQuery(params?: {
  skip?: number;
  limit?: number;
  status?: string;
}) {
  return useQuery<Organization[]>({
    queryKey: organizationKeys.list(params),
    queryFn: () => listOrganizations(params),
  });
}

/**
 * Hook to fetch a single organization by ID.
 * @param organizationId - Required organization ID (must be non-empty string)
 */
export function useOrganizationQuery(organizationId: string) {
  return useQuery<Organization>({
    queryKey: organizationKeys.detail(organizationId),
    queryFn: () => getOrganization(organizationId),
    enabled: organizationId.length > 0,
  });
}
