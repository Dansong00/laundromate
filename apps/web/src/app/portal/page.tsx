"use client";

import { useAuth } from "@/components/AuthProvider";
import { getAuthHeader, getMyCustomer } from "@/lib/api";
import { Button, ProgressBar, StatusBadge } from "@/lib/ui";
import { useRouter, usePathname } from "next/navigation";
import { useEffect, useState } from "react";

// Tab Navigation Component
function TabNavigation({
  activeTab,
  onTabChange,
}: {
  activeTab: string;
  onTabChange: (tab: string) => void;
}) {
  const tabs = [
    { id: "home", label: "Home", icon: "🏠" },
    { id: "orders", label: "Orders", icon: "📦" },
    { id: "addresses", label: "Addresses", icon: "📍" },
    { id: "account", label: "Account", icon: "👤" },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-4 py-2 z-50">
      <div className="flex justify-around max-w-md mx-auto">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`flex flex-col items-center py-2 px-3 rounded-lg transition-all duration-200 ${
              activeTab === tab.id
                ? "text-blue-600 bg-blue-50"
                : "text-gray-500 hover:text-gray-700"
            }`}
          >
            <span className="text-xl mb-1">{tab.icon}</span>
            <span className="text-xs font-medium">{tab.label}</span>
          </button>
        ))}
      </div>
    </nav>
  );
}

// Mobile Header Component
function MobileHeader({
  title,
  showBack = false,
}: {
  title: string;
  showBack?: boolean;
}) {
  const router = useRouter();

  return (
    <header className="bg-white border-b border-gray-200 px-4 py-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {showBack && (
            <button
              onClick={() => router.back()}
              className="text-gray-600 hover:text-gray-800"
            >
              ←
            </button>
          )}
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center">
              <span className="text-white text-xs">📍</span>
            </div>
            <span className="font-semibold text-lg">LaundroMate</span>
          </div>
        </div>
        <div className="text-sm text-gray-500">9:41</div>
      </div>
      <h1 className="text-2xl font-bold text-gray-900 mt-4">{title}</h1>
    </header>
  );
}

// Home Tab Component
function HomeTab({ customer }: { customer: any }) {
  const router = useRouter();

  return (
    <div className="mobile-container pb-20">
      {/* Hero Greeting */}
      <div className="pt-6 pb-8 animate-fade-in">
        <h1 className="text-display text-foreground mb-2">
          👋 Hi {customer?.first_name || "there"}
        </h1>
        <p className="text-caption">Ready for fresh, clean laundry?</p>
      </div>

      {/* Primary CTA */}
      <div className="mb-8 animate-bounce-in">
        <Button
          onClick={() => router.push("/portal/orders/new")}
          className="w-full h-16 text-lg font-semibold bg-blue-600 hover:bg-blue-700 text-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
        >
          New Order
        </Button>
      </div>

      {/* Secondary CTA */}
      <div className="mb-8 animate-slide-up">
        <Button
          variant="ghost"
          onClick={() => router.push("/portal/orders")}
          className="w-full h-12 text-blue-600 hover:bg-blue-50 rounded-xl border border-blue-200"
        >
          Track Order →
        </Button>
      </div>

      {/* Active Order Card */}
      <div className="mb-6 animate-slide-up">
        <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
          <h3 className="text-title text-foreground mb-4">Active Order</h3>

          <div className="space-y-4">
            <div>
              <p className="text-subtitle font-semibold text-foreground">
                Wash & Fold
              </p>
              <p className="text-caption">
                Estimated Delivery: Tomorrow, 10:00 AM
              </p>
            </div>

            {/* Progress Bar */}
            <div className="space-y-2">
              <ProgressBar progress={35} showIndicator>
                <div className="flex justify-between text-xs text-gray-500">
                  <span className="text-blue-600 font-medium">In Progress</span>
                  <span>Out for Delivery</span>
                  <span>Delivered</span>
                </div>
              </ProgressBar>
            </div>
          </div>
        </div>
      </div>

      {/* Past Orders Link */}
      <div className="animate-slide-up">
        <Button
          variant="link"
          onClick={() => router.push("/portal/orders")}
          className="text-blue-600 hover:text-blue-700 p-0 h-auto"
        >
          Past Orders →
        </Button>
      </div>
    </div>
  );
}

// Orders Tab Component
function OrdersTab() {
  const router = useRouter();

  // Mock order data
  const orders = [
    {
      id: 1,
      type: "Wash & Fold",
      date: "April 20",
      status: "in-progress" as const,
      statusLabel: "In Progress",
    },
    {
      id: 2,
      type: "Wash & Fold",
      date: "April 20",
      status: "out-for-delivery" as const,
      statusLabel: "Out for Delivery",
    },
    {
      id: 3,
      type: "Wash & Fold",
      date: "April 15",
      status: "completed" as const,
      statusLabel: "Delivered",
    },
    {
      id: 4,
      type: "Wash & Fold",
      date: "April 10",
      status: "default" as const,
      statusLabel: "Processing",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <MobileHeader title="My Orders" showBack />

      <div className="mobile-container pt-4">
        {/* Filter/Sort */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <select className="text-sm border border-gray-300 rounded-lg px-3 py-2 bg-white">
              <option>All</option>
              <option>Active</option>
              <option>Completed</option>
            </select>
          </div>
          <button className="text-gray-500 hover:text-gray-700">
            <span className="text-lg">☰</span>
          </button>
        </div>

        {/* Orders List */}
        <div className="space-y-4">
          {orders.map((order) => (
            <div
              key={order.id}
              className="bg-white rounded-xl border border-gray-200 p-4 shadow-sm"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-lg font-semibold text-gray-900">
                      {order.type}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600">{order.date}</p>
                </div>
                <StatusBadge variant={order.status}>
                  {order.statusLabel}
                </StatusBadge>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// Addresses Tab Component
function AddressesTab({ customer }: { customer: any }) {
  const router = useRouter();

  // Mock address data
  const addresses = [
    {
      id: 1,
      name: "Dee",
      street: "123 Main St",
      city: "Anytown, NY 12345",
    },
    {
      id: 2,
      street: "456 Elm St",
      city: "Anytown, NY 12345",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <MobileHeader title="Saved Addresses" showBack />

      <div className="mobile-container pt-4">
        {/* Addresses List */}
        <div className="space-y-4 mb-6">
          {addresses.map((address) => (
            <div
              key={address.id}
              className="bg-white rounded-xl border border-gray-200 p-4 shadow-sm"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  {address.name && (
                    <p className="font-semibold text-gray-900 mb-1">
                      {address.name}
                    </p>
                  )}
                  <p className="text-gray-900">{address.street}</p>
                  <p className="text-gray-600">{address.city}</p>
                </div>
                <button className="text-gray-500 hover:text-gray-700 text-sm">
                  Edit
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Add Address Button */}
        <Button
          onClick={() => router.push("/portal/addresses/new")}
          className="w-full h-14 text-lg font-semibold bg-blue-600 hover:bg-blue-700 text-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-200"
        >
          + Add Address
        </Button>
      </div>
    </div>
  );
}

// Account Tab Component
function AccountTab({ me, customer }: { me: any; customer: any }) {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <MobileHeader title="My Account" showBack />

      <div className="mobile-container pt-4">
        {/* Profile Section */}
        <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm mb-4">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Profile</h3>
          <div className="space-y-3">
            <div>
              <p className="text-sm text-gray-500">Name</p>
              <p className="font-medium text-gray-900">
                {customer?.first_name || "Dee"}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Email</p>
              <p className="font-medium text-gray-900">
                {me?.email || "dee@example.com"}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Phone</p>
              <p className="font-medium text-gray-900">123-456-7890</p>
            </div>
          </div>
        </div>

        {/* Notifications Section */}
        <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm mb-4">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Notifications
          </h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-gray-900">SMS Notifications</span>
              <div className="w-12 h-6 bg-blue-600 rounded-full relative">
                <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full"></div>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-900">Email Notifications</span>
              <div className="w-12 h-6 bg-blue-600 rounded-full relative">
                <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full"></div>
              </div>
            </div>
          </div>
        </div>

        {/* Security Section */}
        <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm mb-4">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Security</h3>
          <button className="text-blue-600 hover:text-blue-700 text-left">
            Change Password
          </button>
        </div>

        {/* Legal Links */}
        <div className="space-y-2">
          <button className="text-gray-600 hover:text-gray-800 text-sm">
            Terms of Service
          </button>
          <button className="text-gray-600 hover:text-gray-800 text-sm">
            Privacy Policy
          </button>
        </div>
      </div>
    </div>
  );
}

export default function PortalPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();
  const [me, setMe] = useState<any | null>(null);
  const [customer, setCustomer] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState("home");

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace("/auth/login");
      return;
    }
    (async () => {
      try {
        const res = await fetch("/api/me", {
          headers: {
            ...getAuthHeader(),
          },
          cache: "no-store",
        });
        if (!res.ok) throw new Error("Failed to fetch profile");
        const data = await res.json();
        setMe(data);
        try {
          const c = await getMyCustomer();
          setCustomer(c);
        } catch (_) {
          // ignore if customer not found
        }
      } catch (e) {
        setError((e as Error).message);
      }
    })();
  }, [isAuthenticated, router]);

  if (!isAuthenticated) return null;

  const renderActiveTab = () => {
    switch (activeTab) {
      case "home":
        return <HomeTab customer={customer} />;
      case "orders":
        return <OrdersTab />;
      case "addresses":
        return <AddressesTab customer={customer} />;
      case "account":
        return <AccountTab me={me} customer={customer} />;
      default:
        return <HomeTab customer={customer} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {error && (
        <div className="mobile-container pt-4">
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
            <p className="text-red-800 text-sm">{error}</p>
          </div>
        </div>
      )}

      {!me ? (
        <div className="mobile-container pt-20">
          <div className="flex items-center justify-center py-8">
            <div className="text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p className="text-caption">Loading your account...</p>
            </div>
          </div>
        </div>
      ) : (
        <>
          {renderActiveTab()}
          <TabNavigation activeTab={activeTab} onTabChange={setActiveTab} />
        </>
      )}
    </div>
  );
}
