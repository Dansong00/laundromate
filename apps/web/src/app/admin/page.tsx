"use client";

import { useAuth } from "@/components/AuthProvider";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { AdminPortal } from "@/components/admin/AdminPortal";
import { isSuperAdminUser, getMe, UserRead } from "@/lib/api";

export default function AdminPage() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();
  const [isSuperAdmin, setIsSuperAdmin] = useState(false);
  const [currentUser, setCurrentUser] = useState<UserRead | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace("/auth/login");
      return;
    }

    // Check if user is super admin
    const checkSuperAdminStatus = async () => {
      try {
        const user = await getMe();
        setCurrentUser(user);
        const superAdmin = isSuperAdminUser(user);
        setIsSuperAdmin(superAdmin);

        if (!superAdmin) {
          // Non-super-admins should not access the admin area
          router.replace("/portal");
        }
      } catch (error) {
        console.error("Error checking super admin status:", error);
        router.replace("/portal");
      } finally {
        setLoading(false);
      }
    };

    checkSuperAdminStatus();
  }, [isAuthenticated, router]);

  if (!isAuthenticated || loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-black mx-auto mb-4"></div>
          <p className="text-sm text-gray-500">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isSuperAdmin) {
    return null; // Will redirect to admin/portal
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <AdminPortal currentUser={currentUser} />
    </div>
  );
}
