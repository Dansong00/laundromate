import { describe, it, expect, beforeEach, vi } from "vitest";
import { renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  organizationKeys,
  useOrganizationsQuery,
  useOrganizationQuery,
} from "./queries";
import * as client from "./client";
import { ReactNode } from "react";

// Mock the client functions
vi.mock("./client", () => ({
  listOrganizations: vi.fn(),
  getOrganization: vi.fn(),
}));

describe("organizationKeys", () => {
  it("has correct base key", () => {
    expect(organizationKeys.all).toEqual(["organizations"]);
  });

  it("builds lists key correctly", () => {
    expect(organizationKeys.lists()).toEqual(["organizations", "list"]);
  });

  it("builds list key with filters", () => {
    expect(organizationKeys.list({ skip: 0, limit: 10 })).toEqual([
      "organizations",
      "list",
      { skip: 0, limit: 10 },
    ]);
  });

  it("builds list key without filters", () => {
    expect(organizationKeys.list()).toEqual([
      "organizations",
      "list",
      undefined,
    ]);
  });

  it("builds details key correctly", () => {
    expect(organizationKeys.details()).toEqual(["organizations", "detail"]);
  });

  it("builds detail key with id", () => {
    expect(organizationKeys.detail("org-1")).toEqual([
      "organizations",
      "detail",
      "org-1",
    ]);
  });

  it("builds members key correctly", () => {
    expect(organizationKeys.members("org-1")).toEqual([
      "organizations",
      "detail",
      "org-1",
      "members",
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

describe("useOrganizationsQuery", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls listOrganizations with no params", async () => {
    const mockOrganizations = [
      {
        id: "org-1",
        name: "Org 1",
        billingAddress: "123 Main St",
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
      client.listOrganizations as ReturnType<typeof vi.fn>
    ).mockResolvedValueOnce(mockOrganizations);

    const { result } = renderHook(() => useOrganizationsQuery(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(client.listOrganizations).toHaveBeenCalledWith(undefined);
    expect(result.current.data).toEqual(mockOrganizations);
  });

  it("calls listOrganizations with params", async () => {
    const mockOrganizations: Organization[] = [];
    (
      client.listOrganizations as ReturnType<typeof vi.fn>
    ).mockResolvedValueOnce(mockOrganizations);

    const params = { skip: 10, limit: 20, status: "active" };
    const { result } = renderHook(() => useOrganizationsQuery(params), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(client.listOrganizations).toHaveBeenCalledWith(params);
  });

  it("handles errors correctly", async () => {
    const error = new Error("Network error");
    (
      client.listOrganizations as ReturnType<typeof vi.fn>
    ).mockRejectedValueOnce(error);

    const { result } = renderHook(() => useOrganizationsQuery(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(result.current.error).toEqual(error);
  });
});

describe("useOrganizationQuery", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls getOrganization with organizationId", async () => {
    const mockOrganization = {
      id: "org-1",
      name: "Test Org",
      billingAddress: "123 Main St",
      city: "New York",
      state: "NY",
      postalCode: "10001",
      country: "US",
      status: "active" as const,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    (client.getOrganization as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockOrganization,
    );

    const { result } = renderHook(() => useOrganizationQuery("org-1"), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(client.getOrganization).toHaveBeenCalledWith("org-1");
    expect(result.current.data).toEqual(mockOrganization);
  });

  it("is disabled when organizationId is empty string", () => {
    const { result } = renderHook(() => useOrganizationQuery(""), {
      wrapper: createWrapper(),
    });

    expect(result.current.isFetching).toBe(false);
    expect(client.getOrganization).not.toHaveBeenCalled();
  });

  it("handles errors correctly", async () => {
    const error = new Error("Organization not found");
    (client.getOrganization as ReturnType<typeof vi.fn>).mockRejectedValueOnce(
      error,
    );

    const { result } = renderHook(() => useOrganizationQuery("invalid-id"), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(result.current.error).toEqual(error);
  });
});
