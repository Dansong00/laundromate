import { describe, it, expect, beforeEach, vi } from "vitest";
import { validateInvitation, acceptInvitation } from "./client";
import type {
  InvitationValidateResponse,
  InvitationAcceptResponse,
} from "./client";
import * as apiClient from "@/lib/api/client";

// Mock the apiFetch function
vi.mock("@/lib/api/client", () => ({
  apiFetch: vi.fn(),
}));

describe("validateInvitation", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls apiFetch with correct path", async () => {
    const mockResponse: InvitationValidateResponse = {
      valid: true,
      email: "test@example.com",
      organizationId: "org-123",
      organizationName: "Test Org",
      organizationRole: "owner",
    };

    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockResponse,
    );

    const result = await validateInvitation("token-123");

    expect(apiClient.apiFetch).toHaveBeenCalledWith<[string]>(
      "/auth/invitations/token-123/validate",
    );
    expect(result).toEqual(mockResponse);
  });

  it("returns invalid invitation response", async () => {
    const mockResponse: InvitationValidateResponse = {
      valid: false,
      reason: "Token expired",
    };

    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockResponse,
    );

    const result = await validateInvitation("expired-token");

    expect(result).toEqual(mockResponse);
    expect(result.valid).toBe(false);
    expect(result.reason).toBe("Token expired");
  });

  it("handles null values in response", async () => {
    const mockResponse: InvitationValidateResponse = {
      valid: true,
      email: null,
      organizationId: null,
      organizationName: null,
      organizationRole: null,
      reason: null,
    };

    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockResponse,
    );

    const result = await validateInvitation("token-123");

    expect(result).toEqual(mockResponse);
  });

  it("propagates errors from apiFetch", async () => {
    const error = new Error("Network error");
    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(
      error,
    );

    await expect(validateInvitation("token-123")).rejects.toThrow(
      "Network error",
    );
  });
});

describe("acceptInvitation", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("calls apiFetch with correct path, method, and body", async () => {
    const mockResponse: InvitationAcceptResponse = {
      access_token: "access-token-123",
      token_type: "bearer",
      user: {
        id: "user-123",
        email: "test@example.com",
        phone: "+1234567890",
      },
    };

    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockResponse,
    );

    const result = await acceptInvitation("token-123", "password123");

    expect(apiClient.apiFetch).toHaveBeenCalledWith(
      "/auth/invitations/token-123/accept",
      {
        method: "POST",
        body: JSON.stringify({ password: "password123" }),
      },
    );
    expect(result).toEqual(mockResponse);
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

    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockResponse,
    );

    const result = await acceptInvitation("token-123", "password123");

    expect(result.user.email).toBeNull();
    expect(result.user.phone).toBeNull();
  });

  it("propagates errors from apiFetch", async () => {
    const error = new Error("Invalid token");
    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(
      error,
    );

    await expect(
      acceptInvitation("invalid-token", "password123"),
    ).rejects.toThrow("Invalid token");
  });

  it("serializes password correctly in request body", async () => {
    const mockResponse: InvitationAcceptResponse = {
      access_token: "access-token-123",
      token_type: "bearer",
      user: {
        id: "user-123",
      },
    };

    (apiClient.apiFetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      mockResponse,
    );

    await acceptInvitation("token-123", "secure-password-123");

    const callArgs = (apiClient.apiFetch as ReturnType<typeof vi.fn>).mock
      .calls[0];
    expect(callArgs[1]?.body).toBe(
      JSON.stringify({ password: "secure-password-123" }),
    );
  });
});
