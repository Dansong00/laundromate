/**
 * React Query mutations for organizations.
 * Provides mutation functions for creating and updating organizations.
 * Uses Server Actions for CUD operations (BFF pattern).
 */

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createOrganization, updateOrganization } from "./actions";
import { organizationKeys } from "./queries";
import type {
  Organization,
  OrganizationCreate,
  OrganizationUpdate,
} from "@laundromate/types";

/**
 * Hook to create a new organization.
 */
export function useCreateOrganizationMutation() {
  const queryClient = useQueryClient();

  return useMutation<Organization, Error, OrganizationCreate>({
    mutationFn: (data) => createOrganization(data),
    onSuccess: () => {
      // Invalidate organizations list to refetch
      queryClient.invalidateQueries({ queryKey: organizationKeys.lists() });
    },
  });
}

/**
 * Hook to update an organization.
 */
export function useUpdateOrganizationMutation() {
  const queryClient = useQueryClient();

  return useMutation<
    Organization,
    Error,
    { organizationId: string; data: OrganizationUpdate }
  >({
    mutationFn: ({ organizationId, data }) =>
      updateOrganization(organizationId, data),
    onSuccess: (data, variables) => {
      // Invalidate both the list and the specific organization detail
      queryClient.invalidateQueries({ queryKey: organizationKeys.lists() });
      queryClient.invalidateQueries({
        queryKey: organizationKeys.detail(variables.organizationId),
      });
    },
  });
}
