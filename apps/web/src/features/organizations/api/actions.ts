"use server";

/**
 * Server Actions for organizations.
 * These actions call Next.js API routes which proxy to the FastAPI backend.
 */

import type {
  Organization,
  OrganizationCreate,
  OrganizationUpdate,
} from "@laundromate/types";

/**
 * Create a new organization.
 * Server Action that calls Next.js API route.
 */
export async function createOrganization(
  data: OrganizationCreate,
): Promise<Organization> {
  const res = await fetch("/api/admin/organizations", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    let message = `Request failed with ${res.status}`;
    try {
      const errorData = await res.json();
      message =
        (errorData && (errorData.detail || errorData.message)) || message;
    } catch {
      // ignore JSON parse errors
    }
    throw new Error(message);
  }

  return res.json();
}

/**
 * Update an organization.
 * Server Action that calls Next.js API route.
 */
export async function updateOrganization(
  id: string,
  data: OrganizationUpdate,
): Promise<Organization> {
  const res = await fetch(`/api/admin/organizations/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    let message = `Request failed with ${res.status}`;
    try {
      const errorData = await res.json();
      message =
        (errorData && (errorData.detail || errorData.message)) || message;
    } catch {
      // ignore JSON parse errors
    }
    throw new Error(message);
  }

  return res.json();
}
