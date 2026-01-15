import { describe, it, expect, beforeEach, vi } from "vitest";
import { renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  useValidateInvitationMutation,
  useAcceptInvitationMutation,
} from "./mutations";
import * as client from "./client";
import type {
  InvitationValidateResponse,
  InvitationAcceptResponse,
} from "./client";
import { ReactNode } from "react";

// Mock the client functions
vi.mock("./client", () => ({
  validateInvitation: vi.fn(),
  acceptInvitation: vi.fn(),
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

describe("useValidateInvitationMutation", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls validateInvitation on success", async () => {
    const mockResponse: InvitationValidateResponse = {
      valid: true,
      email: "test@example.com",
      organizationId: "org-123",
      organizationName: "Test Org",
      organizationRole: "owner",
    };

    (
      client.validateInvitation as ReturnType<typeof vi.fn>
    ).mockResolvedValueOnce(mockResponse);

    const { result } = renderHook(() => useValidateInvitationMutation(), {
      wrapper: createWrapper(),
    });

    result.current.mutate("token-123");

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(client.validateInvitation).toHaveBeenCalledTimes(1);
    expect(
      (client.validateInvitation as ReturnType<typeof vi.fn>).mock.calls[0][0],
    ).toBe("token-123");
    expect(result.current.data).toEqual(mockResponse);
  });

  it("handles invalid invitation response", async () => {
    const mockResponse: InvitationValidateResponse = {
      valid: false,
      reason: "Token expired",
    };

    (
      client.validateInvitation as ReturnType<typeof vi.fn>
    ).mockResolvedValueOnce(mockResponse);

    const { result } = renderHook(() => useValidateInvitationMutation(), {
      wrapper: createWrapper(),
    });

    result.current.mutate("expired-token");

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(result.current.data?.valid).toBe(false);
    expect(result.current.data?.reason).toBe("Token expired");
  });

  it("handles errors correctly", async () => {
    const error = new Error("Network error");
    (
      client.validateInvitation as ReturnType<typeof vi.fn>
    ).mockRejectedValueOnce(error);

    const { result } = renderHook(() => useValidateInvitationMutation(), {
      wrapper: createWrapper(),
    });

    result.current.mutate("token-123");

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(result.current.error).toEqual(error);
  });
});

describe("useAcceptInvitationMutation", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls acceptInvitation on success", async () => {
    const mockResponse: InvitationAcceptResponse = {
      access_token: "access-token-123",
      token_type: "bearer",
      user: {
        id: "user-123",
        email: "test@example.com",
        phone: "+1234567890",
      },
    };

    (client.acceptInvitation as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockResponse,
    );

    const { result } = renderHook(() => useAcceptInvitationMutation(), {
      wrapper: createWrapper(),
    });

    result.current.mutate({ token: "token-123", password: "password123" });

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(client.acceptInvitation).toHaveBeenCalledWith(
      "token-123",
      "password123",
    );
    expect(result.current.data).toEqual(mockResponse);
  });

  it("handles user with null email and phone", async () => {
    const mockResponse: InvitationAcceptResponse = {
      access_token: "access-token-123",
      token_type: "bearer",
      user: {
        id: "user-123",
        email: null,
        phone: null,
      },
    };

    (client.acceptInvitation as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockResponse,
    );

    const { result } = renderHook(() => useAcceptInvitationMutation(), {
      wrapper: createWrapper(),
    });

    result.current.mutate({ token: "token-123", password: "password123" });

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(result.current.data?.user.email).toBeNull();
    expect(result.current.data?.user.phone).toBeNull();
  });

  it("handles errors correctly", async () => {
    const error = new Error("Invalid token");
    (client.acceptInvitation as ReturnType<typeof vi.fn>).mockRejectedValueOnce(
      error,
    );

    const { result } = renderHook(() => useAcceptInvitationMutation(), {
      wrapper: createWrapper(),
    });

    result.current.mutate({ token: "invalid-token", password: "password123" });

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(result.current.error).toEqual(error);
  });
});
