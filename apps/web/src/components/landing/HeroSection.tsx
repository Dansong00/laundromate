import Link from "next/link";
import { Button } from "@/components/ui/button";

export function HeroSection() {
  return (
    <section className="py-24 lg:py-32">
      <div className="mx-auto max-w-4xl px-4 text-center">
        <h1 className="text-5xl font-bold tracking-tight text-gray-900 sm:text-6xl lg:text-7xl">
          The Operating System for Modern Laundromats
        </h1>
        <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600 leading-relaxed">
          Streamline your laundry business with our all-in-one platform. From
          pickup & delivery to in-store POS, LaundroMate handles the logistics
          so you can focus on growth.
        </p>
        <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link href="/auth/login">
            <Button
              size="lg"
              className="h-12 px-8 text-base bg-black text-white hover:bg-gray-900"
            >
              Get Started
            </Button>
          </Link>
          <Link href="/auth/login">
            <Button variant="outline" size="lg" className="h-12 px-8 text-base">
              Log In
            </Button>
          </Link>
        </div>
      </div>
    </section>
  );
}
