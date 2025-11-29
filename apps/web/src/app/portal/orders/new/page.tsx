"use client";

import { useAuth } from "@/components/AuthProvider";
import { useToast } from "@/components/ToastProvider";
import {
  createOrder,
  getAuthHeader,
  listAddresses,
  listServices,
} from "@/lib/api";
import {
  Alert,
  AlertDescription,
  Button,
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  Input,
  LoadingSpinner,
  Select,
} from "@/lib/ui";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function NewOrderPage() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();
  const { notifySuccess, notifyError } = useToast();
  const [services, setServices] = useState<
    { id: number; name: string; base_price: number }[]
  >([]);
  const [addresses, setAddresses] = useState<any[]>([]);
  const [form, setForm] = useState({
    customer_id: 0,
    pickup_address_id: 0,
    delivery_address_id: 0,
    pickup_date: "",
    pickup_time_slot: "",
    delivery_date: "",
    delivery_time_slot: "",
  });
  const [items, setItems] = useState([
    { service_id: 0, item_name: "", item_type: "", quantity: 1, unit_price: 0 },
  ]);
  const [loading, setLoading] = useState(false);
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
        if (!res.ok) throw new Error("Not authenticated");
        const svc = await listServices();
        setServices(svc);
      } catch (e) {
        setError((e as Error).message);
      }
    })();
  }, [isAuthenticated, router]);

  useEffect(() => {
    async function refreshAddresses() {
      if (!form.customer_id) {
        setAddresses([]);
        return;
      }
      try {
        const data = await listAddresses(Number(form.customer_id));
        setAddresses(data);
      } catch (e) {
        setError((e as Error).message);
      }
    }
    refreshAddresses();
  }, [form.customer_id]);

  function updateField<K extends keyof typeof form>(k: K, v: string | number) {
    setForm((f) => ({ ...f, [k]: v }));
  }

  function updateItem(
    index: number,
    key: keyof (typeof items)[number],
    value: string | number
  ) {
    setItems((arr) =>
      arr.map((it, i) => (i === index ? { ...it, [key]: value } : it))
    );
  }

  function addItem() {
    setItems((arr) => [
      ...arr,
      {
        service_id: 0,
        item_name: "",
        item_type: "",
        quantity: 1,
        unit_price: 0,
      },
    ]);
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await createOrder({
        ...form,
        items,
      } as any);
      notifySuccess("Order created");
      router.push("/portal/orders");
    } catch (e) {
      const msg = (e as Error).message;
      setError(msg);
      notifyError(msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-4xl px-4 py-8">
      <Card>
        <CardHeader>
          <CardTitle>Create New Order</CardTitle>
        </CardHeader>
        <CardContent>
          {error && (
            <Alert variant="destructive" className="mb-6">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-2 gap-3">
              <Input
                label="Customer ID"
                type="number"
                value={form.customer_id}
                onChange={(e) =>
                  updateField("customer_id", Number(e.target.value))
                }
              />
              <Select
                label="Pickup Address"
                value={form.pickup_address_id.toString()}
                onChange={(value) =>
                  updateField("pickup_address_id", Number(value))
                }
                options={[
                  { value: "0", label: "Select address" },
                  ...addresses.map((a) => ({
                    value: a.id.toString(),
                    label: `${a.address_line_1}, ${a.city}`,
                  })),
                ]}
              />
              <Select
                label="Delivery Address"
                value={form.delivery_address_id.toString()}
                onChange={(value) =>
                  updateField("delivery_address_id", Number(value))
                }
                options={[
                  { value: "0", label: "Select address" },
                  ...addresses.map((a) => ({
                    value: a.id.toString(),
                    label: `${a.address_line_1}, ${a.city}`,
                  })),
                ]}
              />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <Input
                label="Pickup Date"
                type="datetime-local"
                value={form.pickup_date}
                onChange={(e) => updateField("pickup_date", e.target.value)}
              />
              <Input
                label="Pickup Time Slot"
                value={form.pickup_time_slot}
                onChange={(e) =>
                  updateField("pickup_time_slot", e.target.value)
                }
                placeholder="e.g., Morning, Afternoon, Evening"
              />
              <Input
                label="Delivery Date"
                type="datetime-local"
                value={form.delivery_date}
                onChange={(e) => updateField("delivery_date", e.target.value)}
              />
              <Input
                label="Delivery Time Slot"
                value={form.delivery_time_slot}
                onChange={(e) =>
                  updateField("delivery_time_slot", e.target.value)
                }
                placeholder="e.g., Morning, Afternoon, Evening"
              />
            </div>
            <Card variant="outlined">
              <CardHeader>
                <CardTitle className="text-lg">Order Items</CardTitle>
              </CardHeader>
              <CardContent>
                {items.map((it, idx) => (
                  <div
                    key={idx}
                    className="grid grid-cols-5 gap-3 mb-4 p-4 border rounded-lg bg-gray-50"
                  >
                    <Select
                      value={it.service_id.toString()}
                      onChange={(value) =>
                        updateItem(idx, "service_id", Number(value))
                      }
                      options={[
                        { value: "0", label: "Select service" },
                        ...services.map((s) => ({
                          value: s.id.toString(),
                          label: s.name,
                        })),
                      ]}
                    />
                    <Input
                      placeholder="Item name"
                      value={it.item_name}
                      onChange={(e) =>
                        updateItem(idx, "item_name", e.target.value)
                      }
                    />
                    <Input
                      placeholder="Item type"
                      value={it.item_type}
                      onChange={(e) =>
                        updateItem(idx, "item_type", e.target.value)
                      }
                    />
                    <Input
                      type="number"
                      placeholder="Qty"
                      value={it.quantity}
                      onChange={(e) =>
                        updateItem(idx, "quantity", Number(e.target.value))
                      }
                    />
                    <Input
                      type="number"
                      step="0.01"
                      placeholder="Unit price"
                      value={it.unit_price}
                      onChange={(e) =>
                        updateItem(idx, "unit_price", Number(e.target.value))
                      }
                    />
                  </div>
                ))}
                <Button
                  type="button"
                  variant="outline"
                  onClick={addItem}
                  className="mt-2"
                >
                  + Add Item
                </Button>
              </CardContent>
            </Card>
            <Button type="submit" disabled={loading} className="w-full">
              {loading ? (
                <>
                  <LoadingSpinner size="sm" className="mr-2" />
                  Creating...
                </>
              ) : (
                "Create Order"
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </main>
  );
}
