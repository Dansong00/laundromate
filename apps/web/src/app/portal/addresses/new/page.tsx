"use client";

import { useToast } from "@/components/ToastProvider";
import { createAddress } from "@/lib/api";
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
} from "@laundromate/ui";
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
      <Card>
        <CardHeader>
          <CardTitle>Add New Address</CardTitle>
        </CardHeader>
        <CardContent>
          {error && (
            <Alert variant="destructive" className="mb-6">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Customer ID"
              type="number"
              value={form.customer_id}
              onChange={(e) => update("customer_id", Number(e.target.value))}
              required
            />
            <Input
              label="Address Line 1"
              value={form.address_line_1}
              onChange={(e) => update("address_line_1", e.target.value)}
              required
            />
            <Input
              label="Address Line 2"
              value={form.address_line_2}
              onChange={(e) => update("address_line_2", e.target.value)}
              placeholder="Apartment, suite, etc. (optional)"
            />
            <div className="grid grid-cols-3 gap-3">
              <Input
                label="City"
                value={form.city}
                onChange={(e) => update("city", e.target.value)}
                required
              />
              <Input
                label="State"
                value={form.state}
                onChange={(e) => update("state", e.target.value)}
                required
              />
              <Input
                label="ZIP Code"
                value={form.zip_code}
                onChange={(e) => update("zip_code", e.target.value)}
                required
              />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <Select
                label="Address Type"
                value={form.address_type}
                onChange={(value) => update("address_type", value)}
                options={[
                  { value: "pickup", label: "Pickup" },
                  { value: "delivery", label: "Delivery" },
                  { value: "home", label: "Home" },
                  { value: "work", label: "Work" },
                ]}
              />
              <div className="flex items-center gap-2 mt-6">
                <input
                  type="checkbox"
                  checked={form.is_default}
                  onChange={(e) => update("is_default", e.target.checked)}
                  className="rounded border-gray-300"
                />
                <span className="text-sm">Set as default</span>
              </div>
            </div>
            <Button type="submit" disabled={loading} className="w-full">
              {loading ? (
                <>
                  <LoadingSpinner size="sm" className="mr-2" />
                  Saving...
                </>
              ) : (
                "Save Address"
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </main>
  );
}
