"use client";

import { useToast } from "@/components/ToastProvider";
import { createAddress } from "@/lib/api";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function NewAddressPage() {
  const router = useRouter();
  const { notifySuccess, notifyError } = useToast();
  const params = new URLSearchParams(
    typeof window !== "undefined" ? window.location.search : ""
  );
  const defaultCustomerId = Number(params.get("customer_id") || 0);
  const [form, setForm] = useState({
    customer_id: defaultCustomerId,
    address_line_1: "",
    address_line_2: "",
    city: "",
    state: "",
    zip_code: "",
    address_type: "pickup",
    is_default: false,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function update<K extends keyof typeof form>(
    k: K,
    v: string | number | boolean
  ) {
    setForm((f) => ({ ...f, [k]: v }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const payload = { ...form } as any;
      payload.customer_id = Number(payload.customer_id);
      await createAddress(payload);
      notifySuccess("Address added");
      router.push(`/portal/addresses?customer_id=${payload.customer_id}`);
    } catch (e) {
      const msg = (e as Error).message;
      setError(msg);
      notifyError(msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-xl px-4 py-8">
      <h1 className="text-2xl font-semibold">Add address</h1>
      {error && <p className="text-red-600 mt-2">{error}</p>}
      <form onSubmit={handleSubmit} className="mt-6 grid gap-3">
        <div>
          <label className="block text-sm font-medium mb-1">Customer ID</label>
          <input
            className="w-full rounded border px-3 py-2"
            type="number"
            value={form.customer_id}
            onChange={(e) => update("customer_id", Number(e.target.value))}
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">
            Address line 1
          </label>
          <input
            className="w-full rounded border px-3 py-2"
            value={form.address_line_1}
            onChange={(e) => update("address_line_1", e.target.value)}
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">
            Address line 2
          </label>
          <input
            className="w-full rounded border px-3 py-2"
            value={form.address_line_2}
            onChange={(e) => update("address_line_2", e.target.value)}
          />
        </div>
        <div className="grid grid-cols-3 gap-3">
          <div>
            <label className="block text-sm font-medium mb-1">City</label>
            <input
              className="w-full rounded border px-3 py-2"
              value={form.city}
              onChange={(e) => update("city", e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">State</label>
            <input
              className="w-full rounded border px-3 py-2"
              value={form.state}
              onChange={(e) => update("state", e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">ZIP</label>
            <input
              className="w-full rounded border px-3 py-2"
              value={form.zip_code}
              onChange={(e) => update("zip_code", e.target.value)}
              required
            />
          </div>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium mb-1">
              Address type
            </label>
            <select
              className="w-full rounded border px-3 py-2"
              value={form.address_type}
              onChange={(e) => update("address_type", e.target.value)}
            >
              <option value="pickup">pickup</option>
              <option value="delivery">delivery</option>
              <option value="home">home</option>
              <option value="work">work</option>
            </select>
          </div>
          <label className="flex items-center gap-2 mt-6">
            <input
              type="checkbox"
              checked={form.is_default}
              onChange={(e) => update("is_default", e.target.checked)}
            />
            <span className="text-sm">Set as default</span>
          </label>
        </div>
        <button
          type="submit"
          className="rounded bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "Saving..." : "Save address"}
        </button>
      </form>
    </main>
  );
}
