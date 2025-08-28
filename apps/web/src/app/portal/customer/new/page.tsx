"use client";

import { useAuth } from "@/components/AuthProvider";
import { useToast } from "@/components/ToastProvider";
import { createCustomer, getAuthHeader } from "@/lib/api";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function NewCustomerPage() {
  const { isAuthenticated } = useAuth();
  const { notifySuccess, notifyError } = useToast();
  const router = useRouter();
  const [userId, setUserId] = useState<string | null>(null);
  const [preferred_pickup_time, setPreferredPickupTime] = useState("");
  const [special_instructions, setSpecialInstructions] = useState("");
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
        if (!res.ok) throw new Error("Failed to load user");
        const data = await res.json();
        setUserId(data.id);
      } catch (e) {
        setError((e as Error).message);
      }
    })();
  }, [isAuthenticated, router]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!userId) return;
    setLoading(true);
    setError(null);
    try {
      await createCustomer({
        user_id: userId,
        preferred_pickup_time,
        special_instructions,
      });
      notifySuccess("Profile created");
      router.push("/portal");
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
      <h1 className="text-2xl font-semibold">Create your customer profile</h1>
      {error && <p className="text-red-600 mt-2">{error}</p>}
      <form onSubmit={handleSubmit} className="mt-6 space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">
            Preferred pickup time
          </label>
          <input
            className="w-full rounded border px-3 py-2"
            value={preferred_pickup_time}
            onChange={(e) => setPreferredPickupTime(e.target.value)}
            placeholder="morning / afternoon / evening"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">
            Special instructions
          </label>
          <textarea
            className="w-full rounded border px-3 py-2"
            value={special_instructions}
            onChange={(e) => setSpecialInstructions(e.target.value)}
          />
        </div>
        <button
          type="submit"
          className="rounded bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 disabled:opacity-50"
          disabled={loading || !userId}
        >
          {loading ? "Saving..." : "Save profile"}
        </button>
      </form>
    </main>
  );
}
