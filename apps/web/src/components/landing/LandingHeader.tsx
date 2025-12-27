import Link from "next/link";
import { Button } from "@/components/ui/button";

export function LandingHeader() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-white/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
        <div className="flex items-center gap-2 font-bold text-xl tracking-tight">
          <span className="text-gray-900">Laundro</span>
          <span className="text-gray-600">Mate</span>
        </div>
        <div className="flex items-center gap-4">
          <Link href="/auth/login">
            <Button variant="ghost" size="sm">
              Log in
            </Button>
          </Link>
          <Link href="/auth/login">
            <Button size="sm" className="bg-black text-white hover:bg-gray-900">
              Get Started
            </Button>
          </Link>
        </div>
      </div>
    </header>
  );
}
