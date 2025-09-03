"use client";

import { useAuth } from "@/components/AuthProvider";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";

export function PortalHeader() {
  const { logout } = useAuth();
  const router = useRouter();

  async function handleLogout() {
    try {
      await fetch("/api/session/logout", { method: "POST" });
    } catch {
      // ignore
    }
    sessionStorage.removeItem("access_token");
    logout();
    router.push("/");
  }

  return (
    <header className="bg-white border-b border-gray-200 px-4 py-3">
      <div className="mobile-container">
        <div className="flex items-center justify-between">
          <Link
            href="/"
            className="flex items-center gap-2 font-semibold text-lg"
            aria-label="LaundroMate home"
          >
            <Image
              src="/logo-mark.svg"
              alt="LaundroMate logo"
              width={24}
              height={24}
            />
            <span>LaundroMate</span>
          </Link>

          <button
            onClick={handleLogout}
            className="text-sm text-gray-500 hover:text-gray-700 px-3 py-1 rounded-lg hover:bg-gray-100 transition-colors"
          >
            Logout
          </button>
        </div>
      </div>
    </header>
  );
}
