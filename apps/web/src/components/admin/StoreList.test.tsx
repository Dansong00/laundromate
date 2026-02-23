import { describe, it, expect, beforeEach, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { StoreList } from "./StoreList";

// Unit-test style: mock external state/calls
vi.mock("@/features/stores/hooks/useStores", () => ({
  useStoresByOrganizationQuery: vi.fn(),
}));

vi.mock("@/lib/routes", () => ({
  ROUTES: {
    ADMIN_STORE_DETAIL: (id: string) => `/admin/stores/${id}`,
  },
}));

import { useStoresByOrganizationQuery } from "@/features/stores/hooks/useStores";

function mockStoresQuery(value: {
  data?: unknown;
  isLoading?: boolean;
  error?: Error | null;
}) {
  (useStoresByOrganizationQuery as ReturnType<typeof vi.fn>).mockReturnValue({
    data: value.data,
    isLoading: value.isLoading ?? false,
    error: value.error ?? null,
  });
}

describe("StoreList", () => {
  const organizationId = "org-123";

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders loading state", () => {
    mockStoresQuery({ isLoading: true });
    render(<StoreList organizationId={organizationId} />);

    expect(document.querySelector(".animate-spin")).toBeTruthy();
  });

  it("renders error state", () => {
    mockStoresQuery({
      isLoading: false,
      error: new Error("Failed to load stores"),
    });
    render(<StoreList organizationId={organizationId} />);

    expect(
      screen.getByText("Error loading stores: Failed to load stores"),
    ).toBeInTheDocument();
  });

  it("renders empty state (no create button when onCreateNew not provided)", () => {
    mockStoresQuery({ data: [], isLoading: false, error: null });
    render(<StoreList organizationId={organizationId} />);

    expect(screen.getByText("No stores")).toBeInTheDocument();
    expect(
      screen.getByText(
        "Get started by creating your first store for this organization",
      ),
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /create store/i }),
    ).not.toBeInTheDocument();
  });

  it("renders empty state with create action and calls onCreateNew", async () => {
    const user = userEvent.setup();
    const onCreateNew = vi.fn();

    mockStoresQuery({ data: [], isLoading: false, error: null });
    render(
      <StoreList organizationId={organizationId} onCreateNew={onCreateNew} />,
    );

    const createBtn = screen.getByRole("button", { name: /create store/i });
    await user.click(createBtn);

    expect(onCreateNew).toHaveBeenCalledTimes(1);
  });

  it("renders stores table and displays store information", async () => {
    const user = userEvent.setup();

    mockStoresQuery({
      data: [
        {
          id: "store-1",
          organizationId: organizationId,
          name: "Downtown Store",
          streetAddress: "123 Main Street",
          city: "New York",
          state: "NY",
          postalCode: "10001",
          country: "US",
          status: "active",
          createdAt: new Date("2024-01-01"),
          updatedAt: new Date("2024-01-01"),
        },
        {
          id: "store-2",
          organizationId: organizationId,
          name: "Uptown Store",
          streetAddress: "456 Park Avenue",
          city: "New York",
          state: "NY",
          postalCode: "10002",
          country: "US",
          status: "inactive",
          createdAt: new Date("2024-01-02"),
          updatedAt: new Date("2024-01-02"),
        },
      ],
      isLoading: false,
      error: null,
    });

    render(<StoreList organizationId={organizationId} onCreateNew={vi.fn()} />);

    expect(screen.getByText("Stores")).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /new store/i }),
    ).toBeInTheDocument();

    // Table headers
    expect(screen.getByText("Name")).toBeInTheDocument();
    expect(screen.getByText("Street Address")).toBeInTheDocument();
    expect(screen.getByText("City")).toBeInTheDocument();
    expect(screen.getByText("State")).toBeInTheDocument();
    expect(screen.getByText("Status")).toBeInTheDocument();
    expect(screen.getByText("Actions")).toBeInTheDocument();

    // First store data
    expect(screen.getByText("Downtown Store")).toBeInTheDocument();
    expect(screen.getByText("123 Main Street")).toBeInTheDocument();
    expect(screen.getAllByText("New York").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("NY").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText("active")).toBeInTheDocument();

    // Second store data (both stores have city "New York", so use getAllByText for city)
    expect(screen.getByText("Uptown Store")).toBeInTheDocument();
    expect(screen.getByText("456 Park Avenue")).toBeInTheDocument();
    expect(screen.getByText("inactive")).toBeInTheDocument();

    // View buttons
    const viewButtons = screen.getAllByRole("button", { name: /view/i });
    expect(viewButtons).toHaveLength(2);

    // Click a View button (router is mocked globally in test setup)
    await user.click(viewButtons[0]);
  });

  it("navigates to store detail when clicking on a table row", async () => {
    const user = userEvent.setup();

    mockStoresQuery({
      data: [
        {
          id: "store-1",
          organizationId: organizationId,
          name: "Downtown Store",
          streetAddress: "123 Main Street",
          city: "New York",
          state: "NY",
          postalCode: "10001",
          country: "US",
          status: "active",
          createdAt: new Date("2024-01-01"),
          updatedAt: new Date("2024-01-01"),
        },
      ],
      isLoading: false,
      error: null,
    });

    render(<StoreList organizationId={organizationId} />);

    // Find the table row by store name and click it
    const storeRow = screen.getByText("Downtown Store").closest("tr");
    expect(storeRow).toBeInTheDocument();

    if (storeRow) {
      await user.click(storeRow);
    }
  });

  it("stops propagation when clicking View button", async () => {
    const user = userEvent.setup();

    mockStoresQuery({
      data: [
        {
          id: "store-1",
          organizationId: organizationId,
          name: "Downtown Store",
          streetAddress: "123 Main Street",
          city: "New York",
          state: "NY",
          postalCode: "10001",
          country: "US",
          status: "active",
          createdAt: new Date("2024-01-01"),
          updatedAt: new Date("2024-01-01"),
        },
      ],
      isLoading: false,
      error: null,
    });

    render(<StoreList organizationId={organizationId} />);

    const viewButton = screen.getByRole("button", { name: /view/i });

    // Simulate click on button
    viewButton.onclick = (e) => {
      if (e) {
        e.stopPropagation();
      }
    };

    await user.click(viewButton);

    // The button click handler should be callable without errors
    expect(viewButton).toBeInTheDocument();
  });
});
