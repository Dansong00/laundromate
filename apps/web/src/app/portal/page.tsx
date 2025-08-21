"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";

export default function PortalPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace("/auth/login");
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) return null;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold">Customer Portal</h1>
      <p className="text-gray-600 mt-2">Welcome back.</p>
    </div>
  );
}


