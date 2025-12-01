"use client";

import { useAuth } from "@/components/AuthProvider";
import { listAddresses } from "@/lib/api";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function AddressesListPage() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();
  const [addresses, setAddresses] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [customerId, setCustomerId] = useState<number | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace("/auth/login");
      return;
    }
    (async () => {
      try {
        // For now, ask user to input customer ID if unknown
        const cid = Number(
          new URLSearchParams(window.location.search).get("customer_id"),
        );
        if (!cid) {
          setError("Provide ?customer_id= in URL to view addresses.");
          return;
        }
        setCustomerId(cid);
        const data = await listAddresses(cid);
        setAddresses(data);
      } catch (e) {
        setError((e as Error).message);
      }
    })();
  }, [isAuthenticated, router]);

  return (
    <main className="mx-auto max-w-3xl px-4 py-8">
      <h1 className="text-2xl font-semibold">Addresses</h1>
      {error && <p className="text-red-600 mt-2">{error}</p>}
      {customerId && (
        <p className="text-sm text-gray-600 mt-1">Customer ID: {customerId}</p>
      )}
      <div className="mt-4 space-y-3">
        {addresses.map((a) => (
          <div key={a.id} className="rounded border p-3">
            <div className="font-medium">
              {a.address_line_1}
              {a.address_line_2 ? `, ${a.address_line_2}` : ""}
            </div>
            <div className="text-sm text-gray-600">
              {a.city}, {a.state} {a.zip_code}
            </div>
            <div className="text-sm mt-1">
              Type: {a.address_type} {a.is_default ? "(default)" : ""}
            </div>
          </div>
        ))}
        {addresses.length === 0 && (
          <div className="text-gray-600">No addresses found.</div>
        )}
      </div>
    </main>
  );
}
