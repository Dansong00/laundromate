/**
 * React Query mutations for stores.
 * Provides mutation functions for creating and updating stores.
 * Uses Server Actions for CUD operations (BFF pattern).
 */

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createStore, updateStore } from "./actions";
import { storeKeys } from "./queries";
import type { Store, StoreCreate, StoreUpdate } from "@laundromate/types";

/**
 * Hook to create a new store.
 */
export function useCreateStoreMutation() {
  const queryClient = useQueryClient();

  return useMutation<Store, Error, StoreCreate>({
    mutationFn: createStore,
    onSuccess: (data) => {
      // Invalidate stores list for the organization
      queryClient.invalidateQueries({
        queryKey: storeKeys.byOrganization(data.organizationId),
      });
      queryClient.invalidateQueries({ queryKey: storeKeys.lists() });
    },
  });
}

/**
 * Hook to update a store.
 */
export function useUpdateStoreMutation() {
  const queryClient = useQueryClient();

  return useMutation<Store, Error, { storeId: string; data: StoreUpdate }>({
    mutationFn: ({ storeId, data }) => updateStore(storeId, data),
    onSuccess: (data, variables) => {
      // Invalidate both the list and the specific store detail
      queryClient.invalidateQueries({
        queryKey: storeKeys.byOrganization(data.organizationId),
      });
      queryClient.invalidateQueries({ queryKey: storeKeys.lists() });
      queryClient.invalidateQueries({
        queryKey: storeKeys.detail(variables.storeId),
      });
    },
  });
}
