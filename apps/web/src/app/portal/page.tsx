"use client";

import { useAuth } from "@/components/AuthProvider";
import { getAuthHeader } from "@/lib/api";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function PortalPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();
  const [me, setMe] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace("/auth/login");
      return;
    }
    (async () => {
      try {
        const res = await fetch("/api/me", {
          headers: {
            ...getAuthHeader(),
          },
          cache: "no-store",
        });
        if (!res.ok) throw new Error("Failed to fetch profile");
        const data = await res.json();
        setMe(data);
      } catch (e) {
        setError((e as Error).message);
      }
    })();
  }, [isAuthenticated, router]);

  if (!isAuthenticated) return null;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold">Customer Portal</h1>
      {error && <p className="text-red-600 mt-2">{error}</p>}
      {me ? (
        <div className="mt-3 text-gray-700">
          <p>
            Signed in as <span className="font-medium">{me.email}</span>
          </p>
        </div>
      ) : (
        <p className="text-gray-600 mt-2">Loading your account...</p>
      )}
    </div>
  );
}


