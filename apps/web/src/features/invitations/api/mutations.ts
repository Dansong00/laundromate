/**
 * React Query mutations for invitations.
 * Provides mutation functions for validating and accepting invitations.
 */

import { useMutation } from "@tanstack/react-query";
import { validateInvitation, acceptInvitation } from "./client";
import type {
  InvitationValidateResponse,
  InvitationAcceptResponse,
} from "./client";

/**
 * Hook to validate an invitation token.
 */
export function useValidateInvitationMutation() {
  return useMutation<InvitationValidateResponse, Error, string>({
    mutationFn: validateInvitation,
  });
}

/**
 * Hook to accept an invitation.
 */
export function useAcceptInvitationMutation() {
  return useMutation<
    InvitationAcceptResponse,
    Error,
    { token: string; password: string }
  >({
    mutationFn: ({ token, password }) => acceptInvitation(token, password),
  });
}
