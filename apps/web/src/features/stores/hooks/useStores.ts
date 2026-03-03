/**
 * Custom hooks for stores.
 * Provides convenient hooks that wrap React Query queries and mutations.
 */

export { useStoresByOrganizationQuery, useStoreQuery } from "../api/queries";
export {
  useCreateStoreMutation,
  useUpdateStoreMutation,
} from "../api/mutations";
