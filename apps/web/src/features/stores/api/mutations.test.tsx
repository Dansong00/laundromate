import { describe, it, expect, beforeEach, vi } from "vitest";
import { renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useCreateStoreMutation, useUpdateStoreMutation } from "./mutations";
import * as actions from "./actions";
import type { Store, StoreCreate, StoreUpdate } from "@laundromate/types";
import { ReactNode } from "react";

// Mock the actions
vi.mock("./actions", () => ({
  createStore: vi.fn(),
  updateStore: vi.fn(),
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

describe("useCreateStoreMutation", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls createStore action on success", async () => {
    const createData: StoreCreate = {
      organizationId: "org-1",
      name: "New Store",
      streetAddress: "456 Oak Ave",
      city: "Los Angeles",
      state: "CA",
      postalCode: "90001",
      country: "US",
      status: "active",
    };

    const mockStore: Store = {
      ...createData,
      id: "store-new",
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    (actions.createStore as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockStore,
    );

    const { result } = renderHook(() => useCreateStoreMutation(), {
      wrapper: createWrapper(),
    });

    result.current.mutate(createData);

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(actions.createStore).toHaveBeenCalledTimes(1);
    expect(
      (actions.createStore as ReturnType<typeof vi.fn>).mock.calls[0][0],
    ).toEqual(createData);
    expect(result.current.data).toEqual(mockStore);
  });

  it("handles errors correctly", async () => {
    const error = new Error("Validation error");
    (actions.createStore as ReturnType<typeof vi.fn>).mockRejectedValueOnce(
      error,
    );

    const createData: StoreCreate = {
      organizationId: "org-1",
      name: "New Store",
      streetAddress: "456 Oak Ave",
      city: "Los Angeles",
      state: "CA",
      postalCode: "90001",
      country: "US",
    };

    const { result } = renderHook(() => useCreateStoreMutation(), {
      wrapper: createWrapper(),
    });

    result.current.mutate(createData);

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(result.current.error).toEqual(error);
  });
});

describe("useUpdateStoreMutation", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls updateStore action on success", async () => {
    const updateData: StoreUpdate = {
      name: "Updated Store",
      status: "inactive",
    };

    const mockStore: Store = {
      id: "store-1",
      organizationId: "org-1",
      name: "Updated Store",
      streetAddress: "123 Main St",
      city: "New York",
      state: "NY",
      postalCode: "10001",
      country: "US",
      status: "inactive",
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    (actions.updateStore as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockStore,
    );

    const { result } = renderHook(() => useUpdateStoreMutation(), {
      wrapper: createWrapper(),
    });

    result.current.mutate({ storeId: "store-1", data: updateData });

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(actions.updateStore).toHaveBeenCalledWith("store-1", updateData);
    expect(result.current.data).toEqual(mockStore);
  });

  it("handles errors correctly", async () => {
    const error = new Error("Store not found");
    (actions.updateStore as ReturnType<typeof vi.fn>).mockRejectedValueOnce(
      error,
    );

    const updateData: StoreUpdate = {
      name: "Updated Name",
    };

    const { result } = renderHook(() => useUpdateStoreMutation(), {
      wrapper: createWrapper(),
    });

    result.current.mutate({ storeId: "invalid-id", data: updateData });

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(result.current.error).toEqual(error);
  });
});
