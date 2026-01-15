import { describe, it, expect, beforeEach, vi } from "vitest";
import { renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  storeKeys,
  useStoresByOrganizationQuery,
  useStoreQuery,
} from "./queries";
import * as client from "./client";
import { ReactNode } from "react";
import type { Store } from "@laundromate/types";

// Mock the client functions
vi.mock("./client", () => ({
  listStoresByOrganization: vi.fn(),
  getStore: vi.fn(),
}));

describe("storeKeys", () => {
  it("has correct base key", () => {
    expect(storeKeys.all).toEqual(["stores"]);
  });

  it("builds lists key correctly", () => {
    expect(storeKeys.lists()).toEqual(["stores", "list"]);
  });

  it("builds list key with organizationId and filters", () => {
    expect(storeKeys.list("org-1", { skip: 0, limit: 10 })).toEqual([
      "stores",
      "list",
      "org-1",
      { skip: 0, limit: 10 },
    ]);
  });

  it("builds list key with organizationId only", () => {
    expect(storeKeys.list("org-1")).toEqual([
      "stores",
      "list",
      "org-1",
      undefined,
    ]);
  });

  it("builds details key correctly", () => {
    expect(storeKeys.details()).toEqual(["stores", "detail"]);
  });

  it("builds detail key with id", () => {
    expect(storeKeys.detail("store-1")).toEqual([
      "stores",
      "detail",
      "store-1",
    ]);
  });

  it("builds byOrganization key correctly", () => {
    expect(storeKeys.byOrganization("org-1")).toEqual([
      "stores",
      "organization",
      "org-1",
    ]);
  });
});

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

describe("useStoresByOrganizationQuery", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls listStoresByOrganization with organizationId and no params", async () => {
    const mockStores = [
      {
        id: "store-1",
        organizationId: "org-1",
        name: "Store 1",
        streetAddress: "123 Main St",
        city: "New York",
        state: "NY",
        postalCode: "10001",
        country: "US",
        status: "active" as const,
        createdAt: new Date(),
        updatedAt: new Date(),
      },
    ];

    (
      client.listStoresByOrganization as ReturnType<typeof vi.fn>
    ).mockResolvedValueOnce(mockStores);

    const { result } = renderHook(() => useStoresByOrganizationQuery("org-1"), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(client.listStoresByOrganization).toHaveBeenCalledWith(
      "org-1",
      undefined,
    );
    expect(result.current.data).toEqual(mockStores);
  });

  it("calls listStoresByOrganization with params", async () => {
    const mockStores: Store[] = [];
    (
      client.listStoresByOrganization as ReturnType<typeof vi.fn>
    ).mockResolvedValueOnce(mockStores);

    const params = { skip: 10, limit: 20 };
    const { result } = renderHook(
      () => useStoresByOrganizationQuery("org-1", params),
      {
        wrapper: createWrapper(),
      },
    );

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(client.listStoresByOrganization).toHaveBeenCalledWith(
      "org-1",
      params,
    );
  });

  it("is disabled when organizationId is empty string", () => {
    const { result } = renderHook(() => useStoresByOrganizationQuery(""), {
      wrapper: createWrapper(),
    });

    expect(result.current.isFetching).toBe(false);
    expect(client.listStoresByOrganization).not.toHaveBeenCalled();
  });

  it("handles errors correctly", async () => {
    const error = new Error("Network error");
    (
      client.listStoresByOrganization as ReturnType<typeof vi.fn>
    ).mockRejectedValueOnce(error);

    const { result } = renderHook(() => useStoresByOrganizationQuery("org-1"), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(result.current.error).toEqual(error);
  });
});

describe("useStoreQuery", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls getStore with storeId", async () => {
    const mockStore = {
      id: "store-1",
      organizationId: "org-1",
      name: "Test Store",
      streetAddress: "123 Main St",
      city: "New York",
      state: "NY",
      postalCode: "10001",
      country: "US",
      status: "active" as const,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    (client.getStore as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockStore,
    );

    const { result } = renderHook(() => useStoreQuery("store-1"), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(client.getStore).toHaveBeenCalledWith("store-1");
    expect(result.current.data).toEqual(mockStore);
  });

  it("is disabled when storeId is empty string", () => {
    const { result } = renderHook(() => useStoreQuery(""), {
      wrapper: createWrapper(),
    });

    expect(result.current.isFetching).toBe(false);
    expect(client.getStore).not.toHaveBeenCalled();
  });

  it("handles errors correctly", async () => {
    const error = new Error("Store not found");
    (client.getStore as ReturnType<typeof vi.fn>).mockRejectedValueOnce(error);

    const { result } = renderHook(() => useStoreQuery("invalid-id"), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(result.current.error).toEqual(error);
  });
});
