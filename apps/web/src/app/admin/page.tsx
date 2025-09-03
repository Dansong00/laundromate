"use client";

import { useAuth } from "@/components/AuthProvider";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { AdminPortal } from "@/components/admin/AdminPortal";
import { isAdminUser } from "@/lib/api";

export default function AdminPage() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();
  const [isAdmin, setIsAdmin] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace("/auth/login");
      return;
    }

    // Check if user is admin (you'll need to implement this based on your backend)
    const checkAdminStatus = async () => {
      try {
        const res = await fetch("/api/me", {
          headers: {
            Authorization: `Bearer ${sessionStorage.getItem("access_token")}`,
          },
        });

        if (res.ok) {
          const user = await res.json();
          // Check for admin role from database
          const isAdmin = isAdminUser(user);
          setIsAdmin(isAdmin);

          if (!isAdmin) {
            router.replace("/portal"); // Redirect non-admin users to customer portal
          }
        }
      } catch (error) {
        console.error("Error checking admin status:", error);
        router.replace("/portal");
      } finally {
        setLoading(false);
      }
    };

    checkAdminStatus();
  }, [isAuthenticated, router]);

  if (!isAuthenticated || loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-sm text-gray-500">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAdmin) {
    return null; // Will redirect to customer portal
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <AdminPortal onBackToMobile={() => router.push("/portal")} />
    </div>
  );
}
