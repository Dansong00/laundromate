"use client";

import { useAuth } from "@/components/AuthProvider";
import { getAuthHeader, getMyCustomer } from "@/lib/api";
import {
  Alert,
  AlertDescription,
  Button,
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  LoadingSpinner,
} from "@laundromate/ui";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function PortalPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();
  const [me, setMe] = useState<any | null>(null);
  const [customer, setCustomer] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);

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

  return (
    <main className="mx-auto max-w-6xl px-4 py-8">
      <Card>
        <CardHeader>
          <CardTitle className="text-3xl">Customer Portal</CardTitle>
        </CardHeader>
        <CardContent>
          {error && (
            <Alert variant="destructive" className="mb-6">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {!me ? (
            <div className="flex items-center justify-center py-8">
              <LoadingSpinner size="lg" text="Loading your account..." />
            </div>
          ) : (
            <>
              <div className="mb-8 p-6 bg-blue-50 border border-blue-200 rounded-lg">
                <h2 className="text-lg font-semibold text-blue-900 mb-2">
                  Account Information
                </h2>
                <p className="text-blue-800">
                  Signed in as <span className="font-medium">{me.email}</span>
                </p>
                {customer ? (
                  <p className="text-sm text-blue-700 mt-1">
                    Customer ID:{" "}
                    <span className="font-mono bg-blue-100 px-2 py-1 rounded">
                      {customer.id}
                    </span>
                  </p>
                ) : (
                  <p className="text-sm text-blue-700 mt-1">
                    No customer profile yet. Create one to get started!
                  </p>
                )}
              </div>

              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <Card
                  variant="outlined"
                  className="hover:shadow-md transition-shadow"
                >
                  <CardContent className="p-6">
                    <h3 className="font-semibold text-lg mb-2">
                      Customer Profile
                    </h3>
                    <p className="text-gray-600 text-sm mb-4">
                      {customer
                        ? "Manage your profile and preferences"
                        : "Create your customer profile to get started"}
                    </p>
                    <Button
                      variant={customer ? "outline" : "default"}
                      className="w-full"
                      onClick={() => router.push("/portal/customer/new")}
                    >
                      {customer ? "Edit Profile" : "Create Profile"}
                    </Button>
                  </CardContent>
                </Card>

                <Card
                  variant="outlined"
                  className="hover:shadow-md transition-shadow"
                >
                  <CardContent className="p-6">
                    <h3 className="font-semibold text-lg mb-2">Addresses</h3>
                    <p className="text-gray-600 text-sm mb-4">
                      Manage pickup and delivery addresses
                    </p>
                    <div className="space-y-2">
                      <Button
                        variant="outline"
                        size="sm"
                        className="w-full"
                        onClick={() =>
                          router.push(
                            customer
                              ? `/portal/addresses?customer_id=${customer.id}`
                              : "/portal/addresses"
                          )
                        }
                      >
                        View Addresses
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        className="w-full"
                        onClick={() =>
                          router.push(
                            customer
                              ? `/portal/addresses/new?customer_id=${customer.id}`
                              : "/portal/addresses/new"
                          )
                        }
                      >
                        Add Address
                      </Button>
                    </div>
                  </CardContent>
                </Card>

                <Card
                  variant="outlined"
                  className="hover:shadow-md transition-shadow"
                >
                  <CardContent className="p-6">
                    <h3 className="font-semibold text-lg mb-2">Orders</h3>
                    <p className="text-gray-600 text-sm mb-4">
                      Create and track your laundry orders
                    </p>
                    <div className="space-y-2">
                      <Button
                        variant="default"
                        size="sm"
                        className="w-full"
                        onClick={() => router.push("/portal/orders/new")}
                      >
                        Create Order
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        className="w-full"
                        onClick={() => router.push("/portal/orders")}
                      >
                        View Orders
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </>
          )}
        </CardContent>
      </Card>
    </main>
  );
}
