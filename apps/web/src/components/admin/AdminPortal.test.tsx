import { describe, it, expect, beforeEach, vi } from "vitest";
import { screen } from "@testing-library/react";
import { AdminPortal } from "./AdminPortal";
import { renderWithProviders } from "@/__tests__/test-utils";

// Mock dependencies
vi.mock("@/components/AuthProvider", () => ({
  useAuth: () => ({
    logout: vi.fn(),
  }),
}));

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    prefetch: vi.fn(),
    back: vi.fn(),
  }),
}));

vi.mock("./AdminUsers", () => ({
  AdminUsers: () => <div data-testid="admin-users">AdminUsers Component</div>,
}));

vi.mock("@/lib/routes", () => ({
  ROUTES: {
    ADMIN: "/admin",
    LOGIN: "/auth/login",
  },
}));

describe("AdminPortal", () => {
  const mockUser = {
    id: "user-123",
    email: "admin@example.com",
    first_name: "John",
    last_name: "Doe",
    phone: "+1234567890",
    is_active: true,
    is_admin: true,
    is_super_admin: true,
    is_support_agent: false,
    is_provisioning_specialist: false,
    created_at: new Date(),
    updated_at: new Date(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders the portal with header", () => {
    renderWithProviders(<AdminPortal currentUser={mockUser} />);

    expect(screen.getByText("Admin Portal")).toBeInTheDocument();
    expect(
      screen.getByText("User Access Provisioning & Management"),
    ).toBeInTheDocument();
  });

  it("displays current user name when provided", () => {
    renderWithProviders(<AdminPortal currentUser={mockUser} />);

    expect(screen.getByText("John Doe")).toBeInTheDocument();
  });

  it("does not display user name when currentUser is null", () => {
    renderWithProviders(<AdminPortal currentUser={null} />);

    expect(screen.queryByText("John Doe")).not.toBeInTheDocument();
  });

  it("does not display user name when currentUser is undefined", () => {
    renderWithProviders(<AdminPortal />);

    expect(screen.queryByText("John Doe")).not.toBeInTheDocument();
  });

  it("renders AdminUsers component by default", () => {
    renderWithProviders(<AdminPortal currentUser={mockUser} />);

    expect(screen.getByTestId("admin-users")).toBeInTheDocument();
  });

  it("renders User Management sidebar button", () => {
    renderWithProviders(<AdminPortal currentUser={mockUser} />);

    expect(screen.getByText("User Management")).toBeInTheDocument();
  });

  it("has active styling on User Management button by default", () => {
    renderWithProviders(<AdminPortal currentUser={mockUser} />);

    const userManagementButton =
      screen.getByText("User Management").parentElement;
    expect(userManagementButton).toHaveClass("bg-black", "text-white");
  });

  it("renders Admin Dashboard button", () => {
    renderWithProviders(<AdminPortal currentUser={mockUser} />);

    expect(
      screen.getByRole("button", { name: /admin dashboard/i }),
    ).toBeInTheDocument();
  });

  it("renders Logout button", () => {
    renderWithProviders(<AdminPortal currentUser={mockUser} />);

    expect(screen.getByRole("button", { name: /logout/i })).toBeInTheDocument();
  });

  it("renders Admin Access info card", () => {
    renderWithProviders(<AdminPortal currentUser={mockUser} />);

    expect(screen.getByText("Admin Access")).toBeInTheDocument();
    expect(
      screen.getByText(
        "You have full access to provision and manage user accounts, including admin privileges.",
      ),
    ).toBeInTheDocument();
    expect(screen.getByText("Highest permission level")).toBeInTheDocument();
  });

  it("displays user with only first name when last name is missing", () => {
    const userWithoutLastName = {
      ...mockUser,
      last_name: null,
    };

    renderWithProviders(<AdminPortal currentUser={userWithoutLastName} />);

    expect(screen.getByText("John")).toBeInTheDocument();
    expect(screen.queryByText("John Doe")).not.toBeInTheDocument();
  });

  it("displays user with only first name when last name is empty string", () => {
    const userWithEmptyLastName = {
      ...mockUser,
      last_name: "",
    };

    renderWithProviders(<AdminPortal currentUser={userWithEmptyLastName} />);

    expect(screen.getByText("John")).toBeInTheDocument();
    expect(screen.queryByText("John Doe")).not.toBeInTheDocument();
  });
});
