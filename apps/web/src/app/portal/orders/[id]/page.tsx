"use client";

import { useAuth } from "@/components/AuthProvider";
import { OrderDetailRead } from "@/lib/api";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function OrderDetailPage({
  params,
}: {
  params: { id: string };
}) {
  const { isAuthenticated } = useAuth();
  const router = useRouter();
  const [order, setOrder] = useState<OrderDetailRead | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace("/auth/login");
      return;
    }
    (async () => {
      try {
        const res = await fetch(`/api/orders/${params.id}/detail`, {
          cache: "no-store",
        });
        if (!res.ok) throw new Error("Failed to load order");
        const data = await res.json();
        setOrder(data);
      } catch (e) {
        setError((e as Error).message);
      }
    })();
  }, [isAuthenticated, params.id, router]);

  return (
    <main className="mx-auto max-w-3xl px-4 py-8">
      <h1 className="text-2xl font-semibold">Order detail</h1>
      {error && <p className="text-red-600 mt-2">{error}</p>}
      {!order ? (
        <p className="text-gray-600 mt-2">Loading…</p>
      ) : (
        <div className="mt-4 space-y-4">
          <div className="rounded border p-4">
            <div className="font-medium">{order.order_number}</div>
            <div className="text-sm text-gray-600">
              Status: {order.status} • Total: $
              {order.total_amount?.toFixed?.(2)}
            </div>
            <div className="text-sm text-gray-600">
              Pickup: {new Date(order.pickup_date).toLocaleString()} at{" "}
              {order.pickup_time_slot}
            </div>
            <div className="text-sm text-gray-600">
              Delivery: {new Date(order.delivery_date).toLocaleString()} at{" "}
              {order.delivery_time_slot}
            </div>
          </div>
          <div className="rounded border p-4">
            <div className="font-medium mb-2">Items</div>
            <table className="w-full text-sm">
              <thead>
                <tr>
                  <th className="text-left p-1">Name</th>
                  <th className="text-left p-1">Type</th>
                  <th className="text-left p-1">Qty</th>
                  <th className="text-left p-1">Unit</th>
                  <th className="text-left p-1">Total</th>
                </tr>
              </thead>
              <tbody>
                {order.items?.map((it) => (
                  <tr key={it.id}>
                    <td className="p-1">{it.item_name}</td>
                    <td className="p-1">{it.item_type}</td>
                    <td className="p-1">{it.quantity}</td>
                    <td className="p-1">${it.unit_price?.toFixed?.(2)}</td>
                    <td className="p-1">${it.total_price?.toFixed?.(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </main>
  );
}
