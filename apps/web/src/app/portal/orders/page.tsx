"use client";

import { useAuth } from "@/components/AuthProvider";
import { listOrders } from "@/lib/api";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function OrdersListPage() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();
  const [orders, setOrders] = useState<
    { id: number; order_number: string; status: string; total_amount: number; created_at: string }[]
  >([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace("/auth/login");
      return;
    }
    (async () => {
      try {
        const data = await listOrders();
        setOrders(data);
      } catch (e) {
        setError((e as Error).message);
      }
    })();
  }, [isAuthenticated, router]);

  return (
    <main className="mx-auto max-w-4xl px-4 py-8">
      <h1 className="text-2xl font-semibold">Orders</h1>
      {error && <p className="text-red-600 mt-2">{error}</p>}
      <div className="mt-4 overflow-x-auto">
        <table className="w-full text-sm border">
          <thead className="bg-gray-50">
            <tr>
              <th className="text-left p-2 border-b">Order #</th>
              <th className="text-left p-2 border-b">Status</th>
              <th className="text-left p-2 border-b">Total</th>
              <th className="text-left p-2 border-b">Created</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((o) => (
              <tr key={o.id} className="hover:bg-gray-50">
                <td className="p-2 border-b">{o.order_number}</td>
                <td className="p-2 border-b">{o.status}</td>
                <td className="p-2 border-b">${o.total_amount.toFixed(2)}</td>
                <td className="p-2 border-b">{new Date(o.created_at).toLocaleString()}</td>
              </tr>
            ))}
            {orders.length === 0 && (
              <tr>
                <td className="p-2" colSpan={4}>No orders yet.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </main>
  );
}



