"use server";

/**
 * Server Actions for stores.
 * These actions call Next.js API routes which proxy to the FastAPI backend.
 */

import type { Store, StoreCreate, StoreUpdate } from "@laundromate/types";

/**
 * Create a new store for an organization.
 * Server Action that calls Next.js API route.
 */
export async function createStore(data: StoreCreate): Promise<Store> {
  const res = await fetch(
    `/api/admin/stores/organizations/${data.organizationId}/stores`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    },
  );

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
 * Update a store.
 * Server Action that calls Next.js API route.
 */
export async function updateStore(
  id: string,
  data: StoreUpdate,
): Promise<Store> {
  const res = await fetch(`/api/admin/stores/${id}`, {
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
