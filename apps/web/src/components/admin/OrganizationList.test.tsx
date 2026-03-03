import { describe, it, expect, beforeEach, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { OrganizationList } from "./OrganizationList";

// Unit-test style: mock external state/calls
vi.mock("@/features/organizations/hooks/useOrganizations", () => ({
  useOrganizationsQuery: vi.fn(),
}));

import { useOrganizationsQuery } from "@/features/organizations/hooks/useOrganizations";

function mockOrganizationsQuery(value: {
  data?: unknown;
  isLoading?: boolean;
  error?: Error | null;
}) {
  (useOrganizationsQuery as ReturnType<typeof vi.fn>).mockReturnValue({
    data: value.data,
    isLoading: value.isLoading ?? false,
    error: value.error ?? null,
  });
}

describe("OrganizationList", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders loading state", () => {
    mockOrganizationsQuery({ isLoading: true });
    render(<OrganizationList />);

    // LoadingSpinner has an optional text prop, but OrganizationList doesn't pass it.
    // Assert presence of spinner element by class.
    expect(document.querySelector(".animate-spin")).toBeTruthy();
  });

  it("renders error state", () => {
    mockOrganizationsQuery({ isLoading: false, error: new Error("boom") });
    render(<OrganizationList />);

    expect(
      screen.getByText("Error loading organizations: boom"),
    ).toBeInTheDocument();
  });

  it("renders empty state (no create button when onCreateNew not provided)", () => {
    mockOrganizationsQuery({ data: [], isLoading: false, error: null });
    render(<OrganizationList />);

    expect(screen.getByText("No organizations")).toBeInTheDocument();
    expect(
      screen.getByText("Get started by creating your first organization"),
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /create organization/i }),
    ).not.toBeInTheDocument();
  });

  it("renders empty state with create action and calls onCreateNew", async () => {
    const user = userEvent.setup();
    const onCreateNew = vi.fn();

    mockOrganizationsQuery({ data: [], isLoading: false, error: null });
    render(<OrganizationList onCreateNew={onCreateNew} />);

    const createBtn = screen.getByRole("button", {
      name: /create organization/i,
    });
    await user.click(createBtn);

    expect(onCreateNew).toHaveBeenCalledTimes(1);
  });

  it("renders organizations table and basic interactions don't crash", async () => {
    const user = userEvent.setup();

    mockOrganizationsQuery({
      data: [
        {
          id: "org-1",
          name: "Acme Laundry",
          billingAddress: "123 Main St",
          city: "New York",
          state: "NY",
          postalCode: "10001",
          country: "US",
          contactEmail: null,
          contactPhone: null,
          status: "active",
          createdAt: new Date(),
          updatedAt: new Date(),
        },
      ],
      isLoading: false,
      error: null,
    });

    render(<OrganizationList onCreateNew={vi.fn()} />);

    expect(screen.getByText("Organizations")).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /new organization/i }),
    ).toBeInTheDocument();

    // Table content
    expect(screen.getByText("Acme Laundry")).toBeInTheDocument();
    expect(screen.getByText("New York")).toBeInTheDocument();
    expect(screen.getByText("NY")).toBeInTheDocument();
    expect(screen.getByText("US")).toBeInTheDocument();
    expect(screen.getByText("-")).toBeInTheDocument(); // contactEmail fallback
    expect(screen.getByText("active")).toBeInTheDocument();

    // Click the "View" button (router is mocked globally in test setup).
    await user.click(screen.getByRole("button", { name: /view/i }));
  });
});
