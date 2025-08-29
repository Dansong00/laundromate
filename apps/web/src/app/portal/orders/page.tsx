"use client";

import { useAuth } from "@/components/AuthProvider";
import { listOrders } from "@/lib/api";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  EmptyState,
  LoadingSpinner,
  Select,
  StatusBadge,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@laundromate/ui";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function OrdersListPage() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();
  const [orders, setOrders] = useState<
    {
      id: number;
      order_number: string;
      status: string;
      total_amount: number;
      created_at: string;
    }[]
  >([]);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState<number | null>(null);

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

  async function updateStatus(orderId: number, status: string) {
    try {
      setSaving(orderId);
      const res = await fetch(`/api/orders/${orderId}/status`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status }),
      });
      if (!res.ok) throw new Error("Failed to update status");
      const updated = await res.json();
      setOrders((arr) =>
        arr.map((o) =>
          o.id === orderId ? { ...o, status: updated.status } : o
        )
      );
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setSaving(null);
    }
  }

  return (
    <main className="mx-auto max-w-6xl px-4 py-8">
      <Card>
        <CardHeader>
          <CardTitle>Orders</CardTitle>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800">
              {error}
            </div>
          )}

          {orders.length === 0 ? (
            <EmptyState
              title="No Orders Yet"
              description="Orders you create will appear here."
              icon="📦"
            />
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Order #</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Total</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {orders.map((o) => (
                  <TableRow key={o.id}>
                    <TableCell>
                      <a
                        className="text-blue-600 hover:text-blue-800 underline font-medium"
                        href={`/portal/orders/${o.id}`}
                      >
                        {o.order_number}
                      </a>
                    </TableCell>
                    <TableCell>
                      <StatusBadge status={o.status as any} showIcon />
                    </TableCell>
                    <TableCell className="font-medium">
                      ${o.total_amount.toFixed(2)}
                    </TableCell>
                    <TableCell>
                      {new Date(o.created_at).toLocaleString()}
                    </TableCell>
                    <TableCell>
                      <Select
                        value={o.status}
                        onChange={(value) => updateStatus(o.id, value)}
                        disabled={saving === o.id}
                        options={[
                          { value: "pending", label: "Pending" },
                          { value: "confirmed", label: "Confirmed" },
                          { value: "picked_up", label: "Picked Up" },
                          { value: "in_progress", label: "In Progress" },
                          { value: "ready", label: "Ready" },
                          {
                            value: "out_for_delivery",
                            label: "Out for Delivery",
                          },
                          { value: "delivered", label: "Delivered" },
                          { value: "cancelled", label: "Cancelled" },
                        ]}
                      />
                      {saving === o.id && (
                        <LoadingSpinner size="sm" className="ml-2" />
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </main>
  );
}
