"use client";

import { useAuth } from "@/components/AuthProvider";
import { CustomerRead, getMe, getMyCustomer, UserRead } from "@/lib/api";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

// Import Figma components
import { Home } from "@/components/Home";
import { MyOrders } from "@/components/MyOrders";
import { SavedAddresses } from "@/components/SavedAddresses";
import { MyAccount } from "@/components/MyAccount";
import { BottomNavigation } from "@/components/BottomNavigation";

export default function PortalPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();
  const [me, setMe] = useState<UserRead | null>(null);
  const [, setCustomer] = useState<CustomerRead | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState("home");

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace("/auth/login");
      return;
    }
    (async () => {
      setError(null);
      try {
        const data = await getMe();
        setMe(data);
        try {
          const c = await getMyCustomer();
          setCustomer(c);
        } catch {
          // ignore if customer not found
        }
      } catch (e) {
        setError((e as Error).message ?? "Failed to fetch profile");
      }
    })();
  }, [isAuthenticated, router]);

  if (!isAuthenticated) return null;

  const handleNewOrder = () => {
    router.push("/portal/orders/new");
  };

  const renderActiveTab = () => {
    switch (activeTab) {
      case "home":
        return <Home onNewOrder={handleNewOrder} />;
      case "orders":
        return <MyOrders />;
      case "addresses":
        return <SavedAddresses />;
      case "account":
        return <MyAccount />;
      default:
        return <Home onNewOrder={handleNewOrder} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {error && (
        <div className="px-4 pt-4">
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
            <p className="text-red-800 text-sm">{error}</p>
          </div>
        </div>
      )}

      {error ? null : !me ? (
        <div className="flex items-center justify-center py-8">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-sm text-gray-500">Loading your account...</p>
          </div>
        </div>
      ) : (
        <>
          {renderActiveTab()}
          <BottomNavigation activeTab={activeTab} setActiveTab={setActiveTab} />
        </>
      )}
    </div>
  );
}
