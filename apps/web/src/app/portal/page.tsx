"use client";

import { useAuth } from "@/components/AuthProvider";
import { getAuthHeader, getMyCustomer } from "@/lib/api";
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
    <div className="p-6">
      <h1 className="text-2xl font-semibold">Customer Portal</h1>
      {error && <p className="text-red-600 mt-2">{error}</p>}
      {me ? (
        <div className="mt-3 text-gray-700">
          <p>
            Signed in as <span className="font-medium">{me.email}</span>
          </p>
          {customer ? (
            <p className="text-sm text-gray-600 mt-1">
              Customer ID: {customer.id}
            </p>
          ) : (
            <p className="text-sm text-gray-600 mt-1">
              No customer profile yet.
            </p>
          )}
        </div>
      ) : (
        <p className="text-gray-600 mt-2">Loading your account...</p>
      )}

      <div className="mt-6 grid sm:grid-cols-2 gap-3">
        <a
          href="/portal/customer/new"
          className="rounded border px-4 py-3 hover:bg-gray-50"
        >
          Create customer profile
        </a>
        <a
          href={
            customer
              ? `/portal/addresses?customer_id=${customer.id}`
              : "/portal/addresses"
          }
          className="rounded border px-4 py-3 hover:bg-gray-50"
        >
          View addresses
        </a>
        <a
          href={
            customer
              ? `/portal/addresses/new?customer_id=${customer.id}`
              : "/portal/addresses/new"
          }
          className="rounded border px-4 py-3 hover:bg-gray-50"
        >
          Add address
        </a>
        <a
          href="/portal/orders/new"
          className="rounded border px-4 py-3 hover:bg-gray-50"
        >
          Create order
        </a>
        <a
          href="/portal/orders"
          className="rounded border px-4 py-3 hover:bg-gray-50"
        >
          View orders
        </a>
      </div>
    </div>
  );
}
