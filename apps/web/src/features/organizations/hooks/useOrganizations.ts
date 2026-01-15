/**
 * Custom hooks for organizations.
 * Provides convenient hooks that wrap React Query queries and mutations.
 */

export { useOrganizationsQuery, useOrganizationQuery } from "../api/queries";
export {
  useCreateOrganizationMutation,
  useUpdateOrganizationMutation,
} from "../api/mutations";
