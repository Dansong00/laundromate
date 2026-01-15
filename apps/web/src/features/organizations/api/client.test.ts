import { describe, it, expect, beforeEach, vi } from "vitest";
import {
  listOrganizations,
  getOrganization,
  createOrganization,
  updateOrganization,
} from "./client";
import type {
  Organization,
  OrganizationCreate,
  OrganizationUpdate,
} from "@laundromate/types";
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

describe("listOrganizations", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls apiFetch with correct path and no query params", async () => {
    const mockOrganizations: Organization[] = [
      {
        id: "org-1",
        name: "Org 1",
        billingAddress: "123 Main St",
        city: "New York",
        state: "NY",
        postalCode: "10001",
        country: "US",
        contactEmail: "org1@example.com",
        contactPhone: "+1234567890",
        status: "active",
        createdAt: new Date(),
        updatedAt: new Date(),
      },
    ];

    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockOrganizations,
    );

    const result = await listOrganizations();

    expect(apiClient.apiFetch).toHaveBeenCalledWith("/api/admin/organizations");
    expect(result).toEqual(mockOrganizations);
  });

  it("calls apiFetch with query params for pagination", async () => {
    const mockOrganizations: Organization[] = [];
    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockOrganizations,
    );

    await listOrganizations({ skip: 10, limit: 20 });

    expect(apiClient.apiFetch).toHaveBeenCalledWith(
      "/api/admin/organizations?skip=10&limit=20",
    );
  });

  it("calls apiFetch with status filter", async () => {
    const mockOrganizations: Organization[] = [];
    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockOrganizations,
    );

    await listOrganizations({ status: "active" });

    expect(apiClient.apiFetch).toHaveBeenCalledWith(
      "/api/admin/organizations?status=active",
    );
  });

  it("calls apiFetch with all query params", async () => {
    const mockOrganizations: Organization[] = [];
    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockOrganizations,
    );

    await listOrganizations({ skip: 0, limit: 10, status: "inactive" });

    expect(apiClient.apiFetch).toHaveBeenCalledWith(
      "/api/admin/organizations?skip=0&limit=10&status=inactive",
    );
  });

  it("propagates errors from apiFetch", async () => {
    const error = new Error("Network error");
    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(
      error,
    );

    await expect(listOrganizations()).rejects.toThrow("Network error");
  });
});

describe("getOrganization", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls apiFetch with correct path", async () => {
    const mockOrganization: Organization = {
      id: "org-1",
      name: "Test Org",
      billingAddress: "123 Main St",
      city: "New York",
      state: "NY",
      postalCode: "10001",
      country: "US",
      contactEmail: "test@example.com",
      contactPhone: "+1234567890",
      status: "active",
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockOrganization,
    );

    const result = await getOrganization("org-1");

    expect(apiClient.apiFetch).toHaveBeenCalledWith(
      "/api/admin/organizations/org-1",
    );
    expect(result).toEqual(mockOrganization);
  });

  it("propagates errors from apiFetch", async () => {
    const error = new Error("Organization not found");
    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(
      error,
    );

    await expect(getOrganization("invalid-id")).rejects.toThrow(
      "Organization not found",
    );
  });
});

describe("createOrganization", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls apiFetch with correct path, method, and body", async () => {
    const createData: OrganizationCreate = {
      name: "New Org",
      billingAddress: "456 Oak Ave",
      city: "Los Angeles",
      state: "CA",
      postalCode: "90001",
      country: "US",
      contactEmail: "neworg@example.com",
      contactPhone: "+1987654321",
      status: "active",
    };

    const mockOrganization: Organization = {
      ...createData,
      id: "org-new",
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockOrganization,
    );

    const result = await createOrganization(createData);

    expect(apiClient.apiFetch).toHaveBeenCalledWith(
      "/api/admin/organizations",
      {
        method: "POST",
        body: JSON.stringify(createData),
      },
    );
    expect(result).toEqual(mockOrganization);
  });

  it("handles null contactEmail and contactPhone", async () => {
    const createData: OrganizationCreate = {
      name: "New Org",
      billingAddress: "456 Oak Ave",
      city: "Los Angeles",
      state: "CA",
      postalCode: "90001",
      country: "US",
      contactEmail: null,
      contactPhone: null,
    };

    const mockOrganization: Organization = {
      ...createData,
      id: "org-new",
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockOrganization,
    );

    await createOrganization(createData);

    const callArgs = (apiClient.apiFetch as ReturnType<typeof vi.fn>).mock
      .calls[0];
    expect(JSON.parse(callArgs[1]?.body as string)).toMatchObject({
      contactEmail: null,
      contactPhone: null,
    });
  });

  it("propagates errors from apiFetch", async () => {
    const error = new Error("Validation error");
    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(
      error,
    );

    const createData: OrganizationCreate = {
      name: "New Org",
      billingAddress: "456 Oak Ave",
      city: "Los Angeles",
      state: "CA",
      postalCode: "90001",
      country: "US",
    };

    await expect(createOrganization(createData)).rejects.toThrow(
      "Validation error",
    );
  });
});

describe("updateOrganization", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls apiFetch with correct path, method, and body", async () => {
    const updateData: OrganizationUpdate = {
      name: "Updated Org",
      status: "inactive",
    };

    const mockOrganization: Organization = {
      id: "org-1",
      name: "Updated Org",
      billingAddress: "123 Main St",
      city: "New York",
      state: "NY",
      postalCode: "10001",
      country: "US",
      contactEmail: "test@example.com",
      contactPhone: "+1234567890",
      status: "inactive",
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockOrganization,
    );

    const result = await updateOrganization("org-1", updateData);

    expect(apiClient.apiFetch).toHaveBeenCalledWith(
      "/api/admin/organizations/org-1",
      {
        method: "PUT",
        body: JSON.stringify(updateData),
      },
    );
    expect(result).toEqual(mockOrganization);
  });

  it("handles partial updates with null values", async () => {
    const updateData: OrganizationUpdate = {
      name: null,
      contactEmail: null,
    };

    const mockOrganization: Organization = {
      id: "org-1",
      name: "Existing Name",
      billingAddress: "123 Main St",
      city: "New York",
      state: "NY",
      postalCode: "10001",
      country: "US",
      contactEmail: null,
      contactPhone: "+1234567890",
      status: "active",
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockOrganization,
    );

    await updateOrganization("org-1", updateData);

    const callArgs = (apiClient.apiFetch as ReturnType<typeof vi.fn>).mock
      .calls[0];
    expect(JSON.parse(callArgs[1]?.body as string)).toMatchObject({
      name: null,
      contactEmail: null,
    });
  });

  it("propagates errors from apiFetch", async () => {
    const error = new Error("Organization not found");
    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(
      error,
    );

    const updateData: OrganizationUpdate = {
      name: "Updated Name",
    };

    await expect(updateOrganization("invalid-id", updateData)).rejects.toThrow(
      "Organization not found",
    );
  });
});
