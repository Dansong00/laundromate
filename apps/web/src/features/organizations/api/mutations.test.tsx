import { describe, it, expect, beforeEach, vi } from "vitest";
import { renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  useCreateOrganizationMutation,
  useUpdateOrganizationMutation,
} from "./mutations";
import * as actions from "./actions";
import type {
  Organization,
  OrganizationCreate,
  OrganizationUpdate,
} from "@laundromate/types";
import { ReactNode } from "react";

// Mock the actions
vi.mock("./actions", () => ({
  createOrganization: vi.fn(),
  updateOrganization: vi.fn(),
}));

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: 0 },
      mutations: { retry: false },
    },
  });

  const TestWrapper = ({ children }: { children: ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
  TestWrapper.displayName = "TestWrapper";
  return TestWrapper;
}

describe("useCreateOrganizationMutation", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls createOrganization action on success", async () => {
    const createData: OrganizationCreate = {
      name: "New Org",
      billingAddress: "123 Main St",
      city: "New York",
      state: "NY",
      postalCode: "10001",
      country: "US",
    };

    const mockOrganization: Organization = {
      ...createData,
      id: "org-new",
      status: "active",
      contactEmail: null,
      contactPhone: null,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    (
      actions.createOrganization as ReturnType<typeof vi.fn>
    ).mockResolvedValueOnce(mockOrganization);

    const { result } = renderHook(() => useCreateOrganizationMutation(), {
      wrapper: createWrapper(),
    });

    result.current.mutate(createData);

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(actions.createOrganization).toHaveBeenCalledWith(createData);
    expect(result.current.data).toEqual(mockOrganization);
  });

  it("handles errors correctly", async () => {
    const error = new Error("Validation error");
    (
      actions.createOrganization as ReturnType<typeof vi.fn>
    ).mockRejectedValueOnce(error);

    const createData: OrganizationCreate = {
      name: "New Org",
      billingAddress: "123 Main St",
      city: "New York",
      state: "NY",
      postalCode: "10001",
      country: "US",
    };

    const { result } = renderHook(() => useCreateOrganizationMutation(), {
      wrapper: createWrapper(),
    });

    result.current.mutate(createData);

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(result.current.error).toEqual(error);
  });
});

describe("useUpdateOrganizationMutation", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls updateOrganization action on success", async () => {
    const updateData: OrganizationUpdate = {
      name: "Updated Org",
    };

    const mockOrganization: Organization = {
      id: "org-1",
      name: "Updated Org",
      billingAddress: "123 Main St",
      city: "New York",
      state: "NY",
      postalCode: "10001",
      country: "US",
      status: "active",
      contactEmail: null,
      contactPhone: null,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    (
      actions.updateOrganization as ReturnType<typeof vi.fn>
    ).mockResolvedValueOnce(mockOrganization);

    const { result } = renderHook(() => useUpdateOrganizationMutation(), {
      wrapper: createWrapper(),
    });

    result.current.mutate({ organizationId: "org-1", data: updateData });

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(actions.updateOrganization).toHaveBeenCalledWith(
      "org-1",
      updateData,
    );
    expect(result.current.data).toEqual(mockOrganization);
  });

  it("handles errors correctly", async () => {
    const error = new Error("Organization not found");
    (
      actions.updateOrganization as ReturnType<typeof vi.fn>
    ).mockRejectedValueOnce(error);

    const updateData: OrganizationUpdate = {
      name: "Updated Name",
    };

    const { result } = renderHook(() => useUpdateOrganizationMutation(), {
      wrapper: createWrapper(),
    });

    result.current.mutate({ organizationId: "invalid-id", data: updateData });

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(result.current.error).toEqual(error);
  });
});
