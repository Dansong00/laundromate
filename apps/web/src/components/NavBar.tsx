"use client";

import { useAuth } from "@/components/AuthProvider";
import Link from "next/link";
import { useRouter } from "next/navigation";

export function NavBar() {
  const { isAuthenticated, logout } = useAuth();
  const router = useRouter();

  function handleLogout() {
    logout();
    router.push("/");
  }

  return (
    <header className="w-full border-b">
      <div className="mx-auto max-w-6xl px-4 py-3 flex items-center justify-between">
        <Link href="/" className="font-semibold text-lg">LaundroMate</Link>
        <nav className="flex items-center gap-4">
          <Link href="/" className="text-sm">Home</Link>
          {isAuthenticated ? (
            <>
              <Link href="/portal" className="text-sm">Portal</Link>
              <button
                onClick={handleLogout}
                className="text-sm rounded bg-black text-white px-3 py-1"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link href="/auth/login" className="text-sm">Login</Link>
              <Link
                href="/auth/register"
                className="text-sm rounded bg-black text-white px-3 py-1"
              >
                Get Started
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}


