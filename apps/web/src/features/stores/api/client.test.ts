import { describe, it, expect, beforeEach, vi } from "vitest";
import {
  listStoresByOrganization,
  getStore,
  createStore,
  updateStore,
  inviteStoreOwner,
} from "./client";
import type { Store, StoreCreate, StoreUpdate } from "@laundromate/types";
import * as apiClient from "@/lib/api/client";

// Mock the apiFetch and buildQueryString functions
vi.mock("@/lib/api/client", () => ({
  apiFetch: vi.fn(),
  buildQueryString: vi.fn((params) => {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        searchParams.append(key, String(value));
      }
    });
    const queryString = searchParams.toString();
    return queryString ? `?${queryString}` : "";
  }),
}));

describe("listStoresByOrganization", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls apiFetch with correct path and no query params", async () => {
    const mockStores: Store[] = [
      {
        id: "store-1",
        organizationId: "org-1",
        name: "Store 1",
        streetAddress: "123 Main St",
        city: "New York",
        state: "NY",
        postalCode: "10001",
        country: "US",
        status: "active",
        createdAt: new Date(),
        updatedAt: new Date(),
      },
    ];

    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockStores,
    );

    const result = await listStoresByOrganization("org-1");

    expect(apiClient.apiFetch).toHaveBeenCalledWith(
      "/api/admin/stores/organizations/org-1/stores",
    );
    expect(result).toEqual(mockStores);
  });

  it("calls apiFetch with pagination query params", async () => {
    const mockStores: Store[] = [];
    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockStores,
    );

    await listStoresByOrganization("org-1", { skip: 10, limit: 20 });

    expect(apiClient.apiFetch).toHaveBeenCalledWith(
      "/api/admin/stores/organizations/org-1/stores?skip=10&limit=20",
    );
  });

  it("calls apiFetch with only skip param", async () => {
    const mockStores: Store[] = [];
    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockStores,
    );

    await listStoresByOrganization("org-1", { skip: 5 });

    expect(apiClient.apiFetch).toHaveBeenCalledWith(
      "/api/admin/stores/organizations/org-1/stores?skip=5",
    );
  });

  it("calls apiFetch with only limit param", async () => {
    const mockStores: Store[] = [];
    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockStores,
    );

    await listStoresByOrganization("org-1", { limit: 50 });

    expect(apiClient.apiFetch).toHaveBeenCalledWith(
      "/api/admin/stores/organizations/org-1/stores?limit=50",
    );
  });

  it("propagates errors from apiFetch", async () => {
    const error = new Error("Network error");
    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(
      error,
    );

    await expect(listStoresByOrganization("org-1")).rejects.toThrow(
      "Network error",
    );
  });
});

describe("getStore", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls apiFetch with correct path", async () => {
    const mockStore: Store = {
      id: "store-1",
      organizationId: "org-1",
      name: "Test Store",
      streetAddress: "123 Main St",
      city: "New York",
      state: "NY",
      postalCode: "10001",
      country: "US",
      status: "active",
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockStore,
    );

    const result = await getStore("store-1");

    expect(apiClient.apiFetch).toHaveBeenCalledWith(
      "/api/admin/stores/store-1",
    );
    expect(result).toEqual(mockStore);
  });

  it("propagates errors from apiFetch", async () => {
    const error = new Error("Store not found");
    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(
      error,
    );

    await expect(getStore("invalid-id")).rejects.toThrow("Store not found");
  });
});

describe("createStore", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls apiFetch with correct path, method, and body", async () => {
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

    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockStore,
    );

    const result = await createStore(createData);

    expect(apiClient.apiFetch).toHaveBeenCalledWith(
      "/api/admin/stores/organizations/org-1/stores",
      {
        method: "POST",
        body: JSON.stringify(createData),
      },
    );
    expect(result).toEqual(mockStore);
  });

  it("handles optional status field", async () => {
    const createData: StoreCreate = {
      organizationId: "org-1",
      name: "New Store",
      streetAddress: "456 Oak Ave",
      city: "Los Angeles",
      state: "CA",
      postalCode: "90001",
      country: "US",
    };

    const mockStore: Store = {
      ...createData,
      id: "store-new",
      status: "active",
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockStore,
    );

    await createStore(createData);

    const callArgs = (apiClient.apiFetch as ReturnType<typeof vi.fn>).mock
      .calls[0];
    expect(JSON.parse(callArgs[1]?.body as string)).toMatchObject(createData);
  });

  it("propagates errors from apiFetch", async () => {
    const error = new Error("Validation error");
    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(
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

    await expect(createStore(createData)).rejects.toThrow("Validation error");
  });
});

describe("updateStore", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls apiFetch with correct path, method, and body", async () => {
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

    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockStore,
    );

    const result = await updateStore("store-1", updateData);

    expect(apiClient.apiFetch).toHaveBeenCalledWith(
      "/api/admin/stores/store-1",
      {
        method: "PUT",
        body: JSON.stringify(updateData),
      },
    );
    expect(result).toEqual(mockStore);
  });

  it("handles partial updates with null values", async () => {
    const updateData: StoreUpdate = {
      name: null,
      city: null,
    };

    const mockStore: Store = {
      id: "store-1",
      organizationId: "org-1",
      name: "Existing Name",
      streetAddress: "123 Main St",
      city: "Existing City",
      state: "NY",
      postalCode: "10001",
      country: "US",
      status: "active",
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockStore,
    );

    await updateStore("store-1", updateData);

    const callArgs = (apiClient.apiFetch as ReturnType<typeof vi.fn>).mock
      .calls[0];
    expect(JSON.parse(callArgs[1]?.body as string)).toMatchObject({
      name: null,
      city: null,
    });
  });

  it("propagates errors from apiFetch", async () => {
    const error = new Error("Store not found");
    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(
      error,
    );

    const updateData: StoreUpdate = {
      name: "Updated Name",
    };

    await expect(updateStore("invalid-id", updateData)).rejects.toThrow(
      "Store not found",
    );
  });
});

describe("inviteStoreOwner", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls apiFetch with correct path, method, and body", async () => {
    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      undefined,
    );

    await inviteStoreOwner("store-1", "owner@example.com");

    expect(apiClient.apiFetch).toHaveBeenCalledWith(
      "/api/admin/stores/store-1/invite-owner",
      {
        method: "POST",
        body: JSON.stringify({ email: "owner@example.com" }),
      },
    );
  });

  it("propagates errors from apiFetch", async () => {
    const error = new Error("Store not found");
    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(
      error,
    );

    await expect(
      inviteStoreOwner("invalid-id", "owner@example.com"),
    ).rejects.toThrow("Store not found");
  });
});
