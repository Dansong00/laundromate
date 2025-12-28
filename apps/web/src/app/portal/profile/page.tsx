"use client";

import { useAuth } from "@/components/AuthProvider";
import {
  AddressRead,
  CustomerRead,
  getAuthHeader,
  getMyCustomer,
  listAddresses,
  UserRead,
} from "@/lib/api";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function ProfilePage() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();
  const [me, setMe] = useState<UserRead | null>(null);
  const [customer, setCustomer] = useState<CustomerRead | null>(null);
  const [addresses, setAddresses] = useState<AddressRead[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace("/auth/login");
      return;
    }
    (async () => {
      try {
        const res = await fetch("/api/me", {
          headers: { ...getAuthHeader() },
          cache: "no-store",
        });
        if (!res.ok) throw new Error("Failed to load user");
        const data = await res.json();
        setMe(data);
        try {
          const c = await getMyCustomer();
          setCustomer(c);
          const addrs = await listAddresses(c.id);
          setAddresses(addrs);
        } catch {
          // ignore
        }
      } catch (e) {
        setError((e as Error).message);
      }
    })();
  }, [isAuthenticated, router]);

  return (
    <main className="mx-auto max-w-3xl px-4 py-8">
      <h1 className="text-2xl font-semibold">My profile</h1>
      {error && <p className="text-red-600 mt-2">{error}</p>}
      {me && (
        <div className="mt-4 rounded border p-4">
          <div className="font-medium">{me.email}</div>
          <div className="text-sm text-gray-600">
            {me.first_name} {me.last_name}
          </div>
        </div>
      )}
      {customer && (
        <div className="mt-4 rounded border p-4">
          <div className="font-medium">Customer</div>
          <div className="text-sm text-gray-600">ID: {customer.id}</div>
        </div>
      )}
      {addresses.length > 0 && (
        <div className="mt-4 rounded border p-4">
          <div className="font-medium mb-2">Addresses</div>
          <ul className="space-y-2">
            {addresses.map((a) => (
              <li key={a.id} className="text-sm">
                {a.address_line_1}
                {a.address_line_2 ? `, ${a.address_line_2}` : ""} — {a.city},{" "}
                {a.state} {a.zip_code} {a.is_default ? "(default)" : ""}
              </li>
            ))}
          </ul>
        </div>
      )}
    </main>
  );
}
