/**
 * API client functions for organizations.
 * Provides functions to interact with the organizations API endpoints.
 */

import { apiFetch, buildQueryString } from "@/lib/api/client";
import type {
  Organization,
  OrganizationCreate,
  OrganizationUpdate,
} from "@laundromate/types";

/**
 * List all organizations with optional filtering and pagination.
 */
export async function listOrganizations(params?: {
  skip?: number;
  limit?: number;
  status?: string;
}): Promise<Organization[]> {
  const queryParams: Record<string, string | number | undefined> = {};
  if (params?.skip !== undefined) queryParams.skip = params.skip;
  if (params?.limit !== undefined) queryParams.limit = params.limit;
  if (params?.status) queryParams.status = params.status;

  const queryString = buildQueryString(queryParams);
  return apiFetch<Organization[]>(`/api/admin/organizations${queryString}`);
}

/**
 * Get a specific organization by ID.
 */
export async function getOrganization(
  organizationId: string,
): Promise<Organization> {
  return apiFetch<Organization>(`/api/admin/organizations/${organizationId}`);
}

/**
 * Create a new organization.
 */
export async function createOrganization(
  data: OrganizationCreate,
): Promise<Organization> {
  return apiFetch<Organization>("/api/admin/organizations", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

/**
 * Update an organization.
 */
export async function updateOrganization(
  organizationId: string,
  data: OrganizationUpdate,
): Promise<Organization> {
  return apiFetch<Organization>(`/api/admin/organizations/${organizationId}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });
}
