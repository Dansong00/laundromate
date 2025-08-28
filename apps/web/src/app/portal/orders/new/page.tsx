"use client";

import { useAuth } from "@/components/AuthProvider";
import { useToast } from "@/components/ToastProvider";
import {
  createOrder,
  getAuthHeader,
  listAddresses,
  listServices,
} from "@/lib/api";
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
    <main className="mx-auto max-w-2xl px-4 py-8">
      <h1 className="text-2xl font-semibold">Create order</h1>
      {error && <p className="text-red-600 mt-2">{error}</p>}
      <form onSubmit={handleSubmit} className="mt-6 grid gap-4">
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium mb-1">
              Customer ID
            </label>
            <input
              className="w-full rounded border px-3 py-2"
              type="number"
              value={form.customer_id}
              onChange={(e) =>
                updateField("customer_id", Number(e.target.value))
              }
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">
              Pickup address
            </label>
            <select
              className="w-full rounded border px-3 py-2"
              value={form.pickup_address_id}
              onChange={(e) =>
                updateField("pickup_address_id", Number(e.target.value))
              }
            >
              <option value={0}>Select address</option>
              {addresses.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.address_line_1}, {a.city}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">
              Delivery address
            </label>
            <select
              className="w-full rounded border px-3 py-2"
              value={form.delivery_address_id}
              onChange={(e) =>
                updateField("delivery_address_id", Number(e.target.value))
              }
            >
              <option value={0}>Select address</option>
              {addresses.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.address_line_1}, {a.city}
                </option>
              ))}
            </select>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium mb-1">
              Pickup date
            </label>
            <input
              className="w-full rounded border px-3 py-2"
              type="datetime-local"
              value={form.pickup_date}
              onChange={(e) => updateField("pickup_date", e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">
              Pickup time slot
            </label>
            <input
              className="w-full rounded border px-3 py-2"
              value={form.pickup_time_slot}
              onChange={(e) => updateField("pickup_time_slot", e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">
              Delivery date
            </label>
            <input
              className="w-full rounded border px-3 py-2"
              type="datetime-local"
              value={form.delivery_date}
              onChange={(e) => updateField("delivery_date", e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">
              Delivery time slot
            </label>
            <input
              className="w-full rounded border px-3 py-2"
              value={form.delivery_time_slot}
              onChange={(e) =>
                updateField("delivery_time_slot", e.target.value)
              }
            />
          </div>
        </div>
        <div className="rounded border p-4">
          <div className="font-medium mb-2">Items</div>
          {items.map((it, idx) => (
            <div key={idx} className="grid grid-cols-5 gap-2 mb-2">
              <select
                className="rounded border px-2 py-2"
                value={it.service_id}
                onChange={(e) =>
                  updateItem(idx, "service_id", Number(e.target.value))
                }
              >
                <option value={0}>Select service</option>
                {services.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.name}
                  </option>
                ))}
              </select>
              <input
                className="rounded border px-2 py-2"
                placeholder="Item name"
                value={it.item_name}
                onChange={(e) => updateItem(idx, "item_name", e.target.value)}
              />
              <input
                className="rounded border px-2 py-2"
                placeholder="Item type"
                value={it.item_type}
                onChange={(e) => updateItem(idx, "item_type", e.target.value)}
              />
              <input
                className="rounded border px-2 py-2"
                type="number"
                placeholder="Qty"
                value={it.quantity}
                onChange={(e) =>
                  updateItem(idx, "quantity", Number(e.target.value))
                }
              />
              <input
                className="rounded border px-2 py-2"
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
          <button
            type="button"
            onClick={addItem}
            className="mt-2 text-sm rounded border px-3 py-1"
          >
            Add item
          </button>
        </div>
        <button
          type="submit"
          className="rounded bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "Creating..." : "Create order"}
        </button>
      </form>
    </main>
  );
}
