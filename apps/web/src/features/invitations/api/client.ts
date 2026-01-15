/**
 * API client functions for invitations.
 * Provides functions to interact with the invitation API endpoints.
 */

import { apiFetch } from "@/lib/api/client";

export interface InvitationValidateResponse {
  valid: boolean;
  email?: string | null;
  organizationId?: string | null;
  organizationName?: string | null;
  organizationRole?: "owner" | "employee" | "admin" | null;
  reason?: string | null;
}

export interface InvitationAcceptRequest {
  password: string;
}

export interface InvitationAcceptResponse {
  access_token: string;
  token_type: string;
  user: {
    id: string;
    email?: string | null;
    phone?: string | null;
    [key: string]: unknown;
  };
}

/**
 * Validate an invitation token.
 */
export async function validateInvitation(
  token: string,
): Promise<InvitationValidateResponse> {
  return apiFetch<InvitationValidateResponse>(
    `/auth/invitations/${token}/validate`,
  );
}

/**
 * Accept an invitation with a password.
 */
export async function acceptInvitation(
  token: string,
  password: string,
): Promise<InvitationAcceptResponse> {
  return apiFetch<InvitationAcceptResponse>(
    `/auth/invitations/${token}/accept`,
    {
      method: "POST",
      body: JSON.stringify({ password }),
    },
  );
}
